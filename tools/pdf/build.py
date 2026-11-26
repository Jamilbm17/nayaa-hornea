"""Genera catalogo.html (y luego el PDF con Chrome). Ejecutar: python build.py"""
import math
import random
import subprocess
import urllib.parse
from pathlib import Path

HERE = Path(__file__).parent
WHATSAPP = "937 237 779"
INSTAGRAM = "@naaya_hornea"

GREENS = ["#123a22", "#174a2b", "#1d5a33", "#24693c", "#2f7a47", "#3b8d52"]


# ---------- recorte de fotos: centra (cx, cy) de la foto 3:4 en un marco W x H ----------
def crop(src, W, H, cx, cy, z, alt=""):
    w = W * z
    h = w * 4 / 3
    if h < H:  # asegurar que cubre el marco
        h = H
        w = h * 3 / 4
    left = min(0, max(W - w, W / 2 - cx * w))
    top = min(0, max(H - h, H / 2 - cy * h))
    return (f'<img src="img/{src}.jpg" alt="{alt}" '
            f'style="position:absolute;width:{w:.1f}px;height:{h:.1f}px;left:{left:.1f}px;top:{top:.1f}px">')


# ---------- guirnalda de pino generada ----------
def garland(seed, width=794, height=130):
    rnd = random.Random(seed)
    parts = []
    base = lambda x: 44 + 7 * math.sin(x / 70 + seed)
    needles = []
    for _ in range(1500):
        x = rnd.uniform(-20, width + 20)
        y = base(x) + rnd.gauss(0, 13)
        a = rnd.uniform(0, 2 * math.pi)
        L = rnd.uniform(12, 26)
        shade = min(len(GREENS) - 1, max(0, int(rnd.gauss(2.5, 1.4))))
        needles.append((shade, x, y, a, L))
    needles.sort()
    for shade, x, y, a, L in needles:
        x2, y2 = x + L * math.cos(a), y + L * math.sin(a)
        parts.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{GREENS[shade]}" stroke-width="2.6" stroke-linecap="round"/>')
    # nieve sobre las ramas
    for _ in range(110):
        x = rnd.uniform(0, width)
        y = base(x) + rnd.gauss(-6, 9)
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(1, 2.4):.1f}" fill="#fff" opacity="{rnd.uniform(.55, .95):.2f}"/>')
    # adornos
    x = rnd.uniform(10, 40)
    k = 0
    while x < width - 10:
        y = base(x) + rnd.gauss(0, 7)
        kind = k % 3
        if kind == 0:  # bayas
            for dx, dy in [(-5, 0), (5, -2), (0, 6)]:
                parts.append(f'<circle cx="{x+dx:.1f}" cy="{y+dy:.1f}" r="5.2" fill="url(#gBerry)"/>')
        elif kind == 1:  # esfera dorada
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="url(#gGold)"/>')
            parts.append(f'<circle cx="{x-3:.1f}" cy="{y-3:.1f}" r="2.4" fill="#fff" opacity=".7"/>')
        else:  # esfera roja
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="url(#gRedBall)"/>')
            parts.append(f'<circle cx="{x-2.5:.1f}" cy="{y-3:.1f}" r="2.2" fill="#fff" opacity=".6"/>')
        x += rnd.uniform(48, 78)
        k += 1
    defs = """<defs>
<radialGradient id="gBerry" cx=".35" cy=".35" r=".7"><stop offset="0" stop-color="#ff5a5a"/><stop offset="1" stop-color="#9c0d14"/></radialGradient>
<radialGradient id="gGold" cx=".35" cy=".35" r=".75"><stop offset="0" stop-color="#fff1b8"/><stop offset=".5" stop-color="#e2b04a"/><stop offset="1" stop-color="#8f6418"/></radialGradient>
<radialGradient id="gRedBall" cx=".35" cy=".35" r=".75"><stop offset="0" stop-color="#ff6b6b"/><stop offset=".55" stop-color="#c8141f"/><stop offset="1" stop-color="#6e0a10"/></radialGradient>
</defs>"""
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">{defs}{"".join(parts)}</svg>'
    return "data:image/svg+xml," + urllib.parse.quote(svg)


# ---------- patrón del fondo rojo ----------
def pattern():
    flake = ('<g stroke="#fff" stroke-width="1.6" stroke-linecap="round" fill="none">'
             + "".join(f'<g transform="rotate({a})"><path d="M0 0V-9M0 -5l-3 -3M0 -5l3 -3"/></g>' for a in range(0, 360, 60))
             + '</g>')
    tree = '<path d="M0 -10 L7 2 H3 L9 11 H-9 L-3 2 H-7 Z" fill="#fff"/>'
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="140" height="140" viewBox="0 0 140 140" opacity=".09">'
           f'<g transform="translate(30 32)">{flake}</g>'
           f'<g transform="translate(100 98)">{flake}</g>'
           f'<g transform="translate(102 30) scale(.9)">{tree}</g>'
           f'<g transform="translate(32 104) scale(.9)">{tree}</g>'
           f'<circle cx="68" cy="66" r="2.2" fill="#fff"/><circle cx="8" cy="72" r="1.6" fill="#fff"/><circle cx="70" cy="8" r="1.6" fill="#fff"/>'
           f'</svg>')
    return "data:image/svg+xml," + urllib.parse.quote(svg)


