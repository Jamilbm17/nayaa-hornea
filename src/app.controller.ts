import { Controller, Get, Header } from '@nestjs/common';
import { CatalogService } from './catalog/catalog.service';
import { renderHome } from './views/render';

@Controller()
export class AppController {
  constructor(private readonly catalog: CatalogService) {}

  @Get()
  @Header('Content-Type', 'text/html; charset=utf-8')
  home(): string {
    return renderHome(this.catalog.home());
  }
}
