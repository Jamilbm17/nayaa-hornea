// Fuente única de la información del catálogo (tomada del PDF "Catálogo Navideño 2026").

export interface Spec {
  label: string;
  text: string;
}

export interface Product {
  id: string;
  num: string;
  name: string;
  tagline: string;
  blurb: string;
  price: number;
  ribbon: string;
  featured?: string;
  photo: string;
  insidePhoto: string;
  insideCaption: string;
  photoFocus: string;
  specs: Spec[];
}

export const BRAND = {
  name: 'Naaya Hornea',
  season: 'Navidad 2026',
  whatsapp: process.env.WHATSAPP ?? '51937237779',
  whatsappDisplay: '937 237 779',
  instagram: process.env.INSTAGRAM ?? 'naaya_hornea',
};

export const PRODUCTS: Product[] = [
  {
    id: 'coleccion',
    num: '01',
    name: 'Caja colección de galletas',
    tagline: 'un pedacito de cariño para regalar',
    blurb:
      'Una cajita llena de sabores y formas navideñas, horneadas a mano y envueltas con mucho cariño, perfecta para sorprender a quien más quieres.',
    price: 25,
    ribbon: 'Lista para regalar',
    photo: 'caja-coleccion.jpg',
    insidePhoto: 'coleccion-dentro.jpg',
    insideCaption: 'por dentro',
    photoFocus: '50% 72%',
    specs: [
      { label: 'Variedad de galletas', text: '5 mini chips, 5 polvorones, 3 choco brownie, 4 niditos de amor y 11 estrellitas.' },
      { label: 'Galletas navideñas', text: '1 árbol y 1 muñeco de jengibre.' },
      { label: 'Bien cuidadas', text: 'cada galletita va en su capacillo, acomodada con cariño.' },
      { label: 'Presentación', text: 'caja kraft con ventana, lazo y tarjeta de agradecimiento.' },
    ],
  },
  {
    id: 'casita',
    num: '02',
    name: 'Caja de casita navideña',
    tagline: 'armen juntos una casita de ensueño',
    blurb:
      'Una tarde de risas, glasé y mucha imaginación para armar y decorar tu propia casita y crear recuerdos que se quedan en el corazón.',
    price: 45,
    ribbon: 'Diversión para toda la familia',
    featured: 'La favorita de las familias',
    photo: 'caja-casita.jpg',
    insidePhoto: 'casita-contenido.jpg',
    insideCaption: 'todo lo que trae',
    photoFocus: '50% 62%',
    specs: [
      { label: 'Casita para armar', text: 'piezas de galleta (paredes y techo) con relieve de puerta y ventanas.' },
      { label: '3 mangas de glasé real', text: 'verde, blanco y rojo, para pegar las piezas y decorar.' },
      { label: 'Para decorar', text: 'lentejitas, marshmallows y grageas navideñas.' },
      { label: 'Galletas decorativas', text: '1 muñeco de jengibre y 1 árbol.' },
      { label: 'Para la escena', text: '1 bastón de caramelo.' },
      { label: 'Para jugar', text: 'dibujo para pintar, carta para Santa Claus e instrucciones paso a paso.' },
      { label: 'Presentación', text: 'caja “Feliz Navidad” con tarjeta de agradecimiento.' },
    ],
  },
  {
    id: 'decorar',
    num: '03',
    name: 'Cajita para decorar galletas',
    tagline: 'el detalle perfecto para los peques',
    blurb: 'Un detalle pequeño y lleno de ternura, para que los más chiquitos se diviertan decorando y regalen una sonrisa.',
    price: 15,
    ribbon: 'Decora, disfruta y comparte',
    photo: 'caja-decorar.jpg',
    insidePhoto: 'decorar-contenido.jpg',
    insideCaption: 'galletas para decorar',
    photoFocus: '50% 68%',
    specs: [
      { label: '6 galletas para decorar', text: 'entre ellas el muñeco de jengibre y el árbol.' },
      { label: '2 mangas de glasé real', text: 'rojo y verde, para dar vida a tus galletas.' },
      { label: '3 galletas mini chips', text: 'para acompañar mientras decoras.' },
      { label: 'Presentación', text: 'caja transparente con tapa roja y lazo.' },
    ],
  },
];

export const STEPS = [
  { n: 1, title: 'Elige tu caja', text: 'Mira el catálogo con calma y escoge la caja que más te enamore, para regalar o para consentirte un poquito.' },
  { n: 2, title: 'Escríbenos', text: 'Cuéntanos por WhatsApp o por Instagram qué caja quieres y para cuándo la necesitas. ¡Con mucho gusto te ayudamos!' },
  { n: 3, title: 'Confirma y recibe', text: 'Coordinamos contigo el pago y la entrega para que tus galletas lleguen fresquitas y listas para disfrutar.' },
];