SYMBOLS = """
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
<defs>
  <linearGradient id="ribbon" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e3222d"/><stop offset="1" stop-color="#8e0c14"/></linearGradient>
  <linearGradient id="ribbonDark" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9e0f17"/><stop offset="1" stop-color="#5e070c"/></linearGradient>
  <radialGradient id="ballHi" cx=".32" cy=".3" r=".75"><stop offset="0" stop-color="#fff" stop-opacity=".75"/><stop offset=".35" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".35"/></radialGradient>
  <linearGradient id="goldLin" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f6dc8a"/><stop offset=".5" stop-color="#c8963e"/><stop offset="1" stop-color="#8a6116"/></linearGradient>
</defs>
<symbol id="bow" viewBox="-80 -50 160 125">
  <path d="M-6 6 L-40 70 L-28 63 L-20 75 L4 10 Z" fill="url(#ribbonDark)"/>
  <path d="M6 6 L40 70 L28 63 L20 75 L-4 10 Z" fill="url(#ribbonDark)"/>
  <path d="M0 0 C-18 -42 -76 -50 -72 -8 C-69 24 -24 18 0 0 Z" fill="url(#ribbon)"/>
  <path d="M0 0 C18 -42 76 -50 72 -8 C69 24 24 18 0 0 Z" fill="url(#ribbon)"/>
  <path d="M-4 -2 C-20 -26 -50 -30 -52 -10 C-40 -18 -20 -14 -4 -2 Z" fill="#5e070c" opacity=".55"/>
  <path d="M4 -2 C20 -26 50 -30 52 -10 C40 -18 20 -14 4 -2 Z" fill="#5e070c" opacity=".55"/>
  <path d="M-60 -22 C-50 -36 -30 -36 -18 -24" stroke="#ff7a7a" stroke-width="3" fill="none" opacity=".6" stroke-linecap="round"/>
  <path d="M60 -22 C50 -36 30 -36 18 -24" stroke="#ff7a7a" stroke-width="3" fill="none" opacity=".6" stroke-linecap="round"/>
  <ellipse cx="0" cy="2" rx="13" ry="12" fill="url(#ribbon)" stroke="#6e0a10" stroke-width="1.5"/>
  <ellipse cx="-3" cy="-2" rx="5" ry="3" fill="#ff8a8a" opacity=".55"/>
</symbol>
<symbol id="ornament" viewBox="-22 -32 44 56">
  <path d="M0 -31 a4 4 0 1 1 0.1 0" fill="none" stroke="#c8963e" stroke-width="1.6"/>
  <rect x="-6" y="-27" width="12" height="8" rx="1.5" fill="url(#goldLin)"/>
  <circle r="19" cy="2" fill="currentColor"/>
  <path d="M-18 -4 Q0 4 18 -4 L18 2 Q0 10 -18 2 Z" fill="#f3d27a" opacity=".85"/>
  <circle r="19" cy="2" fill="url(#ballHi)"/>
</symbol>
<symbol id="ornplain" viewBox="-22 -32 44 56">
  <rect x="-6" y="-27" width="12" height="8" rx="1.5" fill="url(#goldLin)"/>
  <circle r="19" cy="2" fill="currentColor"/>
  <circle r="19" cy="2" fill="url(#ballHi)"/>
</symbol>
<symbol id="flake" viewBox="-12 -12 24 24">
  <g stroke="currentColor" stroke-width="1.5" stroke-linecap="round" fill="none">
    <g><path d="M0 0V-11M0 -6l-3.5 -3.5M0 -6l3.5 -3.5"/></g>
    <g transform="rotate(60)"><path d="M0 0V-11M0 -6l-3.5 -3.5M0 -6l3.5 -3.5"/></g>
    <g transform="rotate(120)"><path d="M0 0V-11M0 -6l-3.5 -3.5M0 -6l3.5 -3.5"/></g>
    <g transform="rotate(180)"><path d="M0 0V-11M0 -6l-3.5 -3.5M0 -6l3.5 -3.5"/></g>
    <g transform="rotate(240)"><path d="M0 0V-11M0 -6l-3.5 -3.5M0 -6l3.5 -3.5"/></g>
    <g transform="rotate(300)"><path d="M0 0V-11M0 -6l-3.5 -3.5M0 -6l3.5 -3.5"/></g>
  </g>
</symbol>
<symbol id="holly" viewBox="-40 -24 80 44">
  <path d="M0 0 C-6 -8 -14 -6 -16 -12 C-20 -8 -24 -12 -28 -8 C-28 -14 -34 -16 -36 -14 C-30 -6 -24 4 -14 6 C-10 2 -6 4 0 0 Z" fill="#1d5a33"/>
  <path d="M0 0 C6 -8 14 -6 16 -12 C20 -8 24 -12 28 -8 C28 -14 34 -16 36 -14 C30 -6 24 4 14 6 C10 2 6 4 0 0 Z" fill="#24693c"/>
  <path d="M0 0 C-10 -4 -22 -6 -32 -12 M0 0 C10 -4 22 -6 32 -12" stroke="#3b8d52" stroke-width="1.2" fill="none"/>
  <circle cx="-5" cy="2" r="6" fill="#c8141f"/><circle cx="5" cy="3" r="6" fill="#d61a26"/><circle cx="0" cy="-5" r="6" fill="#b3101a"/>
  <circle cx="-7" cy="0" r="1.8" fill="#fff" opacity=".7"/><circle cx="3" cy="1" r="1.8" fill="#fff" opacity=".7"/><circle cx="-2" cy="-7" r="1.8" fill="#fff" opacity=".7"/>
</symbol>
<symbol id="tree" viewBox="-30 -50 60 80">
  <path d="M0 -44 L14 -22 H8 L22 -2 H12 L28 20 H-28 L-12 -2 H-22 L-8 -22 H-14 Z" fill="currentColor"/>
  <rect x="-4" y="20" width="8" height="8" fill="#7a4a24"/>
  <path d="M0 -50 l2.4 5 5.4 .6 -4 3.6 1.2 5.3 L0 -38.8 -5 -35.5 -3.8 -40.8 -7.8 -44.4 -2.4 -45 Z" fill="#e8b84a"/>
  <circle cx="-6" cy="-14" r="2.2" fill="#c8141f"/><circle cx="7" cy="2" r="2.2" fill="#e8b84a"/><circle cx="-10" cy="10" r="2.2" fill="#c8141f"/><circle cx="12" cy="14" r="2.2" fill="#fff"/>
</symbol>
<symbol id="star" viewBox="-12 -12 24 24">
  <path d="M0 -11 l3.2 6.6 7.3 1 -5.3 5.1 1.3 7.2 L0 5.5 -6.5 8.9 -5.2 1.7 -10.5 -3.4 -3.2 -4.4 Z" fill="currentColor"/>
</symbol>
<symbol id="cane" viewBox="-14 -30 28 60">
  <clipPath id="caneClip"><path d="M4 28 V-14 A8 8 0 0 0 -12 -14" fill="none" stroke="#000" stroke-width="7"/></clipPath>
  <path d="M4 28 V-14 A8 8 0 0 0 -12 -14" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round"/>
  <path d="M4 28 V-14 A8 8 0 0 0 -12 -14" fill="none" stroke="#d61a26" stroke-width="7" stroke-dasharray="4 4" stroke-linecap="butt"/>
</symbol>
<symbol id="snowhills" viewBox="0 0 800 160" preserveAspectRatio="none">
  <path d="M0 70 C120 20 220 30 330 62 C450 96 560 30 680 40 C740 45 780 60 800 66 V160 H0 Z" fill="#e6eef4"/>
  <path d="M0 105 C140 70 260 80 380 100 C520 124 620 76 800 92 V160 H0 Z" fill="#fff"/>
</symbol>
</defs>
</svg>
"""


