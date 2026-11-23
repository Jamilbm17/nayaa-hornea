import 'reflect-metadata';
import { NestFactory } from '@nestjs/core';
import { NestExpressApplication } from '@nestjs/platform-express';
import { join } from 'path';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create<NestExpressApplication>(AppModule);
  // En Vercel la carpeta public/ la sirve la CDN; en local la sirve Nest.
  app.useStaticAssets(join(__dirname, '..', 'public'), {
    maxAge: process.env.NODE_ENV === 'production' ? '7d' : 0,
  });
  const port = process.env.PORT ?? 3000;
  await app.listen(port);
  console.log(`Nayaa Hornea listo en http://localhost:${port}`);
}
bootstrap();
