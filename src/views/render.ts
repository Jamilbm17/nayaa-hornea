import Handlebars from 'handlebars';
import { BUILD_ID } from './build-id';
import { HOME_TEMPLATE } from './home.template';

const home = Handlebars.compile(HOME_TEMPLATE);

/** Devuelve el HTML de la página principal. */
export function renderHome(data: object): string {
  return home({ ...data, assetVersion: BUILD_ID });
}
