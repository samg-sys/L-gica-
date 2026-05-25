"""
Generador de la presentacion 'Hexagramas Magicos'
Estructura inspirada en G06_PRESENTACION.pdf (Beamer-like).
Paleta MONOCROMA AZUL (varias intensidades del mismo color).

No modifica ningun archivo fuente del proyecto.

Version 3 (actualizada): basada en la v1, incorpora
  - una diapositiva nueva que explica que es un hexagrama (figura geometrica),
  - una diapositiva con la implementacion real de los SAT-solvers en Logica.py
    (filtro, dpll con unit_propagate, MiniSAT via pycosat + Minisat22),
  - los tiempos REALES medidos en los notebooks (Samuel) para los 5 solvers,
  - numeracion de pagina automatica.

Produce:
  - Presentacion_Hexagrama_v3.pptx
  - _hexagrama_figura.png / _hexagrama_solucion.png (figuras matplotlib)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

BASE = os.path.dirname(os.path.abspath(__file__))

# =============================================================
# PALETA MONOCROMA AZUL  (de mas claro a mas oscuro)
# =============================================================
B00 = RGBColor(0xF1, 0xF4, 0xFB)  # fondo casi blanco con tinte azul
B05 = RGBColor(0xE4, 0xEA, 0xF5)  # fondo soft
B10 = RGBColor(0xD2, 0xDC, 0xEE)  # lavanda muy claro (header bar)
B20 = RGBColor(0xB7, 0xC4, 0xE0)  # azul lavanda
B30 = RGBColor(0x8E, 0xA1, 0xC8)  # azul medio claro
B40 = RGBColor(0x60, 0x77, 0xA5)  # azul medio
B50 = RGBColor(0x3D, 0x55, 0x86)  # azul corporativo
B60 = RGBColor(0x29, 0x3F, 0x6C)  # azul oscuro
B70 = RGBColor(0x1A, 0x2C, 0x55)  # azul muy oscuro
B80 = RGBColor(0x0F, 0x1E, 0x3F)  # azul navy profundo
B90 = RGBColor(0x07, 0x12, 0x2A)  # casi negro azulado

INK   = B80
INK2  = B70
MUTE  = B40
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

PT = Pt

# =============================================================
# FIGURA HEXAGRAMA NUMERADO 1..12
# =============================================================
def generar_figura_hexagrama(path, casillas_nums=None):
    """Si casillas_nums = dict {casilla: num}, los pinta. Sino, 1..12."""
    fig, ax = plt.subplots(figsize=(6.4, 6.4), dpi=160)
    fig.patch.set_facecolor('#F1F4FB')
    ax.set_facecolor('#F1F4FB')

    t1 = np.array([[0, 1], [0.866, -0.5], [-0.866, -0.5]])
    t2 = np.array([[0, -1], [0.866, 0.5], [-0.866, 0.5]])
    tri1 = patches.Polygon(t1, edgecolor='#1A2C55', facecolor='none',
                           linewidth=2.6, linestyle='-', fill=False, closed=True)
    tri2 = patches.Polygon(t2, edgecolor='#1A2C55', facecolor='none',
                           linewidth=2.6, linestyle='-', fill=False, closed=True)
    ax.add_patch(tri1); ax.add_patch(tri2)
    ax.set_xlim(-1.25, 1.25); ax.set_ylim(-1.25, 1.25)
    ax.set_aspect('equal'); plt.axis('off')

    direcciones = [
        [0,  1.00], [-0.866, 0.50], [-0.2886, 0.50], [0.2886, 0.50], [0.866, 0.50],
        [-0.5773, 0], [0.5773, 0],
        [-0.866,-0.50], [-0.2886,-0.50], [0.2886,-0.50], [0.866,-0.50],
        [0, -1.00],
    ]
    for i, (x, y) in enumerate(direcciones, start=1):
        if casillas_nums and i in casillas_nums:
            valor = str(casillas_nums[i])
            fc = '#1A2C55'; col = '#FFFFFF'
        else:
            valor = str(i)
            fc = '#F1F4FB'; col = '#1A2C55'
        ax.text(x, y, valor, fontsize=15, ha='center', va='center',
                fontweight='bold', color=col,
                bbox=dict(facecolor=fc, alpha=1, edgecolor='#1A2C55',
                          boxstyle='circle,pad=0.45', linewidth=1.6))

    plt.tight_layout()
    plt.savefig(path, dpi=160, bbox_inches='tight', facecolor='#F1F4FB')
    plt.close(fig)

FIG_HEX   = os.path.join(BASE, '_hexagrama_figura.png')
FIG_HEX_S = os.path.join(BASE, '_hexagrama_solucion.png')
generar_figura_hexagrama(FIG_HEX)
# una solucion magica clasica del hexagrama (suma = 26 en cada linea)
# (3,11,5,7) (3,10,8,5) (10,11,2,...) - usamos una valida conocida:
sol = {1:3, 2:11, 3:7, 4:8, 5:5, 6:6, 7:1, 8:10, 9:2, 10:12, 11:4, 12:9}
generar_figura_hexagrama(FIG_HEX_S, sol)

# =============================================================
# PRESENTACION 16:9
# =============================================================
prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]

AUTORES = "Samuel A. Galindo  ·  John S. Valbuena  ·  Alejandro Jimenez"
TITULO_CORTO = "Hexagrama Magico"

# Contenido del seminario (para el footer page X/Y)
TOTAL_SLIDES_ESTIMADO = 53  # actualizado: deck v3 con slide de hexagrama + slide de SAT-solvers

# Contador automatico de pagina: se incrementa una vez por slide (en fondo()),
# asi insertar/eliminar diapositivas no obliga a renumerar a mano.
_PAGINA = [0]

# =============================================================
# HELPERS
# =============================================================
def fondo(slide, color=B00):
    _PAGINA[0] += 1
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, SH)
    bg.line.fill.background()
    bg.fill.solid(); bg.fill.fore_color.rgb = color
    slide.shapes._spTree.remove(bg._element)
    slide.shapes._spTree.insert(2, bg._element)
    return bg

def add_rect(slide, x, y, w, h, fill=None, line=None, line_w=0.5, shape=MSO_SHAPE.RECTANGLE):
    s = slide.shapes.add_shape(shape, x, y, w, h)
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line; s.line.width = Pt(line_w)
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid(); s.fill.fore_color.rgb = fill
    return s

def caja(slide, x, y, w, h, texto, *, size=14, color=INK,
         bold=False, italic=False, align=PP_ALIGN.LEFT,
         font='Calibri', anchor=None, line_spacing=1.15):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Emu(0)
    tf.margin_top = tf.margin_bottom = Emu(0)
    if anchor is not None:
        tf.vertical_anchor = anchor
    if isinstance(texto, str):
        texto = [texto]
    for j, item in enumerate(texto):
        par = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
        par.alignment = align
        par.line_spacing = line_spacing
        if isinstance(item, str):
            pieces = [(item, {})]
        elif isinstance(item, tuple):
            pieces = [item]
        else:
            pieces = item
        for (t, st) in pieces:
            run = par.add_run()
            run.text = t
            run.font.name = st.get('font', font)
            run.font.size = Pt(st.get('size', size))
            run.font.bold = st.get('bold', bold)
            run.font.italic = st.get('italic', italic)
            run.font.color.rgb = st.get('color', color)
    return tb

def header_bar(slide, titulo, n_pag, total_pag=None):
    """Barra superior con titulo de slide, estilo Beamer."""
    # franja superior
    barra = add_rect(slide, 0, 0, SW, Inches(0.72), fill=B10)
    # acento delgado en azul oscuro
    add_rect(slide, 0, Inches(0.72), SW, Inches(0.05), fill=B60)
    caja(slide, Inches(0.45), Inches(0.16), Inches(11.8), Inches(0.45),
         titulo, size=22, color=B80, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    if total_pag is None:
        total_pag = TOTAL_SLIDES_ESTIMADO
    # numero de pagina (automatico: usa el contador global)
    caja(slide, Inches(12.0), Inches(0.16), Inches(1.2), Inches(0.45),
         f"{_PAGINA[0]} / {total_pag}", size=11, color=B60, italic=True,
         align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)

def footer_bar(slide):
    add_rect(slide, 0, SH - Inches(0.35), SW, Inches(0.35), fill=B05)
    caja(slide, Inches(0.45), SH - Inches(0.32), Inches(7.0), Inches(0.3),
         AUTORES, size=8.5, color=B50, italic=True, anchor=MSO_ANCHOR.MIDDLE)
    caja(slide, Inches(7.5), SH - Inches(0.32), Inches(3.5), Inches(0.3),
         TITULO_CORTO, size=8.5, color=B50, italic=True,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    caja(slide, Inches(11.0), SH - Inches(0.32), Inches(2.2), Inches(0.3),
         "Bogota, Colombia  ·  Mayo 2026", size=8.5, color=B50, italic=True,
         align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)

def caja_titulada(slide, x, y, w, h, header, body, *,
                  header_color=B70, body_color=B05,
                  header_text_color=WHITE, body_text_color=INK,
                  header_size=12, body_size=11, body_font='Calibri',
                  header_height=Inches(0.36)):
    """Caja con cabecera azul oscura y cuerpo claro (estilo Beamer block)."""
    # header
    add_rect(slide, x, y, w, header_height, fill=header_color,
             shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    caja(slide, x + Inches(0.18), y, w - Inches(0.36), header_height,
         header, size=header_size, color=header_text_color, bold=True,
         anchor=MSO_ANCHOR.MIDDLE)
    # body
    body_y = y + header_height
    body_h = h - header_height
    add_rect(slide, x, body_y, w, body_h, fill=body_color,
             line=B30, line_w=0.5, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    if isinstance(body, str):
        body = [body]
    caja(slide, x + Inches(0.18), body_y + Inches(0.08),
         w - Inches(0.36), body_h - Inches(0.12),
         body, size=body_size, color=body_text_color, font=body_font,
         anchor=MSO_ANCHOR.TOP)

def bullet_list(items, size=13, color=INK, color_bullet=B50, bullet='● '):
    """Devuelve lista para usar dentro de caja() con bullets estilizados."""
    res = []
    for it in items:
        if isinstance(it, str):
            res.append([
                (bullet, {'size': size-2, 'color': color_bullet, 'bold': True}),
                (it,     {'size': size,   'color': color}),
            ])
        else:
            indent = '   '
            res.append([
                (indent + '◦ ', {'size': size-2, 'color': color_bullet}),
                (it[0],              {'size': size-1, 'color': color}),
            ])
    return res

def bloque_codigo(slide, x, y, w, h, lineas, *, titulo=None):
    """Bloque oscuro estilo editor que muestra codigo (no es captura real)."""
    add_rect(slide, x, y, w, h, fill=B90, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    # botoncitos mac
    for i, c in enumerate([RGBColor(0xFF,0x5F,0x57), RGBColor(0xFE,0xBC,0x2E),
                           RGBColor(0x28,0xC8,0x40)]):
        dot = add_rect(slide, x + Inches(0.15 + i*0.22), y + Inches(0.15),
                       Inches(0.16), Inches(0.16), fill=c, shape=MSO_SHAPE.OVAL)
    if titulo:
        caja(slide, x + Inches(1.0), y + Inches(0.1), w - Inches(2.0), Inches(0.3),
             titulo, size=10, color=B20, italic=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    # codigo
    parrafos = []
    for ln in lineas:
        # ln puede ser str o lista de (texto, color)
        if isinstance(ln, str):
            parrafos.append([(ln, {'font': 'Consolas', 'size': 11, 'color': RGBColor(0xE6,0xED,0xF8)})])
        else:
            seq = []
            for (t, st) in ln:
                seq.append((t, {'font': 'Consolas', 'size': 11,
                                'color': st.get('color', RGBColor(0xE6,0xED,0xF8)),
                                'bold': st.get('bold', False),
                                'italic': st.get('italic', False)}))
            parrafos.append(seq)
    caja(slide, x + Inches(0.35), y + Inches(0.5), w - Inches(0.6), h - Inches(0.7),
         parrafos, line_spacing=1.18)

def caja_resultado(slide, x, y, w, h, header, lineas, header_color=B60):
    """Caja tipo 'Resultado' del PDF de referencia."""
    add_rect(slide, x, y, w, Inches(0.35), fill=header_color,
             shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    caja(slide, x + Inches(0.18), y, w - Inches(0.36), Inches(0.35),
         header, size=11, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    add_rect(slide, x, y + Inches(0.35), w, h - Inches(0.35), fill=B10,
             line=B30, line_w=0.5, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    items = []
    for ln in lineas:
        if isinstance(ln, str):
            items.append([(ln, {'color': INK, 'size': 12})])
        else:
            items.append(ln)
    caja(slide, x + Inches(0.18), y + Inches(0.42), w - Inches(0.36), h - Inches(0.45),
         items, size=12, color=INK)

# =============================================================
# SLIDE 1 - PORTADA
# =============================================================
s = prs.slides.add_slide(BLANK)
fondo(s, B00)

# bloque azul oscuro grande (banda lateral)
add_rect(s, 0, 0, Inches(0.35), SH, fill=B70)
# caja titulo centrada estilo Beamer (rounded)
add_rect(s, Inches(1.2), Inches(0.7), Inches(11.0), Inches(1.7),
         fill=B10, line=B40, line_w=1.0,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE)
caja(s, Inches(1.2), Inches(0.85), Inches(11.0), Inches(0.8),
     "Hexagrama Magico", size=42, color=B80, bold=True,
     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
caja(s, Inches(1.2), Inches(1.55), Inches(11.0), Inches(0.55),
     "Formalizacion mediante Logica Proposicional y verificacion SAT",
     size=18, color=B60, italic=True,
     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
caja(s, Inches(1.2), Inches(1.95), Inches(11.0), Inches(0.45),
     "SATtabla  ·  SATtableaux  ·  DPLL  ·  WalkSAT  ·  MiniSAT22",
     size=13, color=B50,
     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# autores
caja(s, Inches(1.2), Inches(2.85), Inches(11.0), Inches(0.5),
     "Samuel Alejandro Galindo     John Sebastian Valbuena     Alejandro Jimenez",
     size=16, color=B80, align=PP_ALIGN.CENTER)

# afiliacion
caja(s, Inches(1.2), Inches(3.55), Inches(11.0), Inches(1.0),
     ["Logica para Ciencias de la Computacion",
      "Matematicas Aplicadas y Ciencias de la Computacion - MACC",
      "Escuela de Ingenieria, Ciencia y Tecnologia"],
     size=13, color=B60, italic=True, align=PP_ALIGN.CENTER)

# imagen hexagrama centrada abajo
s.shapes.add_picture(FIG_HEX, Inches(5.4), Inches(4.55),
                     width=Inches(2.6), height=Inches(2.6))

# docente y fecha
caja(s, Inches(1.2), Inches(4.7), Inches(3.8), Inches(0.5),
     "Profesor", size=10, color=B50, bold=True, align=PP_ALIGN.CENTER)
caja(s, Inches(1.2), Inches(5.0), Inches(3.8), Inches(0.5),
     "Daniel Alfonso Bojaca", size=14, color=B80, bold=True, align=PP_ALIGN.CENTER)

caja(s, Inches(8.5), Inches(4.7), Inches(3.8), Inches(0.5),
     "Fecha", size=10, color=B50, bold=True, align=PP_ALIGN.CENTER)
caja(s, Inches(8.5), Inches(5.0), Inches(3.8), Inches(0.5),
     "Mayo de 2026", size=14, color=B80, bold=True, align=PP_ALIGN.CENTER)

caja(s, Inches(1.2), Inches(7.0), Inches(11.0), Inches(0.4),
     "Bogota, Colombia  ·  Periodo 2026-01  ·  Codigo 11310035",
     size=10, color=B50, italic=True, align=PP_ALIGN.CENTER)


# =============================================================
# SLIDE 2 - CONTENIDO
# =============================================================
s = prs.slides.add_slide(BLANK)
fondo(s, B00)
header_bar(s, "Contenido", 2)
footer_bar(s)

secciones = [
    "Bienvenida e Introduccion al Problema",
    "Sistema de Representacion",
    "Reglas del Problema",
    "Arquitectura e Implementacion Computacional",
    "Metodos SAT Solver",
    "Metodologia y Analisis Experimental",
    "Resultados y Analisis Comparativo",
    "Discusion y Conclusiones",
    "Agradecimientos",
]
y = Inches(1.5)
for i, sec in enumerate(secciones, start=1):
    # bullet circular con numero
    add_rect(s, Inches(1.8), y, Inches(0.5), Inches(0.5),
             fill=B70, shape=MSO_SHAPE.OVAL)
    caja(s, Inches(1.8), y, Inches(0.5), Inches(0.5),
         str(i), size=14, color=WHITE, bold=True,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    caja(s, Inches(2.6), y, Inches(9.5), Inches(0.5),
         sec, size=18, color=B80, anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(0.55)


# =============================================================
# Funcion utilitaria: portada de seccion
# =============================================================
def slide_seccion(num, total, titulo, n_pag, subtitulo=None):
    s = prs.slides.add_slide(BLANK)
    fondo(s, B00)
    # banda azul izquierda
    add_rect(s, 0, 0, Inches(4.5), SH, fill=B70)
    # detalle vertical
    add_rect(s, Inches(4.5), 0, Inches(0.08), SH, fill=B40)
    caja(s, Inches(0.4), Inches(2.5), Inches(3.8), Inches(0.5),
         f"SECCION  {num} / {total}", size=12, color=B20, bold=True,
         align=PP_ALIGN.CENTER)
    caja(s, Inches(0.4), Inches(3.0), Inches(3.8), Inches(2.0),
         titulo, size=30, color=WHITE, bold=True,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # lado derecho - subtitulo
    if subtitulo:
        caja(s, Inches(5.0), Inches(3.2), Inches(7.8), Inches(2.0),
             subtitulo, size=18, color=B60, italic=True,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)
    # numero en footer (automatico)
    caja(s, Inches(12.0), Inches(7.05), Inches(1.2), Inches(0.3),
         f"{_PAGINA[0]} / {TOTAL_SLIDES_ESTIMADO}", size=10, color=B50, italic=True,
         align=PP_ALIGN.RIGHT)
    return s

# =============================================================
# SECCION 1 - BIENVENIDA / INTRODUCCION AL PROBLEMA
# =============================================================
slide_seccion(1, 9, "Introduccion al Problema", 3,
              "Que es un hexagrama, que lo vuelve magico y por que\nmerece ser modelado con logica proposicional.")

# ---- SLIDE: Que es un hexagrama? (concepto geometrico, antes de la version magica) ----
s = prs.slides.add_slide(BLANK); fondo(s, B00)
header_bar(s, "Que es un Hexagrama?", 0); footer_bar(s)

caja(s, Inches(0.5), Inches(1.0), Inches(7.4), Inches(0.5),
     "La figura geometrica:", size=18, color=B80, bold=True)
caja(s, Inches(0.5), Inches(1.55), Inches(7.4), Inches(3.6),
     bullet_list([
       "Es una estrella de seis puntas: una de las figuras geometricas mas antiguas y reconocibles.",
       "Se forma al superponer DOS triangulos equilateros iguales, uno apuntando hacia arriba y otro hacia abajo.",
       "En geometria es el poligono estrellado { 6 / 2 }: 6 vertices que se unen saltando de 2 en 2.",
       "Al cruzarse los triangulos aparece un hexagono regular en el centro y 6 puntas triangulares alrededor.",
       "Tambien se le conoce como Estrella de David o Sello de Salomon, con fuerte carga simbolica en varias culturas.",
     ], size=13))

caja_titulada(s, Inches(0.5), Inches(5.25), Inches(7.4), Inches(1.65),
              "Hexagrama  vs.  Hexagrama magico",
              [
                "Hexagrama = la figura (la estrella de 6 puntas).",
                "Hexagrama magico = colocar los numeros 1..12 en sus 12 casillas de modo que las 6 lineas rectas sumen todas lo mismo (M = 26).",
                "Eso ultimo es lo que formalizamos y resolvemos en este proyecto.",
              ],
              header_color=B70, body_color=B05, body_size=12)

s.shapes.add_picture(FIG_HEX, Inches(8.2), Inches(1.4),
                     width=Inches(4.6), height=Inches(4.6))
caja(s, Inches(8.2), Inches(6.05), Inches(4.6), Inches(0.7),
     "Las 12 casillas del hexagrama: 6 en las puntas y 6 en los cruces interiores. "
     "Cada casilla pertenece exactamente a dos lineas rectas.",
     size=11, color=B50, italic=True, align=PP_ALIGN.CENTER, line_spacing=1.15)

# ---- SLIDE 4: El hexagrama magico ----
s = prs.slides.add_slide(BLANK); fondo(s, B00)
header_bar(s, "El Hexagrama Magico", 4); footer_bar(s)
caja(s, Inches(0.5), Inches(1.0), Inches(7.2), Inches(0.5),
     "Definicion:", size=18, color=B80, bold=True)
caja(s, Inches(0.5), Inches(1.55), Inches(7.2), Inches(4.5),
     bullet_list([
       "Estrella de seis puntas (hexagrama), formada por DOS triangulos equilateros superpuestos.",
       "Es la estrella magica mas pequena que existe: en notacion star polygon es m | p con m = 6 y p = 2.",
       "Consta de 12 casillas y 6 lineas rectas, cada linea con 4 casillas.",
       "Se colocan los numeros 1, 2, ..., 12 sin repetir, uno por casilla.",
       "La suma de los cuatro numeros de cada linea debe ser igual a una constante magica M.",
     ], size=14))
caja(s, Inches(0.5), Inches(5.7), Inches(7.2), Inches(0.5),
     "Constante magica:", size=18, color=B80, bold=True)
caja(s, Inches(0.5), Inches(6.2), Inches(7.2), Inches(0.45),
     [[("M(m) = 4m + 2          ", {'size':16,'color':B70,'bold':True,'font':'Cambria'}),
       ("→  M(6) = 4(6) + 2 = 26", {'size':16,'color':B60,'italic':True,'font':'Cambria'})]])

s.shapes.add_picture(FIG_HEX, Inches(8.0), Inches(1.2),
                     width=Inches(4.8), height=Inches(4.8))
caja(s, Inches(8.0), Inches(6.05), Inches(4.8), Inches(0.4),
     "Figura: Hexagrama con M = 26.", size=11, color=B50, italic=True,
     align=PP_ALIGN.CENTER)

# ---- SLIDE 5: Anatomia / Lineas rectas ----
s = prs.slides.add_slide(BLANK); fondo(s, B00)
header_bar(s, "Anatomia del Hexagrama: las 6 Lineas Rectas", 5); footer_bar(s)
caja(s, Inches(0.5), Inches(1.0), Inches(8.0), Inches(0.5),
     "Cada linea recta es un subconjunto de 4 casillas (de las 12 totales):",
     size=14, color=B70)
lineas_def = [
    ("l₁", "{ 1, 3, 6, 8 }",   "Triangulo superior - lado izquierdo"),
    ("l₂", "{ 1, 4, 7, 11 }",  "Triangulo superior - lado derecho"),
    ("l₃", "{ 8, 9, 10, 11 }", "Triangulo superior - base"),
    ("l₄", "{ 2, 3, 4, 5 }",   "Triangulo inferior - base superior"),
    ("l₅", "{ 2, 6, 9, 12 }",  "Triangulo inferior - lado izquierdo"),
    ("l₆", "{ 5, 7, 10, 12 }", "Triangulo inferior - lado derecho"),
]
y = Inches(1.6)
for nom, conj, desc in lineas_def:
    add_rect(s, Inches(0.5), y, Inches(7.6), Inches(0.55),
             fill=B05, line=B20, line_w=0.5,
             shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    caja(s, Inches(0.7), y, Inches(0.8), Inches(0.55),
         nom, size=18, color=B70, bold=True, italic=True,
         font='Cambria', anchor=MSO_ANCHOR.MIDDLE)
    caja(s, Inches(1.5), y, Inches(2.2), Inches(0.55),
         conj, size=13, color=B80, bold=True, font='Consolas',
         anchor=MSO_ANCHOR.MIDDLE)
    caja(s, Inches(3.8), y, Inches(4.2), Inches(0.55),
         desc, size=11, color=B60, italic=True, anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(0.62)

s.shapes.add_picture(FIG_HEX, Inches(8.4), Inches(1.4),
                     width=Inches(4.4), height=Inches(4.4))
caja(s, Inches(8.4), Inches(5.85), Inches(4.4), Inches(0.4),
     "Numeracion de casillas del proyecto", size=11, color=B50, italic=True,
     align=PP_ALIGN.CENTER)

caja(s, Inches(0.5), Inches(5.7), Inches(7.6), Inches(1.2),
     [[("Observacion: ", {'size':12,'bold':True,'color':B70}),
       ("la casilla central no existe en el hexagrama; las casillas 6 y 7 son los cruces interiores. "
        "Cada casilla pertenece exactamente a dos lineas rectas.",
        {'size':12,'color':INK,'italic':True})]],
     line_spacing=1.25)

# ---- SLIDE 6: Por que es interesante ----
s = prs.slides.add_slide(BLANK); fondo(s, B00)
header_bar(s, "Por que es un Problema SAT", 6); footer_bar(s)
caja(s, Inches(0.5), Inches(1.0), Inches(12.3), Inches(0.5),
     "Un problema combinatorio chico en numeros pero denso en restricciones:",
     size=14, color=B70)
# 3 tarjetas
datos = [
    ("80",          "configuraciones esencialmente distintas",
     "Aunque parece un puzzle simple, existen exactamente 80 hexagramas magicos distintos modulo simetrias."),
    ("12!",         "ordenes posibles sin restricciones",
     "12! = 479,001,600 maneras de colocar 12 numeros. Solo una fraccion infima cumple las 4 restricciones."),
    ("240",         "variables proposicionales en nuestro modelo",
     "Con un descriptor binario D_{n,c} y dominios extendidos cubrimos toda la combinatoria."),
]
xs = [Inches(0.5), Inches(4.85), Inches(9.2)]
for (big, sub, txt), x in zip(datos, xs):
    add_rect(s, x, Inches(1.7), Inches(4.0), Inches(4.5),
             fill=B05, line=B30, line_w=0.7,
             shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    caja(s, x, Inches(1.9), Inches(4.0), Inches(1.4),
         big, size=66, color=B70, bold=True,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    caja(s, x, Inches(3.4), Inches(4.0), Inches(0.5),
         sub, size=12, color=B50, italic=True, align=PP_ALIGN.CENTER)
    caja(s, x + Inches(0.2), Inches(4.0), Inches(3.6), Inches(2.0),
         txt, size=12, color=INK, align=PP_ALIGN.CENTER)

caja(s, Inches(0.5), Inches(6.4), Inches(12.3), Inches(0.5),
     "Objetivo: codificar las restricciones como formula proposicional y probar satisfacibilidad con cinco SAT-solvers.",
     size=13, color=B70, italic=True, align=PP_ALIGN.CENTER)


# =============================================================
# SECCION 2 - SISTEMA DE REPRESENTACION
# =============================================================
slide_seccion(2, 9, "Sistema de Representacion", 7,
              "Un unico descriptor binario y la codificacion de\ncada par (numero, casilla) como una letra proposicional.")

# ---- SLIDE 8: Predicado ----
s = prs.slides.add_slide(BLANK); fondo(s, B00)
header_bar(s, "Variables Proposicionales", 8); footer_bar(s)

caja(s, Inches(0.5), Inches(1.0), Inches(12.3), Inches(0.5),
     "Predicado:", size=18, color=B80, bold=True)
caja(s, Inches(0.5), Inches(1.55), Inches(12.3), Inches(0.6),
     [[("D",  {'size':28,'bold':True,'color':B70}),
       ("n,c",{'size':22,'bold':True,'color':B70,'italic':True}),
       ("   :   ", {'size':22,'color':INK}),
       ('"El numero ', {'size':18,'color':INK,'italic':True}),
       ("n",  {'size':18,'italic':True,'bold':True,'color':B60}),
       (" se encuentra en la casilla ", {'size':18,'color':INK,'italic':True}),
       ("c",  {'size':18,'italic':True,'bold':True,'color':B60}),
       ('"',   {'size':18,'color':INK,'italic':True})]])

# columnas con conjuntos / cardinalidad / operadores
y = Inches(2.9)
caja(s, Inches(0.5), y, Inches(4.0), Inches(0.4),
     "Conjuntos:", size=16, color=B80, bold=True)
caja(s, Inches(0.5), y + Inches(0.45), Inches(4.0), Inches(2.5),
     bullet_list([
       "N = { 1, 2, ..., 20 }  (numeros)",
       "C = { 1, 2, ..., 12 }  (casillas)",
       "Lineas = { l₁, ..., l₆ }  (6 lineas rectas)",
     ], size=13))

caja(s, Inches(4.8), y, Inches(4.0), Inches(0.4),
     "Cardinalidad:", size=16, color=B80, bold=True)
add_rect(s, Inches(4.8), y + Inches(0.5), Inches(4.0), Inches(1.6),
         fill=B05, line=B30, line_w=0.6, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
caja(s, Inches(4.8), y + Inches(0.55), Inches(4.0), Inches(0.5),
     "|N|  ·  |C|  =  20 · 12", size=15, color=B70, bold=True,
     align=PP_ALIGN.CENTER, font='Cambria', anchor=MSO_ANCHOR.MIDDLE)
caja(s, Inches(4.8), y + Inches(1.0), Inches(4.0), Inches(1.0),
     "240 atomos", size=34, color=B80, bold=True,
     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

caja(s, Inches(9.1), y, Inches(3.8), Inches(0.4),
     "Operadores:", size=16, color=B80, bold=True)
caja(s, Inches(9.1), y + Inches(0.45), Inches(3.8), Inches(2.5),
     bullet_list([
       "Y    (conjuncion,  ∧)",
       "O    (disyuncion,  ∨)",
       "-    (negacion,    ¬)",
       ">    (implicacion, →)",
       "=    (equivalencia,↔)",
     ], size=13))

# observacion
add_rect(s, Inches(0.5), Inches(5.85), Inches(12.3), Inches(1.0),
         fill=B10, line=B40, line_w=0.6, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
caja(s, Inches(0.7), Inches(5.92), Inches(11.9), Inches(0.9),
     [[("Codificacion de letras:  ", {'size':12,'bold':True,'color':B70}),
       ("la clase ", {'size':12,'color':INK}),
       ("Descriptor", {'size':12,'color':INK,'font':'Consolas','bold':True}),
       (" en ", {'size':12,'color':INK}),
       ("Logica.py", {'size':12,'color':INK,'font':'Consolas','bold':True}),
       (" mapea cada par (n,c) a un caracter unico usando ", {'size':12,'color':INK}),
       ("chr(256 + n*|C| + c)", {'size':12,'color':INK,'font':'Consolas','bold':True}),
       (". Asi, una sola letra (1 caracter Unicode) representa un atomo proposicional.",
        {'size':12,'color':INK})]],
     line_spacing=1.3)

# ---- SLIDE 9: Por que n hasta 20 ----
s = prs.slides.add_slide(BLANK); fondo(s, B00)
header_bar(s, "Cardinalidad: por que n llega hasta 20?", 9); footer_bar(s)

caja(s, Inches(0.5), Inches(1.0), Inches(12.3), Inches(0.6),
     "Una sutileza importante del modelo:", size=18, color=B80, bold=True)

caja_titulada(s, Inches(0.5), Inches(1.8), Inches(12.3), Inches(1.5),
              "Pregunta clave",
              "Si solo usamos numeros del 1 al 12, por que el dominio de n llega hasta 20?",
              header_color=B70, body_color=B05)

caja(s, Inches(0.5), Inches(3.6), Inches(12.3), Inches(0.5),
     "Razon:", size=16, color=B80, bold=True)
caja(s, Inches(0.5), Inches(4.1), Inches(12.3), Inches(2.2),
     bullet_list([
       "La regla 1 enumera combinaciones de 4 numeros distintos cuya SUMA sea 26.",
       "La maxima suma alcanzable con 4 numeros distintos cuyos valores son lo mas grandes posibles es 20 + 3 + 2 + 1 = 26.",
       "Si truncaramos a {1..12}, perderiamos combinaciones como (20, 3, 2, 1) y solo obtendriamos parte de las 80 configuraciones validas.",
       "Trabajar con n in {1..20} garantiza generar TODAS las combinaciones validas (luego la solucion del solver solo asigna numeros 1..12 a casillas, sin contradiccion).",
     ], size=13))

# ---- SLIDE 10: Ytoria / Otoria balanceadas ----
s = prs.slides.add_slide(BLANK); fondo(s, B00)
header_bar(s, "Conectivos Iterados: Ytoria y Otoria Balanceadas", 10); footer_bar(s)

caja(s, Inches(0.5), Inches(1.0), Inches(12.3), Inches(0.5),
     "Construyendo formulas grandes sin que el arbol explote:",
     size=14, color=B70)

caja_titulada(s, Inches(0.5), Inches(1.7), Inches(6.0), Inches(2.6),
              "Ytoria_balanceada",
              [
                "Reemplaza una conjuncion iterada (A₁ Y A₂ Y ... Y Aₙ) por un arbol BINARIO BALANCEADO mediante divide-y-venceras.",
                "",
                "Beneficio: la profundidad pasa de n a log₂(n), lo cual es CRITICO para tableaux (que descomponen por la raiz) y para el parser.",
              ], body_size=11)

caja_titulada(s, Inches(6.85), Inches(1.7), Inches(6.0), Inches(2.6),
              "Otoria_balanceada",
              [
                "Analoga para la disyuncion iterada (A₁ O A₂ O ... O Aₙ).",
                "",
                "En la regla 1, la disyuncion enumera TODAS las permutaciones validas por linea: sin balanceo el arbol seria una cadena lineal de miles de O encadenadas.",
              ], body_size=11)

# codigo
bloque_codigo(s, Inches(0.5), Inches(4.5), Inches(12.3), Inches(2.5),
              titulo="Hexagrama_arr.py",
              lineas=[
                  [("def ", {'color':RGBColor(0xC6,0x78,0xDD)}),
                   ("Ytoria_balanceada", {'color':RGBColor(0x61,0xAF,0xEF),'bold':True}),
                   ("(lista):", {'color':RGBColor(0xE6,0xED,0xF8)})],
                  "    n = len(lista)",
                  [("    if ", {'color':RGBColor(0xC6,0x78,0xDD)}),
                   ("n == 0: ", {'color':RGBColor(0xE6,0xED,0xF8)}),
                   ("return ", {'color':RGBColor(0xC6,0x78,0xDD)}),
                   ("''", {'color':RGBColor(0x98,0xC3,0x79)})],
                  [("    if ", {'color':RGBColor(0xC6,0x78,0xDD)}),
                   ("n == 1: ", {'color':RGBColor(0xE6,0xED,0xF8)}),
                   ("return ", {'color':RGBColor(0xC6,0x78,0xDD)}),
                   ("lista[0]", {'color':RGBColor(0xE6,0xED,0xF8)})],
                  "    mid = n // 2",
                  [("    return ", {'color':RGBColor(0xC6,0x78,0xDD)}),
                   ('"("', {'color':RGBColor(0x98,0xC3,0x79)}),
                   (" + Ytoria_balanceada(lista[:mid])", {'color':RGBColor(0xE6,0xED,0xF8)}),
                   (' + "Y"', {'color':RGBColor(0x98,0xC3,0x79)}),
                   (" + Ytoria_balanceada(lista[mid:])", {'color':RGBColor(0xE6,0xED,0xF8)}),
                   (' + ")"', {'color':RGBColor(0x98,0xC3,0x79)})],
              ])


# =============================================================
# SECCION 3 - REGLAS DEL PROBLEMA
# =============================================================
slide_seccion(3, 9, "Reglas del Problema", 11,
              "Cuatro restricciones que, juntas, caracterizan\nexactamente a los hexagramas magicos validos.")

# ---- Generador generico de slide-regla ----
def slide_regla(num, nombre, natural, formula_math, descripcion, pag):
    s = prs.slides.add_slide(BLANK); fondo(s, B00)
    header_bar(s, f"Regla {num}: {nombre}", pag); footer_bar(s)

    caja_titulada(s, Inches(0.5), Inches(1.1), Inches(12.3), Inches(0.95),
                  "Lenguaje Natural", natural,
                  header_color=B70, body_color=B10, body_size=13)

    caja_titulada(s, Inches(0.5), Inches(2.3), Inches(12.3), Inches(2.4),
                  "Formalizacion Matematica", formula_math,
                  header_color=B70, body_color=B05, body_size=14,
                  body_font='Cambria')

    caja_titulada(s, Inches(0.5), Inches(4.95), Inches(12.3), Inches(1.95),
                  "Descripcion", descripcion,
                  header_color=B70, body_color=B10, body_size=12.5)
    return s

slide_regla(
    1, "Suma de cada Linea Recta = 26",
    "La suma de los cuatro numeros que ocupan cualquier linea recta del hexagrama debe ser exactamente 26.",
    [
      "",
      "    ⋀  l ∈ Lineas      ⋁  (n₁,n₂,n₃,n₄) ∈ Combs(l)    ( Dₙ₁,l[1]  Y  Dₙ₂,l[2]  Y  Dₙ₃,l[3]  Y  Dₙ₄,l[4] )",
      "",
      "donde  Combs(l) = { permutaciones de 4 numeros distintos cuya suma = 26 }",
    ],
    "Para cada linea l existe alguna asignacion de 4 numeros distintos cuya suma es 26 y que ocupan exactamente las 4 casillas de l. Es la regla mas pesada: combina seleccion de combinaciones (subset-sum) con todas las permutaciones validas.",
    12
)

slide_regla(
    2, "Completitud de Casillas",
    "Ninguna casilla del hexagrama puede quedar vacia.",
    [
      "",
      "                          ⋀  c ∈ Casillas     ⋁  n ∈ N    Dₙ,c",
      "",
      "Para toda casilla c, existe al menos un numero n tal que n esta en c.",
    ],
    "Garantiza que cada una de las 12 casillas tenga al menos un numero asignado. Es la regla mas estructurada y suele resolverse en milisegundos por cualquier solver.",
    13
)

slide_regla(
    3, "Unicidad Global del Numero",
    "Si un numero esta en una casilla, no puede estar en ninguna otra (no hay numeros repetidos).",
    [
      "",
      "        ⋀  n ∈ N      ⋀  c ∈ Casillas    ( Dₙ,c  →  ¬  ⋁  e ≠ c    Dₙ,e )",
      "",
      "Si n esta en c, entonces n NO esta en ninguna otra casilla e ≠ c.",
    ],
    "Implementa exclusion mutua a nivel de numero. Genera del orden de |N|*|C|*(|C|-1) implicaciones, lo que se traduce en miles de clausulas tras Tseitin.",
    14
)

slide_regla(
    4, "A lo sumo un Numero por Casilla",
    "Cada casilla contiene a lo sumo un numero (no se pueden poner dos numeros distintos en la misma posicion).",
    [
      "",
      "        ⋀  c ∈ Casillas   ⋀  n,m ∈ N, n ≠ m    ( Dₙ,c  →  ¬  Dₘ,c )",
      "",
      "Si n esta en c, entonces ningun otro numero m puede estar tambien en c.",
    ],
    "Implementa exclusion mutua a nivel de casilla. Es cuadratica en |N|: con |N|=20 y |C|=12 genera 12 · 20 · 19 = 4,560 implicaciones binarias. Es la regla que mas castiga a la fuerza bruta.",
    15
)


# =============================================================
# SECCION 4 - ARQUITECTURA / IMPLEMENTACION
# =============================================================
slide_seccion(4, 9, "Arquitectura e Implementacion Computacional", 16,
              "Dos modulos, una clase central y un pipeline\nde 6 pasos para llevar una regla a un modelo dibujado.")

# ---- SLIDE 17: Arquitectura general ----
s = prs.slides.add_slide(BLANK); fondo(s, B00)
header_bar(s, "Arquitectura General del Proyecto", 17); footer_bar(s)

caja(s, Inches(0.5), Inches(1.0), Inches(6.0), Inches(0.5),
     "Modulos:", size=18, color=B80, bold=True)

mods = [
    ("Logica.py",
     "Clases Formula, Letra, Negacion, Binario y Descriptor (chr/ord). Transformaciones a FNC: eliminar_imp, DeMorgan, distribuir_o_en_y, fnc(), tseitin(). Los CINCO solvers viven aqui: SATtabla, tableaux (primero_anchura / primero_profundidad / backtracking), dpll (con unit_propagate), walkSAT (clase WalkSatEstado) y MiniSAT (pycosat + Minisat22). Funcion filtro() para quitar variables de Tseitin."),
    ("Hexagrama_arr.py",
     "Clase Numero(N=12, C=12). Implementa regla1..regla4 devolviendo strings inorder. Define Ytoria_balanceada y Otoria_balanceada (divide-y-venceras). Metodo visualizar(I) que pinta el hexagrama con matplotlib."),
    ("Proyecto_*.ipynb",
     "Un notebook por solver: Reglas, SATTabla, Tableaux, DPLL, WalkSAT, MiniSAT. Cada uno construye n = Numero(), evalua cada regla por separado y luego la conjuncion total."),
]
y = Inches(1.5)
for nom, desc in mods:
    add_rect(s, Inches(0.5), y, Inches(6.2), Inches(1.65),
             fill=B05, line=B30, line_w=0.6, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    caja(s, Inches(0.7), y + Inches(0.08), Inches(5.8), Inches(0.4),
         nom, size=13, color=B70, bold=True, font='Consolas')
    caja(s, Inches(0.7), y + Inches(0.45), Inches(5.8), Inches(1.2),
         desc, size=10.5, color=INK, line_spacing=1.2)
    y += Inches(1.8)

# pipeline derecha
caja(s, Inches(7.0), Inches(1.0), Inches(5.8), Inches(0.5),
     "Pipeline de una regla:", size=18, color=B80, bold=True)
pasos = [
    ("regla_i()",       "Construye string inorder con Y/Otoria_balanceada"),
    ("inorder_to_tree", "Parsea el string a un arbol Formula"),
    ("tseitin(A)",      "Transforma a FNC polinomial (variables fresh)"),
    ("Solver(S)",       "SATtabla / Tableaux / DPLL / WalkSAT / MiniSAT22"),
    ("filtro(I, A)",    "Elimina variables auxiliares de Tseitin"),
    ("n.visualizar(I)", "Dibuja el hexagrama con la interpretacion"),
]
y = Inches(1.55)
for i, (code, desc) in enumerate(pasos, start=1):
    add_rect(s, Inches(7.0), y, Inches(0.5), Inches(0.5),
             fill=B70, shape=MSO_SHAPE.OVAL)
    caja(s, Inches(7.0), y, Inches(0.5), Inches(0.5),
         str(i), size=13, color=WHITE, bold=True,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    caja(s, Inches(7.7), y - Inches(0.02), Inches(5.1), Inches(0.32),
         code, size=12, color=B70, bold=True, font='Consolas')
    caja(s, Inches(7.7), y + Inches(0.3), Inches(5.1), Inches(0.4),
         desc, size=10, color=INK)
    y += Inches(0.7)

# ---- SLIDE 18: Clase Numero ----
s = prs.slides.add_slide(BLANK); fondo(s, B00)
header_bar(s, "La Clase Numero", 18); footer_bar(s)
caja(s, Inches(0.5), Inches(1.0), Inches(12.3), Inches(0.5),
     "El corazon del modelado:",
     size=14, color=B70)

bloque_codigo(s, Inches(0.5), Inches(1.5), Inches(7.5), Inches(5.4),
              titulo="Hexagrama_arr.py - class Numero",
              lineas=[
                  [("class ", {'color':RGBColor(0xC6,0x78,0xDD)}),
                   ("Numero", {'color':RGBColor(0xE5,0xC0,0x7B),'bold':True}),
                   (":", {'color':RGBColor(0xE6,0xED,0xF8)})],
                  "",
                  [("    def ", {'color':RGBColor(0xC6,0x78,0xDD)}),
                   ("__init__", {'color':RGBColor(0x61,0xAF,0xEF)}),
                   ("(self, N=12, C=12):", {'color':RGBColor(0xE6,0xED,0xF8)})],
                  "        self.N = N",
                  "        self.C = C",
                  [("        self.NenC = ", {'color':RGBColor(0xE6,0xED,0xF8)}),
                   ("Descriptor", {'color':RGBColor(0xE5,0xC0,0x7B)}),
                   ("([N, C])", {'color':RGBColor(0xE6,0xED,0xF8)})],
                  "        self.NenC.escribir = MethodType(",
                  "            escribir_numero, self.NenC)",
                  "        r1 = self.regla1()",
                  "        r2 = self.regla2()",
                  "        r3 = self.regla3()",
                  "        r4 = self.regla4()",
                  "        self.reglas = [r1, r2, r3, r4]",
              ])

# panel derecho
caja(s, Inches(8.3), Inches(1.5), Inches(4.5), Inches(0.4),
     "Atributos clave:", size=13, color=B80, bold=True)
caja(s, Inches(8.3), Inches(1.9), Inches(4.5), Inches(2.5),
     bullet_list([
       "N = 12: cuantos numeros (1..12 visibles)",
       "C = 12: cuantas casillas en el hexagrama",
       "NenC: descriptor binario (numero, casilla)",
       "reglas: lista [r1, r2, r3, r4] en inorder",
     ], size=11))

caja(s, Inches(8.3), Inches(4.5), Inches(4.5), Inches(0.4),
     "Por que aqui?", size=13, color=B80, bold=True)
caja(s, Inches(8.3), Inches(4.9), Inches(4.5), Inches(2.0),
     "Encapsular el problema permite que cada SAT solver simplemente reciba el atributo n.reglas y trabaje sobre el. La separacion Logica.py / Hexagrama_arr.py mantiene el problema independiente del motor.",
     size=11, color=INK, line_spacing=1.3)

# ---- SLIDE 19: implementacion regla 1 ----
def slide_codigo_regla(pag, titulo_slide, comentario_top, lineas_codigo, comentario_bottom):
    s = prs.slides.add_slide(BLANK); fondo(s, B00)
    header_bar(s, titulo_slide, pag); footer_bar(s)
    caja(s, Inches(0.5), Inches(1.0), Inches(12.3), Inches(0.5),
         comentario_top, size=13, color=B70)
    bloque_codigo(s, Inches(0.5), Inches(1.5), Inches(12.3), Inches(4.6),
                  titulo="Hexagrama_arr.py",
                  lineas=lineas_codigo)
    caja(s, Inches(0.5), Inches(6.25), Inches(12.3), Inches(0.85),
         comentario_bottom, size=11, color=B60, italic=True, line_spacing=1.3)
    return s

slide_codigo_regla(
    19, "Implementacion: Regla 1 (suma = 26)",
    "Enumera combinaciones validas de 4 numeros que sumen 26 y todas sus permutaciones sobre cada linea.",
    [
        "def regla1(self):",
        "    val_numeros = np.arange(self.N)",
        "    # 1) combinaciones de 4 numeros distintos cuya suma sea 26",
        "    comb_validas = np.array([c for c in combinations(val_numeros, 4)",
        "                             if sum(x + 1 for x in c) == 26])",
        "",
        "    # 2) las 6 lineas rectas (subconjuntos de casillas)",
        "    lineas = np.array([[0,2,5,7], [0,3,6,10], [7,8,9,10],",
        "                       [1,2,3,4], [1,5,8,11], [4,6,9,11]])",
        "",
        "    formulas_lineas = []",
        "    for linea in lineas:",
        "        opciones_linea = []",
        "        for comb in comb_validas:",
        "            for perm in permutations(comb):  # 4! = 24 ordenes",
        "                c0 = self.NenC.ravel([perm[0], linea[0]])",
        "                c1 = self.NenC.ravel([perm[1], linea[1]])",
        "                c2 = self.NenC.ravel([perm[2], linea[2]])",
        "                c3 = self.NenC.ravel([perm[3], linea[3]])",
        "                opciones_linea.append(Ytoria_balanceada([c0,c1,c2,c3]))",
        "        formulas_lineas.append(Otoria_balanceada(opciones_linea))",
        "    return Ytoria_balanceada(formulas_lineas)",
    ],
    "Para cada una de las 6 lineas se generan miles de cuadruplas validas; la disyuncion balanceada agrupa todas las opciones validas y la conjuncion global pide que todas las lineas sean satisfechas."
)

slide_codigo_regla(
    20, "Implementacion: Regla 2 (completitud)",
    "Cada casilla c debe contener al menos un numero n.",
    [
        "def regla2(self):",
        "    casillas = np.arange(self.C)",
        "    numeros  = np.arange(self.N)",
        "    lista = []",
        "    for c in casillas:",
        "        lista_o = []",
        "        for n in numeros:",
        "            lista_o.append(self.NenC.ravel([n, c]))",
        "        lista.append(Otoria_balanceada(lista_o))",
        "    return Ytoria_balanceada(lista)",
    ],
    "Una Otoria por casilla (existe algun numero) envuelta en una Ytoria global (para todas las casillas)."
)

slide_codigo_regla(
    21, "Implementacion: Regla 3 (unicidad global)",
    "Si el numero n esta en c, no puede estar en otra casilla.",
    [
        "def regla3(self):",
        "    num_casillas = np.array([(n, c)",
        "                             for n in range(self.N)",
        "                             for c in range(self.C)])",
        "    lista = []",
        "    for m in num_casillas:",
        "        n, c = m",
        "        otras_casillas = np.array([c1 for c1 in range(self.C)",
        "                                   if c1 != c])",
        "        lista_o = []",
        "        for k in otras_casillas:",
        "            lista_o.append(self.NenC.ravel([n, k]))",
        "        form = '(' + self.NenC.ravel([*m]) + '>-' + \\",
        "               Otoria_balanceada(lista_o) + ')'",
        "        lista.append(form)",
        "    return Ytoria_balanceada(lista)",
    ],
    "Implementa la implicacion  D_{n,c} -> NOT (OR_{e != c} D_{n,e})  para cada par (n, c)."
)

slide_codigo_regla(
    22, "Implementacion: Regla 4 (a lo sumo uno)",
    "Para cada casilla c, no pueden coexistir dos numeros distintos n y m.",
    [
        "def regla4(self):",
        "    formulas = []",
        "    for c in range(self.C):",
        "        for n in range(self.N):",
        "            for m in range(self.N):",
        "                if n != m:",
        "                    formulas.append(",
        "                        f'({self.NenC.ravel([n, c])}'",
        "                        f'>-{self.NenC.ravel([m, c])})')",
        "    return Ytoria_balanceada(formulas)",
    ],
    "Genera C * N * (N-1) implicaciones binarias. Para N=20 y C=12 son 4,560 implicaciones. Es la responsable del peor caso de SATtabla (11 horas)."
)

# ---- SLIDE 23: visualizar ----
s = prs.slides.add_slide(BLANK); fondo(s, B00)
header_bar(s, "Metodo visualizar(): de la Interpretacion al Dibujo", 23); footer_bar(s)
caja(s, Inches(0.5), Inches(1.0), Inches(12.3), Inches(0.5),
     "Traduce un diccionario booleano {letra: True/False} en el hexagrama dibujado.",
     size=13, color=B70)

caja(s, Inches(0.5), Inches(1.6), Inches(7.0), Inches(0.4),
     "Proposito:", size=14, color=B80, bold=True)
caja(s, Inches(0.5), Inches(2.0), Inches(7.0), Inches(0.7),
     "Convertir la interpretacion boolena I devuelta por el solver en un grafico interpretable.",
     size=12, color=INK, line_spacing=1.25)

caja(s, Inches(0.5), Inches(2.85), Inches(7.0), Inches(0.4),
     "Proceso:", size=14, color=B80, bold=True)
caja(s, Inches(0.5), Inches(3.25), Inches(7.0), Inches(3.0),
     bullet_list([
       "Construye los dos triangulos con matplotlib.patches.Polygon.",
       "Mantiene un diccionario casilla_a_numeros (permite varios numeros por casilla, util para depurar).",
       "Recorre I; para cada literal verdadero (sin '-') decodifica (n, c) con NenC.unravel.",
       "Dibuja en la posicion correcta usando una tabla de coordenadas (centro de cada casilla).",
       "Si una casilla tiene 2+ numeros, reduce el tamano de fuente automaticamente.",
     ], size=11))

s.shapes.add_picture(FIG_HEX_S, Inches(8.0), Inches(1.5),
                     width=Inches(4.8), height=Inches(4.8))
caja(s, Inches(8.0), Inches(6.3), Inches(4.8), Inches(0.4),
     "Salida del visualizador para una solucion valida.",
     size=11, color=B50, italic=True, align=PP_ALIGN.CENTER)


# =============================================================
# SECCION 5 - METODOS SAT SOLVER
# =============================================================
slide_seccion(5, 9, "Metodos SAT Solver", 24,
              "Cinco enfoques distintos para responder la misma pregunta:\nexiste alguna interpretacion que satisfaga la formula?")

# ---- SLIDE 25: Analisis comparativo intro ----
s = prs.slides.add_slide(BLANK); fondo(s, B00)
header_bar(s, "Analisis Comparativo con Metodos SAT Solver", 25); footer_bar(s)

caja(s, Inches(0.5), Inches(1.0), Inches(12.3), Inches(0.7),
     [[("La seleccion de metodos SAT responde a una intencion ", {'size':13,'color':INK}),
       ("pedagogica y experimental ", {'size':13,'color':B70,'bold':True}),
       ("para evaluar cada regla del hexagrama magico:", {'size':13,'color':INK})]])

solvers = [
    ("1. SATtabla",            "Tabla de verdad - base conceptual exhaustiva (Logica.py).",                 B30),
    ("2. SATtableaux",         "Descomposicion en arbol - 3 estrategias: anchura, profundidad, backtracking.", B40),
    ("3. DPLL",                "Davis-Putnam-Logemann-Loveland - propagacion unitaria + backtracking.",     B50),
    ("4. WalkSAT",             "Busqueda local estocastica - flips probabilisticos sobre asignacion completa.", B60),
    ("5. MiniSAT22 (CDCL)",    "Estado del arte - aprendizaje de clausulas y backjumping no-cronologico.",  B70),
]
y = Inches(1.85)
for nom, desc, col in solvers:
    add_rect(s, Inches(0.5), y, Inches(0.5), Inches(0.5),
             fill=col, shape=MSO_SHAPE.OVAL)
    caja(s, Inches(0.5), y, Inches(0.5), Inches(0.5),
         nom[0], size=14, color=WHITE, bold=True,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    caja(s, Inches(1.2), y, Inches(11.5), Inches(0.5),
         [[(nom + "  ", {'size':14,'bold':True,'color':B80}),
           (desc,       {'size':13,'color':INK,'italic':True})]],
         anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(0.7)

caja_titulada(s, Inches(0.5), Inches(6.0), Inches(12.3), Inches(1.05),
              "Objetivo",
              "Validar la formalizacion del hexagrama y comprender ventajas y limitaciones de cada estrategia, aplicando los cinco SAT solvers a cada regla por separado y a la conjuncion total.",
              header_color=B70, body_color=B05, body_size=12)

# ---- SLIDE: Implementacion de los SAT-solvers en Logica.py ----
s = prs.slides.add_slide(BLANK); fondo(s, B00)
header_bar(s, "Implementacion de los SAT-Solvers en Logica.py", 0); footer_bar(s)
caja(s, Inches(0.5), Inches(0.95), Inches(12.3), Inches(0.5),
     "Las cinco estrategias se implementaron en el modulo. Tres piezas clave: filtrado de Tseitin, DPLL con propagacion unitaria y MiniSAT via PySAT.",
     size=12.5, color=B70)

bloque_codigo(s, Inches(0.5), Inches(1.55), Inches(6.15), Inches(5.3),
              titulo="filtro()  +  dpll()",
              lineas=[
                  "def filtro(I, formula_original):",
                  "    if I is None or I == {}:",
                  "        return I",
                  "    reales = set(inorder_to_tree(",
                  "        formula_original).letras())",
                  "    return {v: val for v, val in I.items()",
                  "            if v in reales}",
                  "",
                  "def dpll(F, S, I):",
                  "    S, I, conf = unit_propagate(S, I)",
                  "    if conf: return 'Insatisfacible', {}",
                  "    if len(S) == 0: return 'Satisfacible', I",
                  "    if any(len(c)==0 for c in S):",
                  "        return 'Insatisfacible', {}",
                  "    S = sorted(S, key=len)   # clausula corta",
                  "    l = S[0][0]; lc = complemento_dpll(l)",
                  "    r, I2 = dpll(F, eliminar_literal(S, l),",
                  "                 extender_I(deepcopy(I), l))",
                  "    if r == 'Satisfacible':",
                  "        return r, filtro(I2, F)",
                  "    return dpll(F, eliminar_literal(S, lc),",
                  "                extender_I(deepcopy(I), lc))",
              ])

bloque_codigo(s, Inches(6.85), Inches(1.55), Inches(5.95), Inches(5.3),
              titulo="MiniSAT()  (pycosat + Minisat22)",
              lineas=[
                  "from pysat.solvers import Minisat22",
                  "import pycosat",
                  "",
                  "def MiniSAT(A):",
                  "    def lit_numero(l):",
                  "        return (-(ord(l[1:]) - 255)",
                  "                if '-' in l",
                  "                else ord(l) - 255)",
                  "    # letra -> entero (codificacion DIMACS)",
                  "    S = fnc_numero(tseitin(A))",
                  "    with Minisat22(bootstrap_with=S) as m:",
                  "        if m.solve():",
                  "            I = obtener_int(m.get_model())",
                  "            return 'Satisfacible', filtro(I, A)",
                  "        return 'Insatisfacible', {}",
                  "",
                  "# WalkSAT: clase WalkSatEstado con",
                  "# break_count() y clausulas_sat/unsat;",
                  "# tableaux: primero_anchura,",
                  "# primero_profundidad, backtracking.",
              ])

# ---- generador slide-solver ----
def slide_solver(pag, num, nombre, descripcion, ventajas, desventajas, observacion=None):
    s = prs.slides.add_slide(BLANK); fondo(s, B00)
    header_bar(s, f"{num}. {nombre}", pag); footer_bar(s)

    caja(s, Inches(0.5), Inches(1.0), Inches(12.3), Inches(0.5),
         "Descripcion:", size=16, color=B80, bold=True)
    caja(s, Inches(0.5), Inches(1.45), Inches(12.3), Inches(2.0),
         bullet_list(descripcion, size=13))

    # Ventajas
    add_rect(s, Inches(0.5), Inches(3.8), Inches(6.0), Inches(2.6),
             fill=B05, line=B30, line_w=0.6, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    caja(s, Inches(0.7), Inches(3.9), Inches(5.6), Inches(0.4),
         "Ventajas", size=14, color=B70, bold=True)
    caja(s, Inches(0.7), Inches(4.3), Inches(5.6), Inches(2.0),
         bullet_list(ventajas, size=12))

    # Desventajas
    add_rect(s, Inches(6.85), Inches(3.8), Inches(6.0), Inches(2.6),
             fill=B05, line=B30, line_w=0.6, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    caja(s, Inches(7.05), Inches(3.9), Inches(5.6), Inches(0.4),
         "Desventajas", size=14, color=B70, bold=True)
    caja(s, Inches(7.05), Inches(4.3), Inches(5.6), Inches(2.0),
         bullet_list(desventajas, size=12))

    if observacion:
        add_rect(s, Inches(0.5), Inches(6.5), Inches(12.3), Inches(0.55),
                 fill=B10, line=B40, line_w=0.5,
                 shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        caja(s, Inches(0.7), Inches(6.5), Inches(11.9), Inches(0.55),
             observacion, size=11, color=B70, italic=True,
             anchor=MSO_ANCHOR.MIDDLE)

slide_solver(
    26, "1", "SATtabla (Tablas de Verdad)",
    [
      "Enumeracion exhaustiva de todas las posibles asignaciones (2^n).",
      "Evalua la formula completa para cada combinacion.",
      "Metodo fundamental y conceptualmente simple, implementado en Logica.py.",
    ],
    [
      "Completitud garantizada.",
      "Certeza absoluta (siempre encuentra o descarta).",
      "Ideal para didactica y para corroborar.",
    ],
    [
      "Complejidad O(2^n).",
      "Inviable para problemas grandes.",
      "Sin optimizaciones de poda.",
    ],
    "Para el hexagrama, con 240 atomos, 2^240 ≈ 1.77 x 10^72 asignaciones: completamente impracticable."
)

slide_solver(
    27, "2", "SATtableaux (Tableaux Semanticos)",
    [
      "Construccion de un arbol de descomposicion segun reglas alfa y beta.",
      "Implementadas tres estrategias: primero en anchura, primero en profundidad y backtracking.",
      "Deteccion temprana de contradicciones por literales complementarios en una rama.",
    ],
    [
      "Mas eficiente que tablas en muchos casos.",
      "Poda de ramas contradictorias.",
      "Representacion visual intuitiva.",
      "Completo y correcto.",
    ],
    [
      "Complejidad exponencial en el peor caso.",
      "Muy sensible al orden de expansion.",
      "Consumo significativo de memoria.",
      "Profundidad de recursion enorme.",
    ],
    "En el proyecto fue necesario hacer sys.setrecursionlimit(10,000,000) para que Python no abortara antes de tiempo."
)

slide_solver(
    28, "3", "DPLL (Davis-Putnam-Logemann-Loveland)",
    [
      "Trabaja sobre formula en FNC obtenida via Tseitin.",
      "Busqueda con retroceso (backtracking).",
      "Propagacion de clausulas unitarias (unit propagation).",
      "Base teorica de practicamente todos los solvers modernos.",
    ],
    [
      "Inferencias deterministas.",
      "Reduccion dramatica del espacio.",
      "Completo y correcto.",
      "Muy efectivo en problemas estructurados.",
    ],
    [
      "Retroceso cronologico (sin backjumping).",
      "Sin aprendizaje de conflictos.",
      "Sensible a heuristicas de seleccion.",
      "Mas lento que CDCL en instancias industriales.",
    ],
    "La implementacion del proyecto incluye una heuristica: ordenar las clausulas por longitud y ramificar por el primer literal de la clausula mas corta."
)

slide_solver(
    29, "4", "WalkSAT",
    [
      "Busqueda local estocastica sobre asignaciones COMPLETAS.",
      "En cada paso, escoge una clausula no satisfecha y voltea un literal (greedy o random).",
      "Balance entre exploracion y explotacion (parametro p).",
    ],
    [
      "Extremadamente eficiente en problemas aleatorios.",
      "Memoria constante.",
      "Simple de implementar.",
      "Multiples reinicios posibles.",
    ],
    [
      "Incompleto: no demuestra insatisfacibilidad.",
      "Dependiente de parametros (max_flips, p).",
      "Atrapamiento en optimos locales.",
      "Inconsistente en problemas estructurados.",
    ],
    "Medido: WalkSAT resuelve R2 en 0.84 s, pero en R3 corre 12 h 25 min SIN encontrar solucion y en R4 se interrumpe a las 14 h 43 min. Los optimos locales y las restricciones de unicidad fuerzan flips que destruyen el progreso."
)

slide_solver(
    30, "5", "MiniSAT22 (CDCL - Estado del Arte)",
    [
      "Conflict-Driven Clause Learning: aprende clausulas a partir de cada conflicto.",
      "Backjumping no-cronologico: salta varios niveles de decision a la vez.",
      "Heuristica de seleccion VSIDS (Variable State Independent Decaying Sum).",
      "Implementacion C de referencia usada via libreria python-sat (Minisat22).",
    ],
    [
      "Memoria de conflictos evita repetir errores.",
      "Saltos inteligentes en el espacio de busqueda.",
      "Heuristicas sofisticadas (watched literals, VSIDS).",
      "Maneja millones de variables y clausulas.",
    ],
    [
      "Gestion de memoria mas compleja.",
      "Codigo de implementacion no trivial.",
      "Overhead computacional en problemas chicos.",
      "Configuracion de parametros no obvia.",
    ],
    "Medido: MiniSAT22 resuelve R2, R3 y R4 en milisegundos; el cuello de botella es la Regla 1 (suma=26), que toma 19.1 s. La conjuncion de las 4 reglas se resuelve en 33.1 s."
)

# ---- SLIDE 31: sintesis comparativa ----
s = prs.slides.add_slide(BLANK); fondo(s, B00)
header_bar(s, "Sintesis Comparativa", 31); footer_bar(s)

headers = ["Metodo", "Completitud", "Complejidad", "Aprendizaje", "Aplicabilidad"]
rows = [
    ("SATtabla",          "Si", "O(2^n)",       "No",  "Didactica"),
    ("Tableaux",          "Si", "Exponencial",  "No",  "Problemas pequenos"),
    ("DPLL",              "Si", "Exponencial*", "No",  "Problemas estructurados"),
    ("WalkSAT",           "No", "Polinomial**", "No",  "Instancias satisfacibles"),
    ("MiniSAT22 (CDCL)",  "Si", "Exponencial*", "Si",  "Industrial"),
]
table_x = Inches(0.8); table_y = Inches(1.5)
col_widths = [Inches(3.3), Inches(2.2), Inches(2.5), Inches(2.2), Inches(3.0)]
row_h = Inches(0.5)
x = table_x
for j, h in enumerate(headers):
    add_rect(s, x, table_y, col_widths[j], row_h, fill=B70,
             line=B50, line_w=0.5)
    caja(s, x, table_y, col_widths[j], row_h,
         h, size=13, color=WHITE, bold=True,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    x += col_widths[j]
for i, row in enumerate(rows):
    x = table_x
    y = table_y + row_h * (i + 1)
    bg = B00 if i % 2 == 0 else B05
    for j, val in enumerate(row):
        add_rect(s, x, y, col_widths[j], row_h, fill=bg,
                 line=B20, line_w=0.4)
        bold = (j == 0)
        col = B80 if (j == 0 or val.startswith("Si") or "Industrial" in val) else INK
        caja(s, x, y, col_widths[j], row_h, val, size=12, color=col, bold=bold,
             align=PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER,
             anchor=MSO_ANCHOR.MIDDLE)
        x += col_widths[j]

caja(s, Inches(0.8), Inches(4.6), Inches(12.0), Inches(0.4),
     "Cuadro: *Con poda eficiente, **Sin garantia de terminacion",
     size=10, color=B50, italic=True, align=PP_ALIGN.CENTER)

caja_titulada(s, Inches(0.8), Inches(5.3), Inches(11.7), Inches(1.5),
              "Conclusion",
              "MiniSAT22 emerge como el enfoque mas robusto al combinar busqueda sistematica completa (CDCL) con aprendizaje adaptativo de conflictos. Resuelve la conjuncion en 33 s, hasta 3 ordenes de magnitud mas rapido que los metodos academicos que corren horas sin terminar.",
              header_color=B70, body_color=B05, body_size=13)


# =============================================================
# SECCION 6 - METODOLOGIA Y RESULTADOS
# =============================================================
slide_seccion(6, 9, "Metodologia y Analisis Experimental", 32,
              "Como se corrio el experimento, en que hardware\ny con que protocolos de medicion.")

# ---- SLIDE 33: metodologia ----
s = prs.slides.add_slide(BLANK); fondo(s, B00)
header_bar(s, "Metodologia Experimental", 33); footer_bar(s)

caja(s, Inches(0.5), Inches(1.0), Inches(6.5), Inches(0.5),
     "Protocolo de Evaluacion Incremental:", size=15, color=B80, bold=True)
caja(s, Inches(0.5), Inches(1.5), Inches(6.5), Inches(2.8),
     bullet_list([
       "Evaluar cada regla individualmente (R1, R2, R3, R4).",
       "Evaluar la conjuncion total de las 4 reglas (R1 ∧ R2 ∧ R3 ∧ R4).",
       "Para cada combinacion regla x solver se mide tiempo con %%time de Jupyter.",
       "Si el solver no termina en 24 horas, se marca como Timeout (interrumpido).",
       "Validar el modelo encontrado con verificar_modelo(reglas, I).",
     ], size=12))

caja(s, Inches(0.5), Inches(4.5), Inches(6.5), Inches(0.4),
     "Hardware de Pruebas:", size=14, color=B80, bold=True)
caja(s, Inches(0.5), Inches(4.95), Inches(6.5), Inches(2.0),
     bullet_list([
       "Maquina virtual Oracle VirtualBox.",
       "Sistema base: Windows / Linux (segun integrante).",
       "Python 3.x + Jupyter Notebook.",
       "Librerias: numpy, matplotlib, pycosat, python-sat.",
       "sys.setrecursionlimit(10,000,000) para tableaux y DPLL.",
     ], size=12))

caja_titulada(s, Inches(7.3), Inches(1.0), Inches(5.5), Inches(2.0),
              "Resultado Binario",
              "Cada ejecucion produce uno de dos posibles estados:\n\n   (1) Exito  -  el solver termina y devuelve modelo o UNSAT.\n   (2) Interrupcion (Timeout)  -  pasa el limite de 24h.",
              header_color=B70, body_color=B10, body_size=12)

caja_titulada(s, Inches(7.3), Inches(3.3), Inches(5.5), Inches(3.7),
              "Limite Temporal",
              [
                "Tiempo maximo permitido por ejecucion:",
                "",
                "      24 horas (un dia completo)",
                "",
                "Justificacion: algunas reglas (R3, R4) generan miles de clausulas tras Tseitin. Dar mas tiempo no ayuda: o el solver gana en horas, o no gana en absoluto.",
              ],
              header_color=B70, body_color=B05, body_size=12)

# ---- Slides 34-38: resultados por solver ----
def slide_resultado_solver(pag, num_chip, nombre, caracteristicas,
                           tiempo_resultado, estado_resultado, status_color,
                           ventajas_breve, desventajas_breve, comentario_pie):
    s = prs.slides.add_slide(BLANK); fondo(s, B00)
    header_bar(s, f"{num_chip}. {nombre}", pag); footer_bar(s)

    caja(s, Inches(0.5), Inches(1.0), Inches(7.0), Inches(0.45),
         "Caracteristicas:", size=14, color=B80, bold=True)
    caja(s, Inches(0.5), Inches(1.45), Inches(7.0), Inches(2.0),
         bullet_list(caracteristicas, size=12))

    # caja de resultado
    add_rect(s, Inches(0.5), Inches(3.7), Inches(7.0), Inches(0.4),
             fill=status_color, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    caja(s, Inches(0.5), Inches(3.7), Inches(7.0), Inches(0.4),
         "Resultado", size=12, color=WHITE, bold=True,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_rect(s, Inches(0.5), Inches(4.1), Inches(7.0), Inches(1.6),
             fill=B10, line=B30, line_w=0.5,
             shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    caja(s, Inches(0.7), Inches(4.2), Inches(6.6), Inches(0.5),
         tiempo_resultado, size=20, color=B80, bold=True)
    caja(s, Inches(0.7), Inches(4.7), Inches(6.6), Inches(0.5),
         estado_resultado, size=13, color=B70)

    caja(s, Inches(0.5), Inches(6.0), Inches(7.0), Inches(0.5),
         [[("[ok] ",   {'size':14,'color':B70,'bold':True}),
           (ventajas_breve, {'size':12,'color':INK})]])
    caja(s, Inches(0.5), Inches(6.45), Inches(7.0), Inches(0.5),
         [[("[!]  ",   {'size':14,'color':B40,'bold':True}),
           (desventajas_breve, {'size':12,'color':INK})]])

    # captura/figura derecha
    s.shapes.add_picture(FIG_HEX_S, Inches(8.0), Inches(1.4),
                         width=Inches(4.5), height=Inches(4.5))
    caja(s, Inches(8.0), Inches(5.95), Inches(4.5), Inches(0.4),
         comentario_pie, size=11, color=B50, italic=True, align=PP_ALIGN.CENTER)
    return s

slide_resultado_solver(
    34, "1", "SATtabla - Tablas de Verdad",
    [
      "Enumeracion exhaustiva.",
      "Espacio: 2^240 ≈ 10^72.",
      "Complejidad: O(2^n).",
    ],
    "R1: 116 ms  ·  R4: 11 h 06 min",
    "R1 y R2 resueltas; R4 interrumpida a las 11 h, conjuncion en timeout",
    B50,
    "Simple, completo, ideal para entender el problema.",
    "Inviable para problemas con muchos atomos.",
    "Figura: solucion del hexagrama validada manualmente."
)

slide_resultado_solver(
    35, "2", "SATtableaux - Tableaux Semanticos",
    [
      "Descomposicion en arbol con reglas alfa/beta.",
      "Tres estrategias: anchura, profundidad, backtracking.",
      "Poda de ramas contradictorias.",
    ],
    "Profundidad - todas: 10 h 42 min",
    "Backtracking - todas: 6 h 22 min  ·  R4: 1 min 18 s, R1: 2.4 s",
    B50,
    "Deteccion temprana de conflictos.",
    "Complejidad exponencial persiste.",
    "Truco: fijar una linea (condicion inicial) acelera la busqueda."
)

slide_resultado_solver(
    36, "3", "DPLL - Primer Exito Completo",
    [
      "Propagacion unitaria (unit propagation).",
      "Eliminacion de literales puros (implicita).",
      "Backtracking cronologico con heuristica de clausula corta.",
    ],
    "R1: 2 min 08 s  ·  Conjuncion: 4 min 58 s",
    "Completado en TODAS las reglas (R2: 86 ms, R3: 2.5 s, R4: 9.9 s)",
    B70,
    "Reduce dramaticamente el espacio de busqueda.",
    "Backtracking cronologico sin aprendizaje.",
    "Figura: modelo valido encontrado por DPLL."
)

slide_resultado_solver(
    37, "4", "WalkSAT - Busqueda Estocastica",
    [
      "Busqueda local sobre asignaciones completas.",
      "Movimientos aleatorios y greedy.",
      "Multiples reinicios.",
    ],
    "R3: 12 h 25 min  ·  R4: 14 h 43 min",
    "R2 resuelta en 0.84 s; R3 sin solucion, R4 interrumpida (optimos locales)",
    B40,
    "Excelente en instancias aleatorias.",
    "Incompleto, no garantiza convergencia.",
    "Figura: R2 resuelta; R3 y R4 no convergen."
)

slide_resultado_solver(
    38, "5", "MiniSAT22 - Estado del Arte",
    [
      "Aprendizaje de clausulas (CDCL).",
      "Backjumping no cronologico.",
      "Heuristica VSIDS y watched literals.",
    ],
    "R1: 19.1 s  ·  Conjuncion: 33.1 s",
    "Completado en TODAS las reglas (R2-R4 en milisegundos)",
    B70,
    "Memoria de conflictos evita repeticiones.",
    "El mas eficiente: ordenes de magnitud por debajo de DPLL.",
    "Figura: solucion optima de las 4 reglas en 33 s."
)


# =============================================================
# SECCION 7 - ANALISIS COMPARATIVO DE RESULTADOS
# =============================================================
slide_seccion(7, 9, "Analisis Comparativo de Resultados", 39,
              "Las cifras puestas juntas:\nque solver gana, que solver no termina, y por que.")

# ---- SLIDE 40: tabla comparativa tiempos ----
s = prs.slides.add_slide(BLANK); fondo(s, B00)
header_bar(s, "Tabla Comparativa de Tiempos de Ejecucion", 40); footer_bar(s)

headers = ["SAT Solver", "R1", "R2", "R3", "R4", "Conjuncion (R1..R4)", "Estado global"]
rows = [
    ("SATtabla",              "116 ms",   "0.5 ms",   "timeout",    "11 h 06 min",  "Timeout (>24 h)", "Interrumpido"),
    ("Tableaux - anchura",    "—",        "3 min 12s","—",          "—",            "—",               "Interrumpido"),
    ("Tableaux - profundidad","2.75 s",   "100 ms",   "12.7 s",     "1 min 12 s",   "10 h 42 min",     "Completado"),
    ("Tableaux - backtracking","2.43 s",  "35 ms",    "3.3 s",      "1 min 18 s",   "6 h 22 min",      "Completado"),
    ("DPLL",                  "2 min 08 s","86 ms",   "2.51 s",     "9.95 s",       "4 min 58 s",      "Completado"),
    ("WalkSAT",               "—",        "0.84 s",   "12 h 25 min","14 h 43 min",  "—",               "Parcial"),
    ("MiniSAT22 (CDCL)",      "19.1 s",   "13 ms",    "413 ms",     "1.54 s",       "33.1 s",          "Completado"),
]
table_x = Inches(0.4); table_y = Inches(1.3)
col_widths = [Inches(2.6), Inches(1.3), Inches(1.0), Inches(1.4), Inches(1.5),
              Inches(2.5), Inches(1.6)]
row_h = Inches(0.45)
x = table_x
for j, h in enumerate(headers):
    add_rect(s, x, table_y, col_widths[j], row_h, fill=B70,
             line=B50, line_w=0.5)
    caja(s, x, table_y, col_widths[j], row_h,
         h, size=11, color=WHITE, bold=True,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    x += col_widths[j]
for i, row in enumerate(rows):
    x = table_x; y = table_y + row_h * (i + 1)
    bg = B00 if i % 2 == 0 else B05
    for j, val in enumerate(row):
        add_rect(s, x, y, col_widths[j], row_h, fill=bg,
                 line=B20, line_w=0.4)
        col = INK; bold = (j == 0)
        if j == len(row) - 1:
            if "Completado" in val: col = B70; bold = True
            elif "Interrumpido" in val: col = B50; bold = True
            elif "Parcial" in val: col = B40; bold = True
        elif "Timeout" in val or "h " in val:
            col = B50; bold = True
        elif "ms" in val and j > 0 and "ms" == val.split()[0] if len(val.split()) > 0 else False:
            col = B70; bold = True
        caja(s, x, y, col_widths[j], row_h, val, size=10, color=col, bold=bold,
             align=PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER,
             anchor=MSO_ANCHOR.MIDDLE)
        x += col_widths[j]

caja(s, Inches(0.4), Inches(5.0), Inches(12.5), Inches(0.4),
     "Cuadro: Wall time real medido con %%time de Jupyter sobre cada celda.  '—' = no medido / no termino;  'timeout' = supero el limite de 24 h.",
     size=10, color=B50, italic=True, align=PP_ALIGN.CENTER)

caja_titulada(s, Inches(0.4), Inches(5.6), Inches(12.5), Inches(1.5),
              "Diferencia Critica",
              "Hasta 3 ordenes de magnitud entre los metodos exitosos (DPLL: ~5 min; MiniSAT22: 33 s en la conjuncion) y los interrumpidos por timeout (SATtabla, WalkSAT, que corren horas sin terminar). Dato clave: la Regla 1 (suma=26) es el cuello de botella incluso para los solvers eficientes (DPLL 2 min, MiniSAT 19 s); el resto de reglas se resuelven en milisegundos.",
              header_color=B70, body_color=B05, body_size=12.5)

# ---- SLIDE 41: analisis convergencia ----
s = prs.slides.add_slide(BLANK); fondo(s, B00)
header_bar(s, "Analisis de Convergencia Incremental", 41); footer_bar(s)

caja(s, Inches(0.5), Inches(1.0), Inches(12.3), Inches(0.5),
     "Umbrales de complejidad observados:", size=16, color=B80, bold=True)

datos_umbral = [
    ("SATtabla",         "Resuelve R1/R2 en ms, pero R4 corre 11 h sin terminar; conjuncion en timeout",  B50),
    ("Tableaux",         "Resuelve cada regla, pero la conjuncion total toma 6-10 h (backtracking / profundidad)", B40),
    ("DPLL",             "Exito en todas las reglas y en la conjuncion (~5 min); R1 es la mas costosa (2 min)", B70),
    ("WalkSAT",          "Falla en R3 y R4 individuales: 12-15 h sin solucion (optimos locales)",     B40),
    ("MiniSAT22",        "Exito en todo; conjuncion en 33 s, dominada por R1 (19 s); R2-R4 en ms",     B70),
]
y = Inches(1.7)
for nom, txt, col in datos_umbral:
    add_rect(s, Inches(0.5), y, Inches(0.2), Inches(0.55),
             fill=col)
    caja(s, Inches(0.85), y, Inches(3.2), Inches(0.55),
         nom, size=14, color=B80, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    caja(s, Inches(4.1), y, Inches(8.6), Inches(0.55),
         txt, size=12, color=INK, anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(0.7)

caja_titulada(s, Inches(0.5), Inches(5.5), Inches(12.3), Inches(1.5),
              "Conclusion Experimental",
              "Solo los solucionadores SISTEMATICOS AVANZADOS (DPLL con Tseitin + UP, y MiniSAT22 con CDCL) resuelven el problema completo en hardware estandar dentro del limite de 24 horas. Los demas o se atascan en explosion combinatoria (tabla, tableaux) o en optimos locales (WalkSAT).",
              header_color=B70, body_color=B05, body_size=13)

# ---- SLIDE 42: determinacion satisfacibilidad ----
s = prs.slides.add_slide(BLANK); fondo(s, B00)
header_bar(s, "Determinacion de Satisfacibilidad", 42); footer_bar(s)

caja(s, Inches(0.5), Inches(1.0), Inches(12.3), Inches(0.5),
     "Clasificacion logica de la formula del hexagrama:", size=15, color=B80, bold=True)

opciones = [
    ("Tautologia",        "Verdadera en TODA interpretacion",        B30),
    ("Contradiccion",     "Falsa en TODA interpretacion",            B40),
    ("Contingente",       "Verdadera en al menos UNA interpretacion (satisfacible)", B70),
]
y = Inches(1.7)
for nom, def_, col in opciones:
    add_rect(s, Inches(0.5), y, Inches(12.3), Inches(0.6),
             fill=B05, line=col, line_w=1.2, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    add_rect(s, Inches(0.5), y, Inches(0.15), Inches(0.6), fill=col)
    caja(s, Inches(0.75), y, Inches(3.0), Inches(0.6),
         nom, size=15, color=B80, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    caja(s, Inches(3.8), y, Inches(8.4), Inches(0.6),
         def_, size=12, color=INK, italic=True, anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(0.75)

caja(s, Inches(0.5), Inches(4.2), Inches(12.3), Inches(0.5),
     "Evidencia experimental:", size=14, color=B80, bold=True)
caja(s, Inches(0.5), Inches(4.6), Inches(12.3), Inches(1.4),
     bullet_list([
       "DPLL y MiniSAT22 encontraron MODELOS validos (asignaciones concretas que satisfacen las 4 reglas).",
       "Por lo tanto la formula NO es contradiccion.",
       "Existen tambien interpretaciones que la falsifican (cualquier asignacion aleatoria casi seguro falla).",
       "Por lo tanto la formula NO es tautologia.",
     ], size=12))

caja_titulada(s, Inches(0.5), Inches(6.0), Inches(12.3), Inches(1.1),
              "Resultado Formal",
              "La formula del hexagrama magico es SATISFACIBLE (contingente). Existen exactamente 80 configuraciones esencialmente distintas (modulo rotaciones y reflexiones).",
              header_color=B70, body_color=B05, body_size=13)


# =============================================================
# SECCION 8 - DISCUSION Y CONCLUSIONES
# =============================================================
slide_seccion(8, 9, "Discusion y Conclusiones", 43,
              "Que aprendimos modelando un puzzle de 12 casillas\ny lanzandolo contra cinco solvers distintos.")

# ---- SLIDE 44: conclusiones 1/3 ----
s = prs.slides.add_slide(BLANK); fondo(s, B00)
header_bar(s, "Conclusiones Principales  (1/3)", 44); footer_bar(s)

caja(s, Inches(0.5), Inches(1.0), Inches(12.3), Inches(0.5),
     "1. Formalizacion exitosa", size=18, color=B80, bold=True)
caja(s, Inches(0.7), Inches(1.5), Inches(12.0), Inches(1.5),
     bullet_list([
       "240 variables proposicionales + 4 reglas formales capturan exhaustivamente el hexagrama.",
       "Sin ambiguedades, sin configuraciones invalidas.",
       "Un solo descriptor binario D_{n,c} es suficiente para representar todo el problema.",
     ], size=12))

caja(s, Inches(0.5), Inches(3.2), Inches(12.3), Inches(0.5),
     "2. Implementacion computacional validada", size=18, color=B80, bold=True)
caja(s, Inches(0.7), Inches(3.7), Inches(12.0), Inches(1.5),
     bullet_list([
       "Python con clases Formula, Letra, Negacion, Binario, Descriptor, Numero.",
       "Metodologia incremental: regla por regla y luego la conjuncion total.",
       "Visualizador grafico coherente con el diccionario booleano del solver.",
     ], size=12))

caja(s, Inches(0.5), Inches(5.4), Inches(12.3), Inches(0.5),
     "3. Diferencias cualitativas entre paradigmas", size=18, color=B80, bold=True)
caja(s, Inches(0.7), Inches(5.9), Inches(12.0), Inches(1.5),
     bullet_list([
       "Metodos exhaustivos (tabla, tableaux): impracticables (>15h en la conjuncion total).",
       "Metodos estocasticos (WalkSAT): incompletos, atrapados en optimos locales.",
       "Metodos sistematicos avanzados (DPLL, MiniSAT22): unicos exitosos en el limite de tiempo.",
     ], size=12))

# ---- SLIDE 45: conclusiones 2/3 ----
s = prs.slides.add_slide(BLANK); fondo(s, B00)
header_bar(s, "Conclusiones Principales  (2/3)", 45); footer_bar(s)

caja(s, Inches(0.5), Inches(1.0), Inches(12.3), Inches(0.5),
     "4. Evolucion algoritmica de SAT (1950 - 1990s)", size=18, color=B80, bold=True)

table_x = Inches(1.5); table_y = Inches(1.7)
col_widths = [Inches(2.0), Inches(4.0), Inches(4.5)]
row_h = Inches(0.55)
filas = [
    ("Decada",  "Algoritmo",                "Aporte clave"),
    ("1950s",   "Tablas de Verdad",          "Enumeracion exhaustiva"),
    ("1960s",   "Tableaux Semanticos",       "Descomposicion sistematica"),
    ("1962",    "DPLL",                      "Propagacion unitaria (breakthrough)"),
    ("1990s",   "WalkSAT",                   "Busqueda local estocastica"),
    ("1990s+",  "CDCL / MiniSAT",            "Aprendizaje de clausulas"),
]
for i, fila in enumerate(filas):
    x = table_x
    y = table_y + row_h * i
    for j, val in enumerate(fila):
        if i == 0:
            add_rect(s, x, y, col_widths[j], row_h, fill=B70,
                     line=B50, line_w=0.4)
            caja(s, x, y, col_widths[j], row_h, val,
                 size=12, color=WHITE, bold=True,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        else:
            bg = B00 if i % 2 == 0 else B05
            add_rect(s, x, y, col_widths[j], row_h, fill=bg,
                     line=B20, line_w=0.4)
            caja(s, x, y, col_widths[j], row_h, val, size=12,
                 color=B80 if j != 2 else INK, bold=(j == 1),
                 align=PP_ALIGN.CENTER if j == 0 else PP_ALIGN.LEFT,
                 anchor=MSO_ANCHOR.MIDDLE)
        x += col_widths[j]

caja(s, Inches(0.5), Inches(5.5), Inches(12.3), Inches(0.5),
     "Transformacion: intratable → tratable", size=16, color=B80, bold=True)
caja(s, Inches(0.7), Inches(6.0), Inches(12.0), Inches(1.0),
     bullet_list([
       "Propagacion unitaria (DPLL): reduccion exponencial del espacio de busqueda.",
       "Aprendizaje de conflictos (CDCL): \"memoria\" adaptativa que no repite errores.",
       "Mas de 40 anos de innovacion algoritmica entre el papel y MiniSAT22.",
     ], size=12))

# ---- SLIDE 46: conclusiones 3/3 ----
s = prs.slides.add_slide(BLANK); fondo(s, B00)
header_bar(s, "Conclusiones Principales  (3/3)", 46); footer_bar(s)

caja(s, Inches(0.5), Inches(1.0), Inches(12.3), Inches(0.5),
     "5. Principios fundamentales ilustrados", size=18, color=B80, bold=True)

principios = [
    ("Formalizacion = fundamento",
     "Una traduccion precisa de la descripcion informal a logica proposicional es la base de todo lo que sigue."),
    ("Complejidad inherente ≠ complejidad algoritmica",
     "12! = 479,001,600 permutaciones; las heuristicas inteligentes encuentran la solucion sin enumerar."),
    ("Trade-offs: completitud vs eficiencia",
     "WalkSAT renuncia a completitud por velocidad; MiniSAT22 logra ambas con aprendizaje de conflictos."),
    ("Eleccion critica: el algoritmo determina la tractabilidad",
     "El mismo problema es trivial (ms) o impracticable (>24h) segun el solver elegido."),
]
y = Inches(1.55)
for tit, des in principios:
    add_rect(s, Inches(0.5), y, Inches(12.3), Inches(1.0),
             fill=B05, line=B30, line_w=0.5, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    caja(s, Inches(0.7), y + Inches(0.1), Inches(11.9), Inches(0.4),
         tit, size=13, color=B70, bold=True)
    caja(s, Inches(0.7), y + Inches(0.45), Inches(11.9), Inches(0.5),
         des, size=11, color=INK, italic=True)
    y += Inches(1.1)

caja_titulada(s, Inches(0.5), Inches(6.05), Inches(12.3), Inches(1.05),
              "Implicacion Practica",
              "Problemas de planificacion, verificacion de hardware, configuracion de redes y diseno asistido por computador frecuentemente se reducen a SAT. La eleccion del solver determina si son resolubles en segundos o intratables.",
              header_color=B70, body_color=B05, body_size=12)

# ---- SLIDE 47: trabajos futuros ----
s = prs.slides.add_slide(BLANK); fondo(s, B00)
header_bar(s, "Trabajos Futuros", 47); footer_bar(s)

caja(s, Inches(0.5), Inches(1.1), Inches(12.3), Inches(0.5),
     "Direcciones prometedoras a partir de este trabajo:",
     size=15, color=B80, bold=True)
futuros = [
    ("Generalizacion a estrellas mas grandes",
     "Estrella magica con m > 6. Las variables crecen como m * (numero de casillas), y el numero de lineas tambien."),
    ("Optimizacion de codificaciones",
     "Variables auxiliares para sumas (codificaciones cardinales eficientes). Comparar order encoding vs direct encoding."),
    ("Analisis de complejidad formal",
     "Estudiar si el problema generalizado es NP-completo o pertenece a clases mas refinadas (P #SAT)."),
    ("Paralelizacion",
     "Distribuir el espacio de busqueda entre multiples nucleos / maquinas. SAT paralelo (Plingeling, etc.)."),
    ("Variantes",
     "Semi-magicos, diabolicos, pandiagonales. Hexagramas con sumas adicionales en diametros."),
    ("Integracion con IA",
     "Machine learning para predecir buenas heuristicas de seleccion variable (aprender VSIDS)."),
]
y = Inches(1.85)
for tit, des in futuros:
    add_rect(s, Inches(0.5), y, Inches(0.5), Inches(0.5),
             fill=B70, shape=MSO_SHAPE.OVAL)
    # icono numero pero usamos punto
    caja(s, Inches(0.5), y, Inches(0.5), Inches(0.5),
         "+", size=18, color=WHITE, bold=True,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    caja(s, Inches(1.2), y - Inches(0.02), Inches(11.6), Inches(0.32),
         tit, size=13, color=B80, bold=True)
    caja(s, Inches(1.2), y + Inches(0.28), Inches(11.6), Inches(0.5),
         des, size=11, color=INK)
    y += Inches(0.85)

# ---- SLIDE 48: sintesis final ----
s = prs.slides.add_slide(BLANK); fondo(s, B00)
header_bar(s, "Sintesis Final", 48); footer_bar(s)

caja_titulada(s, Inches(0.5), Inches(1.1), Inches(12.3), Inches(1.4),
              "Demostracion Central",
              "La logica proposicional, pese a su aparente simplicidad sintactica, posee EXPRESIVIDAD SUFICIENTE para codificar problemas combinatorios complejos como el hexagrama magico, y los SAT-solvers modernos los resuelven eficazmente.",
              header_color=B70, body_color=B05, body_size=14)

caja(s, Inches(0.5), Inches(2.85), Inches(12.3), Inches(0.5),
     "Validacion exitosa:", size=16, color=B80, bold=True)
caja(s, Inches(0.5), Inches(3.35), Inches(12.3), Inches(2.3),
     bullet_list([
       "Formalizacion matematica rigurosa (240 atomos + 4 reglas).",
       "Implementacion computacional correcta en Python (clases reutilizables).",
       "Evaluacion experimental exhaustiva (5 solvers, regla por regla y conjuncion total).",
       "Formula SATISFACIBLE (80 configuraciones fundamentales).",
       "Solo DPLL y MiniSAT22 resuelven el problema completo en hardware estandar dentro de 24h.",
     ], size=13))

caja_titulada(s, Inches(0.5), Inches(6.0), Inches(12.3), Inches(1.1),
              "Contribucion del Proyecto",
              "Combinar comprension teorica (logica + computacion + complejidad) con practica ingenieril (modelado, codificacion eficiente, comparacion experimental rigurosa).",
              header_color=B70, body_color=B10, body_size=12)


# =============================================================
# SECCION 9 - AGRADECIMIENTOS
# =============================================================
slide_seccion(9, 9, "Agradecimientos", 49,
              "Las personas e instituciones sin las cuales\neste trabajo no habria sido posible.")

# ---- SLIDE 50: Agradecimientos ----
s = prs.slides.add_slide(BLANK); fondo(s, B00)
header_bar(s, "Agradecimientos", 50); footer_bar(s)

caja(s, Inches(0.5), Inches(1.3), Inches(12.3), Inches(0.6),
     "Agradecemos especialmente al profesor",
     size=18, color=B70, italic=True, align=PP_ALIGN.CENTER)
caja(s, Inches(0.5), Inches(1.95), Inches(12.3), Inches(1.0),
     "Daniel Alfonso Bojaca",
     size=46, color=B80, bold=True, align=PP_ALIGN.CENTER)
caja(s, Inches(0.5), Inches(3.0), Inches(12.3), Inches(1.0),
     [
       "por su invaluable orientacion durante el desarrollo de este proyecto",
       "en el curso de Logica para Ciencias de la Computacion.",
     ],
     size=15, color=B60, italic=True, align=PP_ALIGN.CENTER)

caja(s, Inches(0.5), Inches(4.5), Inches(12.3), Inches(0.5),
     "Tambien agradecemos:",
     size=14, color=B80, bold=True, align=PP_ALIGN.CENTER)
caja(s, Inches(0.5), Inches(5.0), Inches(12.3), Inches(2.0),
     [
       "·  A la comunidad de Matematicas Aplicadas y Ciencias de la Computacion (MACC).",
       "·  A los autores de PySAT y MiniSAT22 por proveer un solver de estado del arte accesible.",
       "·  A los companeros del curso con quienes discutimos estrategias y representaciones.",
     ], size=13, color=INK, align=PP_ALIGN.CENTER, line_spacing=1.4)

# ---- SLIDE 51: Gracias por su atencion ----
s = prs.slides.add_slide(BLANK); fondo(s, B70)
# detalle horizontal
add_rect(s, 0, Inches(0.0), SW, Inches(0.18), fill=B40)
add_rect(s, 0, SH - Inches(0.18), SW, Inches(0.18), fill=B40)

caja(s, Inches(0.5), Inches(1.6), Inches(12.3), Inches(1.5),
     "Gracias por su atencion!", size=64, color=WHITE, bold=True,
     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

caja(s, Inches(0.5), Inches(3.3), Inches(12.3), Inches(0.7),
     "Preguntas?", size=30, color=B20, italic=True,
     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

caja(s, Inches(0.5), Inches(4.5), Inches(12.3), Inches(0.5),
     "Contacto", size=14, color=B20, bold=True,
     align=PP_ALIGN.CENTER)
caja(s, Inches(0.5), Inches(5.0), Inches(12.3), Inches(1.5),
     [
       "samuel.galindo@urosario.edu.co",
       "john.valbuena@urosario.edu.co",
       "alejandro.jimenez@urosario.edu.co",
     ], size=14, color=WHITE, align=PP_ALIGN.CENTER, line_spacing=1.4)

caja(s, Inches(0.5), Inches(6.9), Inches(12.3), Inches(0.3),
     "Logica para Ciencias de la Computacion  ·  MACC  ·  2026-01",
     size=10, color=B20, italic=True, align=PP_ALIGN.CENTER)


# =============================================================
out = os.path.join(BASE, 'Presentacion_Hexagrama_v3.pptx')
try:
    prs.save(out)
except PermissionError:
    out = os.path.join(BASE, 'Presentacion_Hexagrama_v3_alt.pptx')
    prs.save(out)
print("OK:", out)
print(f"Total slides generadas: {len(prs.slides)}")
