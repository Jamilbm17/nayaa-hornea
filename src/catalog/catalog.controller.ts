import { Controller, Get, Inject } from '@nestjs/common';
import { CatalogService } from './catalog.service';

@Controller('api')
export class CatalogController {
  // @Inject explícito: funciona aunque el empaquetador (Vercel) no conserve los tipos.
  constructor(@Inject(CatalogService) private readonly catalog: CatalogService) {}

  /** El catálogo completo en JSON (productos, precios y enlaces de pedido). */
  @Get('catalog')
  list() {
    return this.catalog.products();
  }
}
