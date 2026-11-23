import { Controller, Get } from '@nestjs/common';
import { CatalogService } from './catalog.service';

@Controller('api')
export class CatalogController {
  constructor(private readonly catalog: CatalogService) {}

  /** El catálogo completo en JSON (productos, precios y enlaces de pedido). */
  @Get('catalog')
  list() {
    return this.catalog.products();
  }
}
