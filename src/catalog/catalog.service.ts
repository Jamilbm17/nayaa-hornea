import { Injectable } from '@nestjs/common';
import { BRAND, PRODUCTS, Product, STEPS } from './catalog.data';

@Injectable()
export class CatalogService {
  /** Enlace de WhatsApp con el mensaje ya escrito. */
  whatsappLink(message: string): string {
    return `https://wa.me/${BRAND.whatsapp}?text=${encodeURIComponent(message)}`;
  }

  products() {
    return PRODUCTS.map((p: Product) => ({
      ...p,
      photoUrl: `/assets/${p.photo}`,
      insideUrl: `/assets/${p.insidePhoto}`,
      orderLink: this.whatsappLink(`Hola ${BRAND.name}, quiero pedir la ${p.name} (S/ ${p.price})`),
    }));
  }

  /** Datos para la página principal. */
  home() {
    return {
      brand: BRAND,
      products: this.products(),
      steps: STEPS,
      priceList: [...PRODUCTS].sort((a, b) => a.price - b.price).map((p) => ({ name: p.name, price: p.price })),
      generalLink: this.whatsappLink(`Hola ${BRAND.name}, quiero hacer un pedido navideño`),
      instagramUrl: `https://instagram.com/${BRAND.instagram}`,
      year: new Date().getFullYear(),
    };
  }
}
