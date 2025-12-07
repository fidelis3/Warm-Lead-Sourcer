import { Injectable } from '@nestjs/common';
import * as XLSX from 'xlsx';

@Injectable()
export class ExportService {
  exportToCSV(leads: any[]): string {
    const data = this.formatLeadsForExport(leads);
    const worksheet = XLSX.utils.json_to_sheet(data);
    return XLSX.utils.sheet_to_csv(worksheet);
  }

  exportToXLSX(leads: any[]): Buffer {
    const data = this.formatLeadsForExport(leads);
    const worksheet = XLSX.utils.json_to_sheet(data);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Leads');
    return XLSX.write(workbook, { type: 'buffer', bookType: 'xlsx' });
  }

  private formatLeadsForExport(leads: any[]) {
    return leads.map(lead => ({
      Name: lead.name,
      Headline: lead.headline || '',
      'Profile URL': lead.profileUrl || '',
      'Engagement Type': lead.engagementType,
      'Match Score': lead.matchScore,
      'Guessed Email': lead.guessedEmail || '',
      Country: lead.location?.country || '',
      City: lead.location?.city || '',
      University: lead.education?.[0]?.institution || '',
      Degree: lead.education?.[0]?.degree || '',
      Company: lead.experience?.[0]?.company || '',
      'Job Title': lead.experience?.[0]?.title || '',
      'Created At': new Date(lead.createdAt).toLocaleDateString(),
    }));
  }
}
