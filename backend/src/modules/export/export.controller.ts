import { Controller, Get, Param, Query, Res, UseGuards } from '@nestjs/common';
import { Response } from 'express';
import { ExportService } from './export.service';
import { LeadsService } from '../leads/leads.service';
import { LeadFilterDto } from '../leads/dto/lead-filter.dto';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';

interface AuthenticatedRequest {
  user: {
    userId: string;
    email: string;
  };
}

@Controller('export')
@UseGuards(JwtAuthGuard)
export class ExportController {
  constructor(
    private readonly exportService: ExportService,
    private readonly leadsService: LeadsService,
  ) {}

  @Get('leads/post/:postId/csv')
  async exportCSV(
    @Param('postId') postId: string,
    @Query() filters: LeadFilterDto,
    @Res() res: Response,
  ) {
    const leads = await this.leadsService.findByPost(postId, (res.req as any).user.userId, filters);
    const csv = this.exportService.exportToCSV(leads);
    
    res.setHeader('Content-Type', 'text/csv');
    res.setHeader('Content-Disposition', `attachment; filename=leads-${postId}.csv`);
    res.send(csv);
  }

  @Get('leads/post/:postId/xlsx')
  async exportXLSX(
    @Param('postId') postId: string,
    @Query() filters: LeadFilterDto,
    @Res() res: Response,
  ) {
    const leads = await this.leadsService.findByPost(postId, (res.req as any).user.userId, filters);
    const xlsx = this.exportService.exportToXLSX(leads);
    
    res.setHeader('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
    res.setHeader('Content-Disposition', `attachment; filename=leads-${postId}.xlsx`);
    res.send(xlsx);
  }
}
