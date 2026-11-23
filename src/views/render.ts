import Handlebars from 'handlebars';
import { HOME_TEMPLATE } from './home.template';

const home = Handlebars.compile(HOME_TEMPLATE);

/** Devuelve el HTML de la página principal. */
export function renderHome(data: unknown): string {
  return home(data);
}
