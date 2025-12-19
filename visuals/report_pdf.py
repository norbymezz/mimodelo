# visuals/report_pdf.py
# Generador profesional de reportes PDF para la app multiwell SPE-215031

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import utils
import datetime

styles = getSampleStyleSheet()
title_style = styles["Title"]
h1 = styles["Heading1"]
h2 = styles["Heading2"]
body = styles["BodyText"]

def _img(path, width=450):
    try:
        img = utils.ImageReader(path)
        iw, ih = img.getSize()
        aspect = ih / float(iw)
        return Image(path, width=width, height=width * aspect)
    except:
        p = Paragraph(f"[ERROR: no se pudo cargar {path}]", body)
        return p

def build_pdf(
    filename,
    params,
    geometry_info,
    schedule_info,
    figures,
    regimes,
    notes=None
):
    """
    filename: destino del PDF
    params: dict con parámetros de entrada
    geometry_info: dict con info de geometría
    schedule_info: dict con schedules por pozo
    figures: dict con paths a:
        "plan"
        "pwf"
        "dp"
        "dp12"
        "kernel"
        "slope_well_i"
        "interference"
    regimes: dict con regímenes detectados por pozo
    notes: texto opcional adicional
    """

    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=40, leftMargin=40,
        topMargin=40, bottomMargin=40
    )

    story = []

    # ----------------- PORTADA -----------------
    story.append(Paragraph("Reporte Multiwell SPE-215031 (Modelo Ozkan)", title_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Fecha: {datetime.datetime.now():%Y-%m-%d %H:%M}", body))
    story.append(Spacer(1, 20))

    story.append(Paragraph("Este informe incluye parámetros, geometría, schedules, resultados y diagnóstico experto de regímenes.", body))
    story.append(PageBreak())

    # ----------------- PARÁMETROS -----------------
    story.append(Paragraph("1. Parámetros de Fluido y Roca", h1))
    for k, v in params.items():
        story.append(Paragraph(f"<b>{k}</b>: {v}", body))
    story.append(PageBreak())

    # ----------------- GEOMETRÍA -----------------
    story.append(Paragraph("2. Geometría", h1))
    for k, v in geometry_info.items():
        story.append(Paragraph(f"<b>{k}</b>: {v}", body))

    if "plan" in figures:
        story.append(Spacer(1, 12))
        story.append(_img(figures["plan"]))
    story.append(PageBreak())

    # ----------------- SCHEDULES -----------------
    story.append(Paragraph("3. Schedules (q(t))", h1))
    for well, sched in schedule_info.items():
        story.append(Paragraph(f"<b>{well}</b>: {sched}", body))
    story.append(PageBreak())

    # ----------------- FIGURAS PRINCIPALES -----------------
    story.append(Paragraph("4. Resultados Principales", h1))

    if "pwf" in figures:
        story.append(Paragraph("Presiones Pwf(t)", h2))
        story.append(_img(figures["pwf"]))
        story.append(Spacer(1, 12))

    if "dp" in figures:
        story.append(Paragraph("ΔP_res(t)", h2))
        story.append(_img(figures["dp"]))
        story.append(Spacer(1, 12))

    if "dp12" in figures:
        story.append(Paragraph("ΔP_ij(t)", h2))
        story.append(_img(figures["dp12"]))
        story.append(Spacer(1, 12))

    story.append(PageBreak())

    # ----------------- DIAGNÓSTICO AVANZADO -----------------
    story.append(Paragraph("5. Diagnóstico Avanzado", h1))

    if "kernel" in figures:
        story.append(Paragraph("Kernel R(s)", h2))
        story.append(_img(figures["kernel"]))
        story.append(Spacer(1, 12))

    if "interference" in figures:
        story.append(Paragraph("Mapa de Interferencia", h2))
        story.append(_img(figures["interference"]))
        story.append(Spacer(1, 12))

    # Slopes
    for key, path in figures.items():
        if key.startswith("slope_"):
            story.append(Paragraph(f"Pendiente log-log: {key}", h2))
            story.append(_img(path))
            story.append(Spacer(1, 12))

    story.append(PageBreak())

    # ----------------- REGÍMENES -----------------
    story.append(Paragraph("6. Regímenes Detectados", h1))
    for well, reglist in regimes.items():
        story.append(Paragraph(f"<b>{well}</b>", h2))
        for name, t0, t1 in reglist:
            story.append(Paragraph(f"- {name}: {t0:.3g} — {t1:.3g} días", body))
    story.append(PageBreak())

    # ----------------- NOTAS FINALES -----------------
    story.append(Paragraph("7. Notas / Observaciones", h1))
    if notes:
        story.append(Paragraph(notes, body))
    else:
        story.append(Paragraph("Sin notas adicionales.", body))

    story.append(Spacer(1, 20))
    story.append(Paragraph("Reporte generado automáticamente por la app Multiwell basada en SPE-215031.", body))

    doc.build(story)
