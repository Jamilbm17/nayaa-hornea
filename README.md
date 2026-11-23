# Nayaa Hornea

Landing y catálogo navideño de **Nayaa Hornea**, hecho con NestJS (plantillas Handlebars).

## Cómo correrlo

```bash
npm install
npm run build
npm start          # http://localhost:3000
```

Para desarrollar con recarga automática: `npm run start:dev`.

## Dónde cambiar cosas

| Qué | Dónde |
| --- | --- |
| Productos, precios y textos (vienen del PDF) | `src/catalog/catalog.data.ts` |
| Número de WhatsApp e Instagram | `.env` (ver `.env.example`) |
| Diseño de la página | `views/index.hbs` y `public/css/styles.css` |
| Fotos y PDF para descargar | `public/assets/` |
| Catálogo en JSON | `GET /api/catalog` |

## Regenerar el PDF

La fuente del PDF está en `tools/pdf/` (requiere Python con `pymupdf` y `Pillow`, y Google Chrome):

```bash
cd tools/pdf
python build.py
```

Luego copia `Catalogo-Navideno-Nayaa-Hornea.pdf` a `public/assets/catalogo-navideno-nayaa-hornea.pdf`.
