from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, KeepTogether)

NAVY = colors.HexColor("#14213D"); ACC = colors.HexColor("#E85D04")
GREY = colors.HexColor("#555555"); LIGHT = colors.HexColor("#F3F4F6")

body = ParagraphStyle("b", fontName="Helvetica", fontSize=9.5, leading=13.2, textColor=colors.HexColor("#222222"))
small = ParagraphStyle("s", parent=body, fontSize=9, leading=12.5, textColor=GREY)
h1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=24, leading=28, textColor=NAVY)
sub = ParagraphStyle("sub", parent=body, fontSize=12, leading=16, textColor=GREY)
h2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=14, leading=18, textColor=NAVY, spaceBefore=10, spaceAfter=4)
h3 = ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=10.5, leading=14, textColor=ACC, spaceBefore=6, spaceAfter=2)
bul = ParagraphStyle("bul", parent=body, leftIndent=12, bulletIndent=2, spaceAfter=2)
cell = ParagraphStyle("c", parent=body, fontSize=9, leading=12.5)
cellb = ParagraphStyle("cb", parent=cell, fontName="Helvetica-Bold", textColor=colors.white)

def P(t, s=body): return Paragraph(t, s)
def B(items): return [Paragraph(i, bul, bulletText="•") for i in items]

def tbl(rows, widths, header=True):
    data = [[Paragraph(c, cellb if (header and r == 0) else cell) for c in row] for r, row in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    st = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D1D5DB")),
          ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]
    if header:
        st += [("BACKGROUND", (0, 0), (-1, 0), NAVY)]
        st += [("BACKGROUND", (0, i), (-1, i), LIGHT) for i in range(2, len(rows), 2)]
    t.setStyle(TableStyle(st)); return t

def footer(c, d):
    c.saveState(); c.setFont("Helvetica", 8); c.setFillColor(GREY)
    c.drawString(2*cm, 1.2*cm, "Propuesta confidencial – Youngstar Community")
    c.drawRightString(letter[0]-2*cm, 1.2*cm, "Página %d" % d.page)
    c.setStrokeColor(ACC); c.setLineWidth(2); c.line(2*cm, letter[1]-1.2*cm, letter[0]-2*cm, letter[1]-1.2*cm)
    c.restoreState()

s = []
s += [Spacer(1, 0.2*cm), P("Propuesta de mantenimiento<br/>y operación tecnológica", h1), Spacer(1, 6),
      P("Para <b>Youngstar Community</b>", sub), P("Preparada por: <b>[Nombre de la agencia]</b> &nbsp;|&nbsp; Fecha: [fecha]", sub), Spacer(1, 14)]

s += [P("1. Lo que entendimos", h2),
      P("Youngstar ya tiene un producto funcionando: una comunidad con 6 años de historia, 127 atletas activos, cobros "
        "domiciliados y un sistema que genera planes de entrenamiento. La base está hecha. Lo que se busca ahora es "
        "<b>operarlo con estabilidad, a un costo claro y sin depender de una sola persona</b>, para que el equipo se enfoque en los atletas.")]
s += [P("Los retos que identificamos en la conversación:", body)] + B([
    "<b>Datos que no siempre coinciden:</b> métricas de adherencia, registros repetidos y competencias canceladas que siguen en el plan.",
    "<b>Conexión limitada con TrainingPeaks,</b> plataforma cerrada que condiciona cómo fluye la información.",
    "<b>Planes por deporte con áreas de mejora,</b> sobre todo triatlón (transiciones bici-carrera y técnica de natación).",
    "<b>Seguimiento y ventas manuales:</b> muchos prospectos llegan, pocos se convierten sin intervención directa del equipo.",
    "<b>Necesidad de un mantenimiento predecible,</b> con costos transparentes."])

s += [P("2. Nuestra propuesta", h2),
      P("Entramos como el <b>equipo técnico de mantenimiento</b> de la plataforma que ya tienen: la entendemos, la protegemos, "
        "la estabilizamos y la mejoramos de forma gradual, siempre con su aprobación en cada paso.")]

s += [P("Fase 0 – Diagnóstico y arranque ordenado", h3),
      P("Revisamos cómo está construido el sistema antes de tocar nada.")] + B([
    "Inventario de herramientas, flujos, integraciones, servidores y accesos.",
    "Mapa de cómo viaja la información y <b>en qué puntos se pierde o se duplica</b>.",
    "Verificación de que el código, dominio, servidor y llaves estén a nombre de Youngstar, con respaldos.",
    "Transición coordinada con el equipo técnico actual (reunión y entrega de documentación).",
    "Evaluación de opciones para la conexión con TrainingPeaks.",
    "<b>Entregable:</b> informe, diagrama del sistema y lista priorizada de acciones. Es suyo, decidan o no continuar con nosotros."])

