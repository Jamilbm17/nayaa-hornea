import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { CatalogController } from './catalog/catalog.controller';
import { CatalogService } from './catalog/catalog.service';

@Module({
  controllers: [AppController, CatalogController],
  providers: [CatalogService],
})
export class AppModule {}