MODE = "final"


def page_shell(inner, seed, extra=""):
    if MODE == "bg":  # solo el marco, guirnaldas y lazo: se convierte en UNA imagen compartida
        return f"""
<section class="page">
  <div class="frame"><div class="card"></div></div>
  <img class="garland top" src="{garland(11)}" alt="">
  <img class="garland bottom" src="{garland(18)}" alt="">
  <svg class="bow"><use href="#bow"/></svg>
</section>"""
    return f"""
<section class="page">
  <div class="frame"><div class="card">{inner}</div></div>
  {extra}
</section>"""


def tag(price):
    return f"""<svg class="tag" viewBox="0 0 110 160">
  <path d="M55 -14 L55 22" stroke="#c8963e" stroke-width="2"/>
  <path d="M22 4 H88 L106 24 V150 Q106 156 100 156 H10 Q4 156 4 150 V24 Z" fill="#1d5a33" stroke="#e2b04a" stroke-width="3"/>
  <path d="M25 13 H85 L97 27 V145 H13 V27 Z" fill="none" stroke="#e2b04a" stroke-width="1.2" stroke-dasharray="4 3"/>
  <circle cx="55" cy="26" r="6" fill="#fff7e8" stroke="#e2b04a" stroke-width="2"/>
  <text x="55" y="58" text-anchor="middle" font-family="Quicksand" font-weight="700" font-size="12" letter-spacing="3" fill="#f3d27a">PRECIO</text>
  <text x="55" y="88" text-anchor="middle" font-family="Mountains of Christmas" font-weight="700" font-size="26" fill="#fff">S/</text>
  <text x="55" y="132" text-anchor="middle" font-family="Mountains of Christmas" font-weight="700" font-size="52" fill="#fff">{price}</text>
</svg>"""


