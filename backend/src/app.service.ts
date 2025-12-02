import { Injectable } from '@nestjs/common';

@Injectable()
export class AppService {
  getHello(): string {
    return 'Warm Lead Sourcer API - CI/CD Pipeline Active! 🚀';
  }

  getHealth(): object {
    return {
      status: 'ok',
      timestamp: new Date().toISOString(),
      service: 'warm-lead-sourcer-backend',
    };
  }
}
