import { Controller, Get, Render } from '@nestjs/common';
import { CatalogService } from './catalog/catalog.service';

@Controller()
export class AppController {
  constructor(private readonly catalog: CatalogService) {}

  @Get()
  @Render('index')
  home() {
    return this.catalog.home();
  }
}