def polaroid(img_html, caption, rot, extra_style=""):
    return f"""<figure class="polaroid" style="transform:rotate({rot}deg);{extra_style}">
  <span class="tape"></span>
  <div class="ph">{img_html}</div>
  <figcaption>{caption}</figcaption>
</figure>"""


HERO_W, HERO_H = 626, 405
HH = {"01": 470, "02": 425, "03": 470}
POL = 108


def product(num, title, subtitle, blurb, price, hero, items, pols, ribbon, seed):
    lis = "".join(f"<li>{i}</li>" for i in items)
    inner = f"""
  <div class="kicker"><svg><use href="#star"/></svg> Opción {num} <svg><use href="#star"/></svg></div>
  <h2>{title}</h2>
  <p class="script">{subtitle}</p>
  <p class="blurb">{blurb}</p>
  <div class="hero" style="height:{HH[num]}px">
    <div class="hero-photo">{hero}</div>
    <div class="ribbon"><span>{ribbon}</span></div>
    <svg class="holly-corner"><use href="#holly"/></svg>
    {tag(price)}
  </div>
  <div class="bottom">
    <div class="contents">
      <h3>¿Qué contiene?</h3>
      <ul class="spec">{lis}</ul>
    </div>
    <div class="pols">{pols[0]}</div>
  </div>"""
    return page_shell(inner, seed)


