// Incrusta views/index.hbs dentro del código (src/views/home.template.ts).
// Así la página no depende de leer archivos en tiempo de ejecución (necesario en Vercel).
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'views', 'index.hbs'), 'utf8');
const out =
  '// ARCHIVO GENERADO por scripts/embed-views.js a partir de views/index.hbs. No editar a mano.\n' +
  `export const HOME_TEMPLATE = ${JSON.stringify(html)};\n`;
fs.writeFileSync(path.join(root, 'src', 'views', 'home.template.ts'), out);
console.log('Plantilla incrustada en src/views/home.template.ts');
