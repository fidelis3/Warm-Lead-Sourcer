import { Module } from '@nestjs/common';
import { MongooseModule } from '@nestjs/mongoose';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { AppController } from './app.controller';
import { AppService } from './app.service';

@Module({
  imports: [
    // Global configuration module for environment variables
    ConfigModule.forRoot({
      isGlobal: true,
    }),
    // MongoDB connection with async configuration
    MongooseModule.forRootAsync({
      imports: [ConfigModule],
      useFactory: async (configService: ConfigService) => {
        const uri = configService.get<string>('MONGODB_URI');
        return {
          uri,
          // Connection event handlers for monitoring
          onConnectionCreate: (connection) => {
            connection.on('connected', () => {
              console.log('✅ Database connected successfully');
            });
            connection.on('error', (err) => {
              console.error('❌ Database connection error:', err);
            });
            return connection;
          },
        };
      },
      inject: [ConfigService],
    }),
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}