def build():
    pages = []

    # ---------------- PORTADA ----------------
    hang = ""
    for x, L, color, sc in [(70, 150, "#c8141f", 1.15), (138, 95, "#e2b04a", .9), (205, 175, "#1d5a33", 1.0),
                            (590, 170, "#1d5a33", 1.0), (657, 100, "#c8141f", .95), (725, 155, "#e2b04a", 1.15)]:
        hang += (f'<div class="hang" style="left:{x}px;height:{L}px"></div>'
                 f'<svg class="orn" style="left:{x - 24*sc}px;top:{L + 40}px;width:{48*sc}px;height:{61*sc}px;color:{color}"><use href="#ornament"/></svg>')
    flakes = "".join(
        f'<svg class="flk" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px"><use href="#flake"/></svg>'
        for x, y, s in [(110, 300, 22), (660, 330, 26), (60, 470, 16), (720, 520, 18), (380, 250, 14), (300, 560, 12), (500, 590, 14)])
    covers = [
        ("6", 188, 258, .5, .5, 1.0, "Colección de galletas"),
        ("2", 232, 318, .5, .5, 1.0, "Casita navideña"),
        ("3", 188, 258, .5, .5, 1.0, "Cajita para decorar"),
    ]
    arches = ""
    for src, W, H, cx, cy, z, label in covers:
        arches += (f'<div class="arch-wrap"><div class="arch" style="width:{W}px;height:{H}px">{crop(src, W, H, cx, cy, z, label)}</div>'
                   f'<div class="arch-label">{label}</div></div>')
    cover_inner = f"""
  {flakes}
  <div class="cover-top">
    <div class="season"><svg><use href="#star"/></svg> Temporada 2026 <svg><use href="#star"/></svg></div>
    <h1><span class="c1">Catálogo</span><span class="c2">Navideño</span></h1>
    <p class="script big">galletas hechas con amor para esta Navidad</p>
    <p class="blurb cover-blurb">Horneadas a mano, con cariño y con el sabor de la Navidad de siempre. Gracias por dejarnos ser parte de tu mesa y de tus momentos más bonitos.</p>
  </div>
  <div class="arches">{arches}</div>
  <div class="snow-foot">
    <svg class="hills" preserveAspectRatio="none"><use href="#snowhills"/></svg>
    <svg class="t t1"><use href="#tree"/></svg><svg class="t t2"><use href="#tree"/></svg>
    <svg class="t t3"><use href="#tree"/></svg><svg class="t t4"><use href="#tree"/></svg>
    <div class="brand-foot"><div class="ig">{INSTAGRAM}</div><div class="wa">Pedidos por WhatsApp · {WHATSAPP}</div></div>
  </div>"""
    pages.append(page_shell(cover_inner, 3, f'<div class="hangers">{hang}</div>').replace('class="page"', 'class="page cover"', 1))

    # ---------------- PRODUCTOS ----------------
    pages.append(product(
        "01", "Caja colección de galletas", "un pedacito de cariño para regalar",
        "Una cajita llena de sabores y formas navideñas, horneadas a mano y envueltas con mucho cariño, perfecta para sorprender a quien más quieres.", "25",
        crop("6", HERO_W, HH["01"], .5, .66, 1.0, "Caja colección lista para regalar"),
        ["<b>Variedad de galletas:</b> 5 mini chips, 5 polvorones, 3 choco brownie, 4 niditos de amor y 11 estrellitas.",
         "<b>Galletas navideñas:</b> 1 árbol y 1 muñeco de jengibre.",
         "<b>Bien cuidadas:</b> cada galletita va en su capacillo, acomodada con cariño.",
         "<b>Presentación:</b> caja kraft con ventana y lazo."],
        [polaroid(crop("1", POL, POL, .50, .74, 1.7), "por dentro", -5)],
        "Lista para regalar", 11))

    pages.append(product(
        "02", "Caja de casita navideña", "armen juntos una casita de ensueño",
        "Una tarde de risas, glasé y mucha imaginación para armar y decorar tu propia casita y crear recuerdos que se quedan en el corazón.", "45",
        crop("2", HERO_W, HH["02"], .5, .55, 1.0, "Caja Feliz Navidad"),
        ["<b>Casita para armar:</b> piezas de galleta (paredes, techo y base de casita) con relieve de puerta y ventanas.",
         "<b>3 mangas de glasé real:</b> verde, blanco y rojo, para pegar las piezas y decorar.",
         "<b>Para decorar:</b> lentejitas, marshmallows y grageas navideñas.",
         "<b>Galletas decorativas:</b> 1 muñeco de jengibre y 1 árbol.",
         "<b>Para la escena:</b> 1 bastón de caramelo.",
         "<b>Para jugar:</b> dibujo para pintar, carta para Santa Claus e instrucciones paso a paso.",
         "<b>Presentación:</b> caja “Feliz Navidad”."],
        [polaroid(crop("4", POL, POL, .50, .74, 1.7), "todo lo que trae", -4)],
        "Diversión para toda la familia", 21))

    pages.append(product(
        "03", "Cajita para decorar galletas", "el detalle perfecto para los peques",
        "Un detalle pequeño y lleno de ternura, para que los más chiquitos se diviertan decorando y regalen una sonrisa.", "15",
        crop("3", HERO_W, HH["03"], .5, .62, 1.0, "Cajita con lazo rojo"),
        ["<b>6 galletas para decorar:</b> entre ellas el muñeco de jengibre y el árbol.",
         "<b>2 mangas de glasé real:</b> rojo y verde, para dar vida a tus galletas.",
         "<b>3 galletas mini chips:</b> para acompañar mientras decoras.",
         "<b>Presentación:</b> caja transparente con tapa roja y lazo."],
        [polaroid(crop("7", POL, POL, .56, .66, 1.6), "galletas para decorar", -5)],
        "Decora, disfruta y comparte", 31))

    # ---------------- PEDIDOS ----------------
    steps = [
        ("Elige tu caja", "Mira el catálogo con calma y escoge la caja que más te enamore, para regalar o para consentirte un poquito.", "#c8141f"),
        ("Escríbenos", f"Cuéntanos por WhatsApp al <b>{WHATSAPP}</b> o por Instagram <b>{INSTAGRAM}</b> qué caja quieres y para cuándo la necesitas. ¡Con mucho gusto te ayudamos!", "#1d5a33"),
        ("Confirma y recibe", "Coordinamos contigo el pago y la entrega para que tus galletas lleguen fresquitas y listas para disfrutar.", "#c8963e"),
    ]
    st = ""
    for i, (h, p, c) in enumerate(steps, 1):
        st += (f'<div class="step"><div class="ball"><svg style="color:{c}"><use href="#ornplain"/></svg><span>{i}</span></div>'
               f'<div><h4>{h}</h4><p>{p}</p></div></div>')
    order_inner = f"""
  <div class="kicker"><svg><use href="#star"/></svg> Naaya Hornea <svg><use href="#star"/></svg></div>
  <h2>¿Cómo hacer tu pedido?</h2>
  <p class="script">te lo contamos paso a paso</p>
  <div class="steps">{st}</div>
  <div class="board">
    <svg class="holly-l"><use href="#holly"/></svg>
    <h3>Nuestras cajas</h3>
    <div class="row"><span>Cajita para decorar galletas</span><i></i><b>S/ 15</b></div>
    <div class="row"><span>Caja colección de galletas</span><i></i><b>S/ 25</b></div>
    <div class="row"><span>Caja de casita navideña</span><i></i><b>S/ 45</b></div>
  </div>
  <div class="contact">
    <div class="pill wa"><svg viewBox="0 0 24 24"><path d="M12 3a9 9 0 0 0-7.8 13.5L3 21l4.6-1.2A9 9 0 1 0 12 3Z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M8.6 8.2c.3-.6.6-.6.9-.6h.6c.2 0 .4.1.5.4l.8 1.9c.1.2 0 .4-.1.6l-.5.6c-.1.1-.2.3 0 .5.4.8 1.4 1.9 2.6 2.4.2.1.4 0 .5-.1l.6-.7c.2-.2.4-.2.6-.1l1.8.9c.2.1.3.3.3.5 0 .9-.6 1.8-1.6 1.9-1.1.1-2.9-.4-4.7-2.1-1.7-1.6-2.3-3.4-2.2-4.4 0-.6.4-1.3.6-1.6Z" fill="currentColor"/></svg><div><small>WhatsApp</small>{WHATSAPP}</div></div>
    <div class="pill ig"><svg viewBox="0 0 24 24"><rect x="3.5" y="3.5" width="17" height="17" rx="5" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="17.2" cy="6.8" r="1.2" fill="currentColor"/></svg><div><small>Instagram</small>{INSTAGRAM}</div></div>
  </div>
  <div class="snow-foot order-foot">
    <svg class="hills" preserveAspectRatio="none"><use href="#snowhills"/></svg>
    <svg class="t t1"><use href="#tree"/></svg><svg class="t t4"><use href="#tree"/></svg>
    <p class="script thanks">Cada galleta se hornea con amor y se empaca pensando en ti.<br>¡Gracias por elegirnos para endulzar tu Navidad!</p>
  </div>"""
    pages.append(page_shell(order_inner, 41))

    html = TEMPLATE.replace("{{PATTERN}}", pattern()).replace("{{SYMBOLS}}", SYMBOLS).replace("{{PAGES}}", chr(10).join(pages))
    if MODE == "final":
        html = html.replace("</style>", FINAL_CSS + "</style>", 1)
    (HERE / ("bg.html" if MODE == "bg" else "catalogo.html")).write_text(html, encoding="utf-8")


