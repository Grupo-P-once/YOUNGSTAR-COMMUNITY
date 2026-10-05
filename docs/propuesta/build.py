# -*- coding: utf-8 -*-
"""Propuesta Youngstar (sin precios). Ejecutar: python3 docs/propuesta/build.py"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
                                TableStyle, Flowable, PageBreak, KeepTogether)
from reportlab.pdfgen import canvas as rl_canvas

AGENCIA = "[Nombre de la agencia]"
FECHA = "[Ciudad] · Octubre 2026"
CONTACTO = "[correo] · [teléfono / WhatsApp] · [sitio web]"

W_PAGE, H_PAGE = letter
M = 1.6 * cm
W = W_PAGE - 2 * M
GREEN = colors.HexColor("#14654F"); TEAL = colors.HexColor("#1B8C72")
MINT = colors.HexColor("#E8F5F0"); MINT_B = colors.HexColor("#BFDDD2")
DIAM = colors.HexColor("#F2F8F6"); BORDER = colors.HexColor("#D9E3DF")
INK = colors.HexColor("#1A1F1D"); TXT = colors.HexColor("#2B2F2E"); MUTED = colors.HexColor("#6B7370")
GREYBG = colors.HexColor("#F6F8F7"); AMBER_BG = colors.HexColor("#FBF3E2"); AMBER = colors.HexColor("#B8892B")

def S(name, **kw):
    base = dict(fontName="Helvetica", fontSize=9.6, leading=14, textColor=TXT)
    base.update(kw); return ParagraphStyle(name, **base)
body = S("body"); small = S("small", fontSize=8.6, leading=12, textColor=MUTED)
lead = S("lead", fontSize=11, leading=16, textColor=MUTED)
card_t = S("card_t", fontName="Helvetica-Bold", fontSize=10.5, leading=14, textColor=GREEN)
card_b = S("card_b", fontSize=9, leading=12.6)
card_bw = S("card_bw", fontSize=9, leading=12.6, textColor=colors.white)
sub_h = S("sub_h", fontName="Helvetica-Bold", fontSize=11.5, leading=15, textColor=GREEN, spaceBefore=10, spaceAfter=4)
big = S("big", fontName="Helvetica-Bold", fontSize=21, leading=25, textColor=GREEN)
bigc = S("bigc", parent=None, fontName="Helvetica-Bold", fontSize=30, leading=34, textColor=GREEN, alignment=1) if False else S("bigc", fontName="Helvetica-Bold", fontSize=30, leading=34, textColor=GREEN, alignment=1)
cap = S("cap", fontSize=8.4, leading=11.5, textColor=MUTED)
capc = S("capc", fontSize=9.4, leading=13, textColor=TXT, alignment=1)
center = S("center", fontSize=9, leading=12.5, alignment=1)
centerb = S("centerb", fontName="Helvetica-Bold", fontSize=9, leading=12.5, alignment=1, textColor=GREEN)
bul = S("bul", fontSize=9.2, leading=13, leftIndent=11, bulletIndent=0, spaceAfter=2)
th = S("th", fontName="Courier-Bold", fontSize=7.8, leading=10, textColor=MUTED)
td = S("td", fontSize=9, leading=12.5); tdb = S("tdb", fontName="Helvetica-Bold", fontSize=9, leading=12.5)
tdc = S("tdc", fontSize=9, leading=12.5, alignment=1, textColor=GREEN)
mono = S("mono", fontName="Courier", fontSize=8.4, leading=11.5, textColor=MUTED, alignment=2)

def P(t, s=body): return Paragraph(t, s)
def G(t): return '<font color="#14654F"><b>%s</b></font>' % t

# ---------------------------------------------------------------- flowables
class Eyebrow(Flowable):
    def __init__(s, text, color=GREEN, size=8, space=2.2, align="left"):
        super().__init__(); s.text, s.color, s.size, s.space, s.align = text, color, size, space, align
    def wrap(s, aw, ah): s.aw = aw; return aw, s.size + 6
    def draw(s):
        t = s.canv.beginText(); t.setFont("Courier-Bold", s.size); t.setFillColor(s.color); t.setCharSpace(s.space)
        tw = s.canv.stringWidth(s.text, "Courier-Bold", s.size) + s.space * len(s.text)
        x = 0 if s.align == "left" else (s.aw - tw) / 2
        t.setTextOrigin(x, 2); t.textOut(s.text); t.setCharSpace(0); s.canv.drawText(t)

class SectionHead(Flowable):
    def __init__(s, num, title, size=21, r=11):
        super().__init__(); s.num, s.title, s.size, s.r = num, title, size, r; s.keepWithNext = True
    def wrap(s, aw, ah): return aw, s.r * 2 + 6
    def draw(s):
        c = s.canv; c.setFillColor(TEAL); c.circle(s.r, s.r + 2, s.r, stroke=0, fill=1)
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold", s.r * 0.9); c.drawCentredString(s.r, s.r + 2 - s.r * 0.32, str(s.num))
        c.setFillColor(INK); c.setFont("Helvetica-Bold", s.size); c.drawString(s.r * 2 + 9, s.r + 2 - s.size * 0.33, s.title)

class Arrow(Flowable):
    def wrap(s, aw, ah): s.aw = aw; return aw, 14
    def draw(s):
        c = s.canv; c.setStrokeColor(TEAL); c.setFillColor(TEAL); c.setLineWidth(1.4)
        x0, x1, y = 3, s.aw - 3, 7; c.line(x0, y, x1 - 4, y)
        p = c.beginPath(); p.moveTo(x1, y); p.lineTo(x1 - 6, y + 4); p.lineTo(x1 - 6, y - 4); p.close(); c.drawPath(p, stroke=0, fill=1)

class Card(Flowable):
    def __init__(s, content, bg=colors.white, border=BORDER, pad=11, radius=6, bar=None, fixed_h=None, width=None):
        super().__init__(); s.content = content; s.bg, s.border, s.pad, s.radius, s.bar = bg, border, pad, radius, bar
        s.fixed_h = fixed_h; s.fw = width
    def wrap(s, aw, ah):
        s.w = s.fw or aw; inner = s.w - 2 * s.pad - (4 if s.bar else 0); h = 0; s.sizes = []
        for f in s.content:
            _, fh = f.wrap(inner, 10000); s.sizes.append(fh); h += fh
        s.h = max(h + 2 * s.pad, s.fixed_h or 0); s.ch = h; return s.w, s.h
    def draw(s):
        c = s.canv; c.setFillColor(s.bg); c.setStrokeColor(s.border if s.border else s.bg); c.setLineWidth(0.8)
        c.roundRect(0, 0, s.w, s.h, s.radius, stroke=1 if s.border else 0, fill=1)
        x0 = s.pad + (4 if s.bar else 0)
        if s.bar:
            c.setFillColor(s.bar); c.rect(0, 0, 3.5, s.h, stroke=0, fill=1)
        y = s.h - s.pad
        for f, fh in zip(s.content, s.sizes):
            f.drawOn(c, x0, y - fh); y -= fh

def equalize(cards, w):
    hs = []
    for c in cards: c.fixed_h = None; hs.append(c.wrap(w, 10000)[1])
    m = max(hs)
    for c in cards: c.fixed_h = m

def grid(cards, cols=2, gap=12, total=W):
    cw = (total - gap * (cols - 1)) / cols; rows = []
    for i in range(0, len(cards), cols):
        chunk = cards[i:i + cols]; equalize(chunk, cw)
        row = []
        for j, c in enumerate(chunk):
            row.append(c)
            if j < cols - 1: row.append("")
        while len(row) < cols * 2 - 1: row.append("")
        rows.append(row)
    widths = []
    for j in range(cols): widths += [cw] + ([gap] if j < cols - 1 else [])
    t = Table(rows, colWidths=widths)
    t.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                           ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), gap),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t

def card(title, text, mint=False):
    return Card([P(title, card_t), Spacer(1, 3), P(text, card_b)], bg=MINT if mint else colors.white, border=MINT_B if mint else BORDER)

def line_card(text, mint):
    return Card([P(text, S("lc", fontSize=9.2, leading=12.8, textColor=INK if mint else MUTED,
                           fontName="Helvetica-Bold" if mint else "Helvetica"))], bg=MINT if mint else GREYBG,
                border=MINT_B if mint else BORDER, pad=8.5, radius=5)

def before_after(left_h, right_h, rows):
    cw = (W - 12) / 2
    head = Table([[Eyebrow(left_h, MUTED, 7.4, 1.8), "", Eyebrow(right_h, GREEN, 7.4, 1.8)]], colWidths=[cw, 12, cw])
    head.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0)]))
    cards = []
    for l, r in rows: cards += [line_card(l, False), line_card(r, True)]
    t = grid(cards, 2, 7)
    return [head, Spacer(1, 3), t]

def problem_block(n, title, prob, sol, ben):
    cw = (W - 2 * 10) / 3
    c1 = Card([Eyebrow("EL PROBLEMA", MUTED, 7.2, 1.8), Spacer(1, 3), P(prob, card_b)], bg=GREYBG, border=BORDER)
    c2 = Card([Eyebrow("CÓMO LO RESOLVEMOS", GREEN, 7.2, 1.8), Spacer(1, 3), P(sol, card_b)], bg=colors.white, border=MINT_B)
    c3 = Card([Eyebrow("QUÉ GANA YOUNGSTAR", GREEN, 7.2, 1.8), Spacer(1, 3), P(ben, S("ben", fontSize=9, leading=12.6, textColor=GREEN, fontName="Helvetica-Bold"))], bg=MINT, border=MINT_B)
    return KeepTogether([SectionHead(n, title, size=13.5, r=9), Spacer(1, 6), grid([c1, c2, c3], 3, 10), Spacer(1, 4)])

def callout(text, bg=AMBER_BG, bar=AMBER):
    return Card([P(text, S("co", fontSize=9.4, leading=13.6))], bg=bg, border=None, bar=bar, pad=13, radius=4)

def banner(text):
    return Card([P(text, S("bn", fontSize=11.5, leading=16.5, textColor=colors.white, alignment=1))], bg=TEAL, border=None, pad=18, radius=7)

def tbl(rows, widths, header=True):
    data = []
    for r, row in enumerate(rows):
        data.append([P(c, th if (header and r == 0) else (tdb if i == 0 else (tdc if (i > 0 and len(widths) > 2) else td))) for i, c in enumerate(row)])
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    st = [("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LINEBELOW", (0, 0), (-1, -2), 0.5, BORDER),
          ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
          ("LEFTPADDING", (0, 0), (-1, -1), 11), ("RIGHTPADDING", (0, 0), (-1, -1), 11),
          ("BOX", (0, 0), (-1, -1), 0.8, BORDER), ("ROUNDEDCORNERS", [6, 6, 6, 6])]
    if header: st.append(("BACKGROUND", (0, 0), (-1, 0), GREYBG))
    t.setStyle(TableStyle(st)); return t

def timeline(rows):
    data = [[P(a, mono), P(b, body)] for a, b in rows]
    t = Table(data, colWidths=[2.9 * cm, W - 2.9 * cm])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (1, 0), (1, -2), 0.5, BORDER),
                           ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                           ("LEFTPADDING", (0, 0), (0, -1), 0), ("RIGHTPADDING", (0, 0), (0, -1), 12),
                           ("LEFTPADDING", (1, 0), (1, -1), 10), ("RIGHTPADDING", (1, 0), (1, -1), 0)]))
    return t

def stats(items):
    n = len(items); cw = W / n
    data = [[[P(a, big), Spacer(1, 2), P(b, cap)] for a, b in items]]
    t = Table(data, colWidths=[cw] * n)
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.8, BORDER), ("LINEAFTER", (0, 0), (-2, -1), 0.8, BORDER),
                           ("ROUNDEDCORNERS", [6, 6, 6, 6]), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 13), ("BOTTOMPADDING", (0, 0), (-1, -1), 13),
                           ("LEFTPADDING", (0, 0), (-1, -1), 13), ("RIGHTPADDING", (0, 0), (-1, -1), 11)]))
    return t

def flow_diagram():
    def box(t, sub, mint=False):
        return Card([P("<b>%s</b>" % t, centerb if mint else S("cb2", fontName="Helvetica-Bold", fontSize=9, leading=12, alignment=1, textColor=INK)),
                     P(sub, S("cs", fontSize=7.8, leading=10.5, alignment=1, textColor=MUTED))],
                    bg=MINT if mint else colors.white, border=MINT_B if mint else BORDER, pad=8)
    bw, aw = 3.05 * cm, 0.95 * cm
    boxes = [box("Formulario", "datos del atleta"), box("Airtable", "base central"), box("Dashboard + IA", "genera los planes", True), box("TrainingPeaks", "plataforma del atleta")]
    cells, widths = [], []
    for i, b in enumerate(boxes):
        cells.append(b); widths.append(bw)
        if i < len(boxes) - 1: cells.append(Arrow()); widths.append(aw)
    tot = sum(widths); pad = (W - tot) / 2
    t = Table([cells], colWidths=widths); t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    t.hAlign = "CENTER"
    return t

# ---------------------------------------------------------------- page decoration
def background(c, doc):
    c.saveState(); p = c.beginPath(); p.rect(0, 0, W_PAGE - M + 4, H_PAGE); c.clipPath(p, stroke=0, fill=0)
    c.setFillColor(DIAM); hd = 63
    for cx in (154, 380, 605):
        for cy in (632, 407, 182):
            q = c.beginPath(); q.moveTo(cx, cy + hd); q.lineTo(cx + hd, cy); q.lineTo(cx, cy - hd); q.lineTo(cx - hd, cy); q.close()
            c.drawPath(q, stroke=0, fill=1)
    c.restoreState()

def cover(c, doc):
    background(c, doc); cx = W_PAGE / 2
    c.saveState(); t = c.beginText(); t.setFont("Courier-Bold", 8.5); t.setFillColor(GREEN); t.setCharSpace(3.2)
    txt = "PROPUESTA DE SERVICIO"; tw = c.stringWidth(txt, "Courier-Bold", 8.5) + 3.2 * len(txt)
    t.setTextOrigin(cx - tw / 2, 600); t.textOut(txt); t.setCharSpace(0); c.drawText(t)
    c.setFillColor(MINT); c.setStrokeColor(MINT_B); c.circle(cx, 545, 44, stroke=1, fill=1)
    c.setFillColor(GREEN); c.setFont("Helvetica-Bold", 26); c.drawCentredString(cx, 536, "YS")
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 31)
    c.drawCentredString(cx, 468, "Mantenimiento y operación"); c.drawCentredString(cx, 431, "de la plataforma")
    c.setFillColor(TXT); c.setFont("Helvetica", 12.5)
    c.drawCentredString(cx, 398, "Datos confiables, planes seguros y seguimiento continuo,")
    c.drawCentredString(cx, 380, "con el doctor siempre al mando.")
    c.setStrokeColor(TEAL); c.setLineWidth(2.2); c.line(cx - 23, 350, cx + 23, 350)
    t = c.beginText(); t.setFont("Courier-Bold", 8.5); t.setFillColor(MUTED); t.setCharSpace(2.6)
    txt = "PREPARADA PARA"; tw = c.stringWidth(txt, "Courier-Bold", 8.5) + 2.6 * len(txt)
    t.setTextOrigin(cx - tw / 2, 322); t.textOut(txt); t.setCharSpace(0); c.drawText(t)
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 20); c.drawCentredString(cx, 296, "Youngstar Community")
    t = c.beginText(); t.setFont("Courier-Bold", 8.5); t.setFillColor(MUTED); t.setCharSpace(2.6)
    txt = "PREPARADA POR"; tw = c.stringWidth(txt, "Courier-Bold", 8.5) + 2.6 * len(txt)
    t.setTextOrigin(cx - tw / 2, 256); t.textOut(txt); t.setCharSpace(0); c.drawText(t)
    c.setFillColor(GREEN); c.setFont("Helvetica-Bold", 18); c.drawCentredString(cx, 232, AGENCIA)
    c.setFillColor(MUTED); c.setFont("Courier", 9); c.drawCentredString(cx, 204, FECHA)
    c.restoreState()

class NumberedCanvas(rl_canvas.Canvas):
    def __init__(s, *a, **k): super().__init__(*a, **k); s._saved = []
    def showPage(s): s._saved.append(dict(s.__dict__)); s._startPage()
    def save(s):
        n = len(s._saved)
        for st in s._saved:
            s.__dict__.update(st); s.chrome(n); super().showPage()
        super().save()
    def chrome(s, n):
        s.setFont("Helvetica", 7.6); s.setFillColor(colors.HexColor("#9AA3A0"))
        s.drawString(M, H_PAGE - 1.1 * cm, "%s  ·  Mantenimiento y operación tecnológica" % AGENCIA)
        s.drawRightString(W_PAGE - M, H_PAGE - 1.1 * cm, "Propuesta · Youngstar Community")
        s.drawCentredString(W_PAGE / 2, 1.1 * cm, "Página %d de %d" % (s._pageNumber, n))

# ---------------------------------------------------------------- contenido
s = [PageBreak()]

s += [Card([Eyebrow("RESUMEN EJECUTIVO"), Spacer(1, 5),
            P("Youngstar ya tiene lo más difícil: una comunidad de <b>6 años</b>, <b>127 atletas activos</b>, cobros domiciliados "
              "funcionando y un sistema que genera planes de entrenamiento. Lo que hoy le cuesta tiempo al equipo ya no es "
              "<i>construir</i>, es <b>sostener</b>: datos que no siempre coinciden, planes que hay que corregir a mano y un seguimiento que depende de unas pocas personas.", S("r", fontSize=10.6, leading=16)),
            Spacer(1, 7),
            P("Proponemos <b>hacernos cargo de la operación técnica</b> de lo que ya existe, y mejorarlo en cuatro frentes: "
              "<b>datos confiables, entrenamientos más seguros, seguimiento que no se cae y ventas que no dependen de una sola persona</b>.", S("r2", fontSize=10.6, leading=16)),
            Spacer(1, 7),
            P("Este documento explica, problema por problema, <b>qué vamos a hacer y qué gana Youngstar</b>. "
              "Las condiciones económicas se conversan aparte, después del diagnóstico.", S("r3", fontSize=10.6, leading=16))],
           bg=MINT, border=MINT_B, pad=20, radius=8), Spacer(1, 16)]

s += [SectionHead(1, "Dónde está Youngstar hoy"), Spacer(1, 3),
      P("Cifras mencionadas por el equipo en nuestra conversación. El diagnóstico inicial las verifica contra el sistema real.", lead), Spacer(1, 8),
      stats([("6 años", "de comunidad, de las más grandes de México"), ("127", "atletas activos con pagos domiciliados"),
             ("~2 de 100", "prospectos que cierran sin intervención directa del equipo"), ("100 vs 55", "% de adherencia: el mismo atleta, visto en dos sistemas distintos")]),
      Spacer(1, 12),
      P("Así viaja hoy la información de cada atleta:", body), Spacer(1, 6), flow_diagram(), Spacer(1, 6),
      P("Cada salto entre sistemas es un punto donde un dato puede <b>perderse, duplicarse o llegar tarde</b>. Además están Stripe para los cobros, "
        "WhatsApp e Instagram para el contacto y los datos de recuperación del atleta, que se suman a la cadena.", body), Spacer(1, 14)]

s += [PageBreak(), SectionHead(2, "El reto que eso plantea"), Spacer(1, 4),
      P("No hace falta construir más: hace falta que lo construido sea <b>confiable y fácil de mantener</b>. Cuando una operación así crece, aparecen cuatro fallas que contratar más gente no arregla:", body), Spacer(1, 9),
      grid([card("Datos que no coinciden", "La adherencia, los registros y las competencias se desfasan entre sistemas, y las decisiones se toman sobre cifras equivocadas."),
            card("Planes que no se adaptan", "Si el atleta cancela una carrera o se enferma, el plan sigue como si nada, y los deportes con más piezas, como el triatlón, quedan incompletos."),
            card("Seguimiento que depende de personas", "Preguntar «cómo vas» a cada atleta, cada mes, no escala. Y el doctor y la IA pueden terminar dando indicaciones distintas."),
            card("Dependencia técnica", "El conocimiento del sistema vive en un solo proveedor y el costo de mantenerlo puede cambiar sin previo aviso.")], 2, 12),
      Spacer(1, 4), P("Lo que el mantenimiento evita", sub_h)]
s += before_after("SIN MANTENIMIENTO", "CON MANTENIMIENTO", [
    ("La adherencia cambia según dónde se mire", "Una sola fórmula y una sola fuente de verdad"),
    ("Una carrera cancelada sigue alimentando el plan", "El plan se ajusta en cuanto el atleta responde"),
    ("Un fallo se descubre cuando el atleta se queja", "Una alerta avisa antes de que alguien lo note"),
    ("El triatlón se arma sin transiciones ni técnica", "Reglas por deporte revisan cada plan"),
    ("El expediente está en la cabeza del doctor", "El expediente vive en el sistema, a la vista"),
    ("El costo mensual depende de un solo proveedor", "Alcance definido y costos variables a la vista")])
s += [PageBreak()]

s += [SectionHead(3, "Qué vamos a ofrecer"), Spacer(1, 3),
      P("Siete problemas concretos. Para cada uno: <b>qué pasa hoy, cómo lo resolvemos y qué gana Youngstar</b>.", lead), Spacer(1, 10)]
blocks = [
 ("Datos que no coinciden",
  "La adherencia aparece al 100 % en un lado y al 55 % en otro. Hay registros repetidos. La información pasa por varios sistemas y en el camino se desfasa.",
  "Mapeamos todo el recorrido del dato. Damos a cada atleta un <b>identificador único</b>, evitamos escrituras duplicadas, definimos <b>una sola fórmula de adherencia</b> y dejamos una bitácora de cada sincronización con alertas si algo falla.",
  "Cifras en las que el doctor y el equipo pueden confiar, decisiones de entrenamiento basadas en datos correctos y cierres de mes sin reconstruir nada a mano."),
 ("Competencias canceladas que siguen en el plan",
  "El atleta dijo una vez que correrá una carrera, ya no la corre, y el plan sigue subiendo volumen para ella.",
  "Un mensaje de WhatsApp antes de cada carrera: <b>«¿sigues inscrito?»</b>. La respuesta actualiza el calendario y recalcula el plan; si el cambio es grande, lo valida el doctor.",
  "Planes alineados a la realidad del atleta, menos riesgo de sobrecarga, y el equipo deja de preguntar uno por uno cada mes."),
 ("Planes incompletos en algunos deportes",
  "En triatlón no se programan bien las transiciones bici-carrera (<i>bricks</i>) ni el trabajo de técnica de natación.",
  "<b>Reglas por deporte</b>, definidas con el doctor, que revisan cada plan antes de publicarlo: bricks, descargas y límites de carga entre disciplinas. La IA propone y las reglas validan.",
  "Planes más completos y seguros, y la misma calidad en todos los deportes, no solo en running."),
 ("Conexión limitada con TrainingPeaks",
  "TrainingPeaks no abre su conexión a cualquier desarrollo, así que la información viaja por rutas indirectas y se pierde en el camino.",
  "Evaluamos tres rutas: <b>solicitar acceso como socio, cargar los planes por archivo o apoyarnos en otra plataforma abierta</b>. Recomendamos la de mejor costo-beneficio, sin prometer lo que no depende de nosotros.",
  "Una decisión informada en lugar de una apuesta, y una ruta alterna lista si el acceso se retrasa."),
 ("Seguimiento al atleta y expediente médico",
  "Saber cómo se sintió un atleta, si tiene una molestia o gripa, depende de que alguien escriba a mano. Y lo que dice la IA y lo que dice el doctor puede no coincidir.",
  "Un <b>panel del doctor</b> con el expediente de cada atleta, que alimenta al sistema. Un agente de WhatsApp de alcance acotado detecta molestias y las ajusta o <b>escala al doctor</b> según reglas que él define.",
  "Atención continua sin multiplicar las horas del equipo, indicaciones coherentes y una persona siempre al mando de las decisiones de salud."),
 ("Prospectos que no se convierten",
  "Llegan muchos prospectos y solo unos pocos cierran sin intervención directa del equipo. Un bot que «se nota» que es bot ahuyenta al interesado.",
  "Clasificamos a cada prospecto por interés (<b>alto, medio, bajo</b>), diseñamos conversaciones más naturales con memoria, campañas de recuperación y escalamiento inmediato a una persona cuando el interés es alto o empresarial.",
  "Más oportunidades aprovechadas con el mismo equipo, y fundadores con tiempo para lo importante."),
 ("Dependencia técnica y costo incierto",
  "El conocimiento del sistema vive en un solo proveedor y el costo del mantenimiento puede cambiar sin previo aviso.",
  "<b>Documentamos todo</b>, verificamos que cuentas, código y llaves estén a nombre de Youngstar y operamos con un plan mensual de alcance definido. Los costos variables (IA, servidor, mensajes) se reportan a la vista.",
  "Autonomía, costos predecibles y la libertad de cambiar de equipo cuando quieran."),
]
for i, b in enumerate(blocks, 1): s.append(problem_block(i, *b))
s += [PageBreak()]

s += [SectionHead(4, "Un mes normal, con el sistema funcionando"), Spacer(1, 3),
      P("Una ilustración de lo que cambia en la vida diaria del equipo y del atleta.", lead), Spacer(1, 8),
      timeline([
        ("1 mes antes<br/>de la carrera", "<b>Llega el mensaje de WhatsApp:</b> «¿sigues inscrito al maratón?». El atleta contesta que no."),
        ("Minutos\ndespués", "<b>El sistema quita la carrera,</b> recalcula la carga y marca el plan para revisión del doctor."),
        ("Esa tarde", "<b>El doctor revisa en su panel,</b> con el expediente a la vista, y aprueba con un clic."),
        ("Al día\nsiguiente", "<b>El atleta escribe:</b> «amanecí con gripa». El agente propone una intensidad baja y avisa al doctor. Nadie lo tuvo que perseguir."),
        ("Cada semana", "<b>La adherencia se calcula con una sola fórmula</b> y coincide en todos los reportes. Nada se duplicó."),
        ("Fin de mes", "<b>Reporte del mantenimiento:</b> incidentes atendidos, consumo de IA y servidor, y mejoras entregadas."),
      ]), Spacer(1, 12),
      Card([P("0", bigc), Spacer(1, 2), P("planes preparando una carrera que el atleta ya no va a correr", capc)], bg=MINT, border=MINT_B, pad=16, radius=8),
      Spacer(1, 16)]

s += [SectionHead(5, "Cómo lo hacemos: hoja de ruta"), Spacer(1, 3),
      P("Por fases, y <b>cada fase se aprueba por separado</b>. Los plazos son estimados y se confirman con el diagnóstico.", lead), Spacer(1, 9),
      grid([card("Fase 0 · Diagnóstico y arranque ordenado", "Inventario de herramientas y accesos, mapa del recorrido de los datos, verificación de propiedad del código y respaldos, transición coordinada con el equipo técnico actual y ruta para TrainingPeaks.<br/><b>1 a 2 semanas.</b> El informe es suyo aunque no sigamos juntos.", True),
            card("Fase 1 · Datos confiables", "Identificador único por atleta, fórmula de adherencia corregida, bitácora y alertas de sincronización, y confirmación mensual de competencias por WhatsApp.<br/><b>2 a 4 semanas.</b>"),
            card("Fase 2 · Entrenamiento y panel del doctor", "Reglas por deporte, aprobación del doctor antes de publicar, expediente de cada atleta e indicadores en español, con interpretación.<br/><b>4 a 6 semanas.</b>"),
            card("Fase 3 · Seguimiento y ventas", "Agente de WhatsApp acotado con memoria por atleta, escalamiento al doctor, clasificación de prospectos y campañas de recuperación.<br/><b>4 a 6 semanas.</b>")], 2, 12),
      Spacer(1, 4)]
s += [PageBreak()]

s += [SectionHead(6, "Mantenimiento mensual"), Spacer(1, 3),
      P("Para que la plataforma siga sana después de las mejoras. Tres niveles; los precios se presentan después del diagnóstico.", lead), Spacer(1, 9),
      tbl([["INCLUIDO", "BÁSICO", "ESTÁNDAR", "PLUS"],
           ["Monitoreo de flujos, pagos y sincronizaciones", "Sí", "Sí", "Sí"],
           ["Alertas y corrección de errores", "Sí", "Sí", "Sí"],
           ["Respaldos y actualizaciones de seguridad", "Sí", "Sí", "Sí"],
           ["Reporte mensual (incidentes, consumo, métricas)", "Sí", "Sí", "Sí"],
           ["Horas mensuales de mejoras", "–", "Incluidas", "Ampliadas"],
           ["Atención en fines de semana", "–", "–", "Sí"],
           ["Revisión de planes con el doctor", "–", "Trimestral", "Mensual"]],
          [W - 3 * 2.9 * cm, 2.9 * cm, 2.9 * cm, 2.9 * cm]), Spacer(1, 8),
      callout("<b>Los costos variables van a la vista.</b> IA, servidor, APIs y mensajería se reportan cada mes, sin margen oculto, con un tope acordado y aviso previo al llegar al 80 %."),
      Spacer(1, 12)]
s += [P("Qué incluye y qué no", sub_h),
      grid([Card([P("Incluye", card_t), Spacer(1, 3), P("Monitoreo, corrección de errores, soporte técnico, respaldos, actualizaciones y reportes mensuales.", card_b)], bg=MINT, border=MINT_B),
            Card([P("Se cotiza aparte", card_t), Spacer(1, 3), P("Funciones nuevas de gran alcance, rediseños, cambio de plataforma, atención directa a atletas y decisiones médicas.", card_b)])], 2, 12), Spacer(1, 6)]

s += [SectionHead(7, "Cómo sabremos que funciona"), Spacer(1, 3),
      P("Indicadores que se miden desde el primer mes y aparecen en el reporte mensual.", lead), Spacer(1, 8),
      grid([card("Datos", "Adherencia igual en todos los reportes y sin registros duplicados."),
            card("Planes", "Ningún plan sale sin pasar las reglas y la revisión del doctor."),
            card("Seguimiento", "Toda molestia reportada se atiende o escala en el horario acordado."),
            card("Ventas", "Prospectos que avanzan en cada etapa, medidos desde el mes 1.")], 4, 8),
      PageBreak(), SectionHead(8, "Qué es de quién"), Spacer(1, 6)]
s += before_after("DE LA AGENCIA", "DE YOUNGSTAR", [
    ("Nuestra metodología y herramientas internas", "Sus atletas y todos sus datos"),
    ("El trabajo y la documentación que se entrega", "Cuentas, accesos y llaves del sistema"),
    ("Nuestro tiempo, con alcance definido", "El código y la plataforma que ya pagaron"),
    ("Confidencialidad sobre lo que veamos", "Todo exportable cuando quieran")])
s += [Spacer(1, 8), P("La línea es simple: <b>nosotros aportamos el trabajo, Youngstar conserva todo lo suyo.</b> Contratar el servicio no nos da ningún derecho sobre la información, y se firma un acuerdo de confidencialidad antes de acceder a cualquier sistema.", body), Spacer(1, 8),
      callout("<b>Datos de salud.</b> La información de los atletas incluye datos de salud, que la ley mexicana trata como datos personales sensibles. Recomendamos revisar con el área legal de Youngstar el aviso de privacidad y el consentimiento. <b>Este documento es un resumen, no el contrato.</b>"), Spacer(1, 16)]

s += [SectionHead(9, "Siguientes pasos"), Spacer(1, 6)]
steps = [("Revisión de este documento", "Que el equipo confirme que refleja lo que de verdad necesita, y que no falte nada."),
         ("Acuerdo de confidencialidad", "Lo firmamos antes de pedir cualquier acceso."),
         ("Reunión técnica y accesos de lectura", "Con el equipo que desarrolló la plataforma, para recibir la documentación."),
         ("Diagnóstico (Fase 0)", "De 1 a 2 semanas, con informe y plan priorizado."),
         ("Propuesta económica", "Con el diagnóstico en la mano, la ajustamos al sistema real y a lo que Youngstar necesite.")]
class Step(Flowable):
    def __init__(s, n, t, d): super().__init__(); s.n, s.t, s.d = n, t, d
    def wrap(s, aw, ah):
        s.p = P(s.d, body); _, h = s.p.wrap(aw - 34, 1000); s.h = h + 22; s.w = aw; return aw, s.h
    def draw(s):
        c = s.canv; c.setFillColor(TEAL); c.circle(10, s.h - 11, 9.5, stroke=0, fill=1)
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 9.5); c.drawCentredString(10, s.h - 14.2, str(s.n))
        c.setFillColor(INK); c.setFont("Helvetica-Bold", 11.5); c.drawString(30, s.h - 15, s.t)
        s.p.drawOn(c, 30, s.h - 18 - s.p.height + 0)
for i, (t, d) in enumerate(steps, 1): s.append(Step(i, t, d)); s.append(Spacer(1, 2))
s += [Spacer(1, 14), banner("El sistema ya existe. Este documento no propone empezar de cero: propone <b>cuidarlo, ordenarlo y hacerlo crecer</b> sin que Youngstar dependa de nadie para que funcione."),
      Spacer(1, 16), P("<b>%s</b>" % AGENCIA, S("ag", fontName="Helvetica-Bold", fontSize=17, leading=22, textColor=GREEN, alignment=1)),
      P(CONTACTO, S("ct", fontName="Courier", fontSize=8.8, leading=13, textColor=MUTED, alignment=1))]

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Propuesta-Mantenimiento-Youngstar.pdf")
doc = BaseDocTemplate(out, pagesize=letter, title="Propuesta de mantenimiento - Youngstar Community", author=AGENCIA,
                      leftMargin=M, rightMargin=M, topMargin=1.9 * cm, bottomMargin=1.9 * cm)
fr = Frame(M, 1.9 * cm, W, H_PAGE - 3.8 * cm, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
doc.addPageTemplates([PageTemplate(id="first", frames=[fr], onPage=cover, autoNextPageTemplate="rest"),
                      PageTemplate(id="rest", frames=[fr], onPage=background)])
doc.build(s, canvasmaker=NumberedCanvas)
print("ok", out)
