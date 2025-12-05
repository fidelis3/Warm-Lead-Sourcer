import { 
  Controller, 
  Get, 
  Param, 
  Query, 
  UseGuards,
  Request 
} from '@nestjs/common';
import { LeadsService } from './leads.service';
import { LeadFilterDto } from './dto/lead-filter.dto';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';

@Controller('leads')
@UseGuards(JwtAuthGuard)
export class LeadsController {
  constructor(private readonly leadsService: LeadsService) {}

  @Get('post/:postId')
  async getLeadsByPost(
    @Param('postId') postId: string,
    @Query() filters: LeadFilterDto,
    @Request() req
  ) {
    return this.leadsService.findByPost(postId, req.user.userId, filters);
  }

  @Get('post/:postId/stats')
  async getPostStats(
    @Param('postId') postId: string,
    @Request() req
  ) {
    return this.leadsService.getStats(postId, req.user.userId);
  }
}