FINAL_CSS = """
.page{background:url(bg.jpg) 0 0/100% 100% no-repeat!important}
.frame{background:none!important;box-shadow:none!important}
.card{background:none!important;box-shadow:none!important}
"""

TEMPLATE = r"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Catálogo Navideño - Naaya Hornea</title>
<link href="https://fonts.googleapis.com/css2?family=Mountains+of+Christmas:wght@400;700&family=Great+Vibes&family=Quicksand:wght@500;600;700&display=swap" rel="stylesheet">
<style>
@page { size: 210mm 297mm; margin: 0; }
:root{ --red:#b3121c; --red-d:#7a0c13; --cream:#fff8ea; --gold:#c8963e; --gold-l:#e2b04a; --green:#1d5a33; --ink:#3d1a14; }
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Quicksand',sans-serif;color:var(--ink);-webkit-print-color-adjust:exact;print-color-adjust:exact;background:#fff}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always;
  background:url("{{PATTERN}}") 0 0/140px 140px, radial-gradient(ellipse at 50% 40%, #c8141f 0%, #a10f18 55%, #7a0c13 100%);}
.frame{position:absolute;top:50px;left:30px;right:30px;bottom:42px;border-radius:30px;padding:9px;
  background:repeating-linear-gradient(45deg,#fff 0 9px,#d61a26 9px 18px);box-shadow:0 8px 24px rgba(0,0,0,.35)}
.card{position:relative;width:100%;height:100%;border-radius:22px;overflow:hidden;
  background:radial-gradient(circle at 20% 10%, #fffdf6 0, transparent 50%), radial-gradient(circle at 85% 90%, #fbefd6 0, transparent 55%), var(--cream);
  box-shadow:inset 0 0 0 3px var(--gold-l), inset 0 0 0 7px var(--cream), inset 0 0 0 8.5px var(--gold);
  padding:66px 34px 56px;display:flex;flex-direction:column;align-items:center}
.garland{position:absolute;left:0;width:100%;height:130px;z-index:5;pointer-events:none}
.garland.top{top:-6px}
.garland.bottom{bottom:-62px;transform:scaleY(-1)}
.bow{position:absolute;top:2px;left:50%;width:150px;height:118px;margin-left:-75px;z-index:6;filter:drop-shadow(0 4px 4px rgba(0,0,0,.35))}

.kicker{font-weight:700;font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:var(--gold);display:flex;align-items:center;gap:8px}
.kicker svg{width:12px;height:12px;color:var(--gold-l)}
h1,h2,h3,h4{font-family:'Mountains of Christmas',cursive;font-weight:700}
h2{font-size:50px;line-height:1;color:var(--red);text-align:center;margin-top:4px;text-shadow:0 2px 0 #f3d9b0}
.blurb{width:540px;text-align:center;font-size:14.5px;font-weight:600;line-height:1.45;color:var(--ink);margin-top:6px}
.script{font-family:'Great Vibes',cursive;color:var(--green);font-size:29px;line-height:1.1;margin-top:2px}

/* hero */
.hero{position:relative;width:626px;height:405px;margin-top:10px;flex:none}
.hero-photo{position:absolute;inset:0;border-radius:18px;overflow:hidden;background:#fff;
  box-shadow:0 0 0 4px #fff, 0 0 0 7px var(--gold-l), 0 10px 22px rgba(80,20,10,.28)}
.ribbon{position:absolute;left:-22px;bottom:22px;z-index:3;background:linear-gradient(#d61a26,#9e0f17);color:#fff;
  font-family:'Mountains of Christmas';font-weight:700;font-size:24px;padding:6px 26px 6px 30px;box-shadow:0 4px 8px rgba(0,0,0,.3);
  clip-path:polygon(0 0,100% 0,94% 50%,100% 100%,0 100%)}
.ribbon::before{content:"";position:absolute;left:0;bottom:-10px;border-top:10px solid #5e070c;border-left:22px solid transparent}
.ribbon span{position:relative}
.holly-corner{position:absolute;left:-26px;top:-20px;width:92px;height:52px;z-index:3;transform:rotate(-28deg);filter:drop-shadow(0 2px 2px rgba(0,0,0,.25))}
.tag{position:absolute;right:-14px;top:-8px;width:104px;height:152px;z-index:4;transform:rotate(9deg);transform-origin:50% 0;filter:drop-shadow(0 5px 6px rgba(0,0,0,.35));overflow:visible}

/* bottom */
.bottom{display:flex;gap:18px;width:626px;margin-top:22px;flex:1;min-height:0}
.contents{display:flex;flex-direction:column;flex:1;background:#fff;border-radius:16px;padding:12px 18px 10px;box-shadow:0 0 0 2px var(--gold-l), 0 6px 14px rgba(80,20,10,.12);position:relative}
.contents h3{color:var(--green);font-size:27px;line-height:1;margin-bottom:8px}
.contents ul{list-style:none}
.contents ul.two{columns:2;column-gap:14px}
.contents li{font-size:14.5px;font-weight:600;line-height:1.25;padding:0 0 7px 20px;position:relative;break-inside:avoid}
.contents li::before{content:"";position:absolute;left:0;top:2px;width:13px;height:13px;
  background:radial-gradient(circle at 35% 35%,#ff6b6b,#b3101a 70%);border-radius:50%;box-shadow:6px -4px 0 -2px #1d5a33}
.note{display:flex;align-items:center;gap:10px;font-size:13.5px;font-weight:600;font-style:italic;color:var(--red-d);margin-top:auto;border-top:1.5px dashed var(--gold-l);padding-top:7px}
.note svg{width:52px;height:30px;flex:none}
.contents ul.short li{font-size:17px;padding-bottom:12px}
.contents li{font-size:15px}
.desc{font-size:13.8px;font-weight:600;line-height:1.5;color:var(--ink);text-align:left}
.closing{display:flex;align-items:center;gap:8px;margin-top:auto;padding-top:6px;font-family:'Great Vibes',cursive;font-size:23px;line-height:1.1;color:var(--green)}
.closing svg{width:46px;height:26px;flex:none}
.contents h3{font-size:25px}
.contents ul.spec{margin-top:2px}
.contents ul.spec li{font-size:13.7px;line-height:1.36;padding:0 0 7px 20px}
.contents ul.spec li b{color:var(--green);font-weight:700}
.pols{width:150px;flex:none;display:flex;flex-direction:column;padding-top:4px}
.polaroid{width:128px;background:#fff;padding:10px 10px 6px;box-shadow:0 6px 14px rgba(60,20,10,.3);position:relative}
.polaroid .ph{position:relative;width:108px;height:108px;overflow:hidden}
.polaroid figcaption{font-family:'Great Vibes',cursive;font-size:17px;text-align:center;color:var(--ink);line-height:1.2;margin-top:2px}
.tape{position:absolute;top:-9px;left:50%;width:62px;height:20px;margin-left:-31px;z-index:2;transform:rotate(-4deg);
  background:repeating-linear-gradient(90deg,rgba(214,26,38,.75) 0 7px,rgba(255,255,255,.75) 7px 14px);opacity:.9}

/* cover */
.cover .card{padding-top:0;justify-content:flex-start}
.hangers{position:absolute;inset:0;z-index:4;pointer-events:none}
.hang{position:absolute;top:40px;width:2px;background:var(--gold-l)}
.orn{position:absolute;filter:drop-shadow(0 4px 4px rgba(0,0,0,.3))}
.flk{position:absolute;color:#c9a35a;opacity:.55}
.cover-top{text-align:center;margin-top:136px;position:relative;z-index:2}
.season{font-weight:700;font-size:13px;letter-spacing:.36em;text-transform:uppercase;color:var(--gold);display:flex;justify-content:center;gap:10px;align-items:center}
.season svg{width:13px;height:13px;color:var(--gold-l)}
h1{line-height:.86;margin-top:10px}
h1 .c1{display:block;font-size:104px;color:var(--red);text-shadow:0 3px 0 #f3d9b0}
h1 .c2{display:block;font-size:112px;color:var(--green);text-shadow:0 3px 0 #f3d9b0}
.script.big{font-size:34px;margin-top:10px}
.cover-blurb{width:580px;margin:10px auto 0;font-size:15px}
.arches{display:flex;gap:18px;align-items:flex-end;margin-top:30px;position:relative;z-index:2}
.arch-wrap{text-align:center}
.arch{position:relative;overflow:hidden;border-radius:999px 999px 16px 16px;background:#fff;
  box-shadow:0 0 0 4px #fff,0 0 0 7px var(--gold-l),0 10px 18px rgba(80,20,10,.3)}
.arch-label{font-family:'Mountains of Christmas';font-weight:700;font-size:21px;color:var(--red);margin-top:12px}
.snow-foot{position:absolute;left:0;right:0;bottom:0;height:190px;z-index:1}
.snow-foot .hills{position:absolute;left:0;bottom:0;width:100%;height:160px}
.snow-foot .t{position:absolute;color:#1d5a33}
.t1{left:22px;bottom:70px;width:62px;height:84px}
.t2{left:84px;bottom:60px;width:40px;height:54px;color:#24693c!important}
.t3{right:86px;bottom:62px;width:42px;height:56px;color:#24693c!important}
.t4{right:20px;bottom:68px;width:64px;height:86px}
.brand-foot{position:absolute;left:0;right:0;bottom:30px;text-align:center}
.brand-foot .ig{font-family:'Mountains of Christmas';font-weight:700;font-size:36px;color:var(--red)}
.brand-foot .wa{font-weight:700;font-size:14px;letter-spacing:.06em;color:var(--green)}

/* order */
.steps{width:600px;display:flex;flex-direction:column;gap:16px;margin-top:24px;position:relative;z-index:2}
.step{display:flex;gap:16px;align-items:center;background:#fff;border-radius:16px;padding:15px 20px;box-shadow:0 0 0 2px var(--gold-l),0 6px 14px rgba(80,20,10,.1)}
.ball{position:relative;width:52px;height:66px;flex:none}
.ball svg{width:52px;height:66px}
.ball span{position:absolute;left:0;right:0;top:25px;text-align:center;font-family:'Mountains of Christmas';font-weight:700;color:#fff;font-size:26px;text-shadow:0 1px 2px rgba(0,0,0,.4)}
.step h4{font-size:25px;color:var(--green);line-height:1}
.step p{font-size:14.5px;font-weight:600;line-height:1.38;margin-top:3px}
.board{position:relative;width:600px;margin-top:30px;background:var(--green);color:#fff;border-radius:18px;padding:14px 30px 16px;
  box-shadow:inset 0 0 0 3px var(--gold-l), inset 0 0 0 7px var(--green), inset 0 0 0 8px rgba(226,176,74,.6), 0 8px 16px rgba(0,0,0,.25);z-index:2}
.board h3{text-align:center;font-size:32px;color:#f3d27a;margin-bottom:4px}
.board .row{display:flex;align-items:baseline;gap:8px;font-weight:700;font-size:17px;padding:5px 0}
.board .row i{flex:1;border-bottom:2px dotted rgba(243,210,122,.7);transform:translateY(-4px)}
.board .row b{font-family:'Mountains of Christmas';font-size:26px;color:#f3d27a}
.holly-l{position:absolute;right:-24px;top:-22px;width:96px;height:54px;transform:rotate(24deg)}
.contact{display:flex;gap:16px;margin-top:30px;position:relative;z-index:2}
.pill{display:flex;align-items:center;gap:10px;background:#fff;border-radius:999px;padding:8px 22px 8px 12px;box-shadow:0 0 0 2px var(--gold-l),0 6px 12px rgba(80,20,10,.12);font-weight:700;font-size:19px;color:var(--ink)}
.pill svg{width:34px;height:34px;padding:6px;border-radius:50%;color:#fff}
.pill.wa svg{background:#1d5a33}
.pill.ig svg{background:#b3121c}
.pill small{display:block;font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);line-height:1.1}
.thanks{position:absolute;left:0;right:0;bottom:26px;text-align:center;font-size:27px;line-height:1.25;color:var(--red);z-index:2}
.order-foot{height:165px}
.order-foot .t1{bottom:52px}.order-foot .t4{bottom:50px}
.feliz{position:absolute;left:0;right:0;bottom:30px;text-align:center;font-family:'Great Vibes',cursive;font-size:44px;color:var(--red)}
</style>
</head>
<body>
{{SYMBOLS}}
{{PAGES}}
</body>
</html>
"""


def export_pdf():
    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    html = (HERE / "catalogo.html").resolve().as_uri()
    out = HERE / "Catalogo-Navideno-Naaya-Hornea.pdf"
    subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=20000", f"--print-to-pdf={out}", html], check=True)
    import pymupdf
    d = pymupdf.open(out); tmp = HERE / "opt.pdf"
    d.save(tmp, garbage=4, deflate=True, clean=True); d.close(); tmp.replace(out)
    print("PDF:", out)


def make_background():
    """Renderiza marco+guirnaldas+lazo una sola vez a imagen (2x) y la guarda como bg.jpg."""
    global MODE
    from PIL import Image
    MODE = "bg"
    build()
    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    png = HERE / "bg.png"
    subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
                    "--window-size=794,1123", "--virtual-time-budget=15000",
                    f"--screenshot={png}", (HERE / "bg.html").resolve().as_uri()], check=True)
    im = Image.open(png).convert("RGB")
    print("bg size", im.size)
    im.save(HERE / "bg.jpg", quality=88, optimize=True, progressive=True)
    png.unlink()
    MODE = "final"


if __name__ == "__main__":
    make_background()
    build()
    export_pdf()
