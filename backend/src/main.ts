import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

/**
 * Bootstrap the NestJS application
 */
async function bootstrap() {
  // Create NestJS application instance
  const app = await NestFactory.create(AppModule);
  
  // Get port from environment or default to 5000
  const port = process.env.PORT || 5000;
  
  // Start the server
  await app.listen(port);
  console.log(`🚀 Backend server running on http://localhost:${port}`);
}

// Start the application
bootstrap();