s += [P("Mantenimiento mensual", h3),
      P("Servicio continuo para que la plataforma siga viva y sana. Ofrecemos tres niveles de servicio "
        "(<b>Básico, Estándar y Plus</b>), que se distinguen por tiempos de respuesta, horas de mejoras incluidas y frecuencia de revisión con el doctor.")]
s += [tbl([
    ["Incluido", "Básico", "Estándar", "Plus"],
    ["Monitoreo de flujos, pagos y sincronizaciones", "Sí", "Sí", "Sí"],
    ["Alertas y corrección de errores", "Sí", "Sí", "Sí"],
    ["Respaldos y actualizaciones de seguridad", "Sí", "Sí", "Sí"],
    ["Reporte mensual (incidentes, consumo, métricas)", "Sí", "Sí", "Sí"],
    ["Horas mensuales de mejoras", "–", "Incluidas", "Ampliadas"],
    ["Atención en fines de semana", "–", "–", "Sí"],
    ["Revisión de planes con el doctor", "–", "Trimestral", "Mensual"],
], [7.2*cm, 3.2*cm, 3.2*cm, 3.2*cm])]
s += [Spacer(1, 4), P("Los costos variables (IA, servidor, APIs y mensajería) se muestran <b>a la vista y sin margen oculto</b>, con un tope mensual y aviso previo.", small)]

s += [P("Mejoras por proyecto (se aprueban una por una)", h3)]
s += [tbl([
    ["Mejora", "Qué resuelve"],
    ["Datos confiables", "Identificador único por atleta, sin duplicados, y fórmula de adherencia clara y correcta."],
    ["Competencias al día", "Mensaje de WhatsApp antes de cada carrera para confirmar asistencia y ajustar el plan automáticamente."],
    ["Calidad de entrenamiento", "Reglas por deporte (transiciones, natación, descargas) y panel del doctor para validar planes antes de publicarlos."],
    ["Seguimiento y ventas", "Agente de WhatsApp con memoria por atleta, escalamiento al doctor y clasificación de prospectos por interés."],
], [4.3*cm, 12.5*cm])]

s += [P("3. Principios con los que trabajamos", h2)] + B([
    "<b>Todo es suyo:</b> cuentas, accesos, código y documentación quedan a nombre de Youngstar.",
    "<b>Cambios seguros:</b> respaldo antes de modificar producción, pruebas y registro de cada cambio.",
    "<b>La salud primero:</b> la IA propone y el doctor decide; los síntomas se escalan siempre a una persona.",
    "<b>Sin ataduras:</b> contrato mensual con salida a 30 días y entrega completa de la información al terminar.",
    "<b>Confidencialidad:</b> firmamos un acuerdo de confidencialidad antes de acceder a cualquier sistema."])

s += [P("4. Qué incluye y qué no", h2),
      P("<b>Incluye:</b> monitoreo, corrección de errores, soporte técnico, respaldos, actualizaciones y reportes.<br/>"
        "<b>No incluye (se cotiza aparte):</b> funciones nuevas de gran alcance, rediseños, cambio de plataforma, atención directa a atletas y decisiones médicas.")]

s += [P("5. Siguientes pasos", h2)] + B([
    "Firma del acuerdo de confidencialidad.",
    "Reunión técnica con el equipo que desarrolló la plataforma y accesos de lectura.",
    "Arranque de la Fase 0 (1 a 2 semanas) y entrega del informe.",
    "Con el informe, definimos juntos el plan de mantenimiento y las mejoras prioritarias."])

s += [Spacer(1, 10), P("<b>Una nota importante:</b> la propuesta económica se compartirá por separado, una vez completado el diagnóstico inicial, "
                       "para ajustarla al sistema real y a lo que Youngstar necesite.", small), Spacer(1, 14),
      P("<b>[Nombre de la agencia]</b><br/>[Contacto] &nbsp;|&nbsp; [correo] &nbsp;|&nbsp; [teléfono]", body)]

doc = SimpleDocTemplate("docs/propuesta/Propuesta-Mantenimiento-Youngstar.pdf", pagesize=letter,
                        leftMargin=1.9*cm, rightMargin=1.9*cm, topMargin=1.7*cm, bottomMargin=1.8*cm,
                        title="Propuesta de mantenimiento - Youngstar Community", author="[Nombre de la agencia]")
doc.build(s, onFirstPage=footer, onLaterPages=footer)
