import { Controller, Get, Header, Inject } from '@nestjs/common';
import { CatalogService } from './catalog/catalog.service';
import { renderHome } from './views/render';

@Controller()
export class AppController {
  // @Inject explícito: funciona aunque el empaquetador (Vercel) no conserve los tipos.
  constructor(@Inject(CatalogService) private readonly catalog: CatalogService) {}

  @Get()
  @Header('Content-Type', 'text/html; charset=utf-8')
  home(): string {
    return renderHome(this.catalog.home());
  }
}
