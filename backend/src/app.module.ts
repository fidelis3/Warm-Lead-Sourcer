import { Module } from '@nestjs/common';
import { MongooseModule } from '@nestjs/mongoose';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { ThrottlerModule, ThrottlerGuard } from '@nestjs/throttler'; 
import { APP_GUARD } from '@nestjs/core'; 
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { UserModule } from './users/user.module';

@Module({
  imports: [
    // Global configuration module for environment variables
    ConfigModule.forRoot({
      isGlobal: true,
    }),

  
    ThrottlerModule.forRoot([
      {
        ttl: 60000,   // 60 seconds
        limit: 20,    // 20 requests per minute per IP
      },
    ]),

    // MongoDB connection with async configuration
    MongooseModule.forRootAsync({
      imports: [ConfigModule],
      useFactory: (configService: ConfigService) => {
        const uri = configService.get<string>('MONGODB_URI');
        return {
          uri,
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

    UserModule,
  ],
  controllers: [AppController],
  providers: [
    AppService,
    // Apply throttling globally
    {
      provide: APP_GUARD,
      useClass: ThrottlerGuard,
    },
  ],
})
export class AppModule {}