# -*- coding: utf-8 -*-
"""
Generador de plantillas HTML para Alertas de Auditoría Digital GCO.
Basado en el diseño corporativo de studio_pantilla.html.

Versión COMPATIBLE CON CLIENTES DE CORREO (Outlook, Gmail, móviles):
  - Maquetación con tablas y estilos 100% inline (sin Tailwind/CDN, sin <script>, sin filtros CSS).
  - Logos en PNG (los SVG no se renderizan en Gmail/Outlook).
  - Colores sólidos con 'bgcolor' como respaldo de los degradados.
"""

import base64
import struct
from html import escape
from pathlib import Path
from config_marcas import obtener_config_marca

DIR_BASE = Path(__file__).resolve().parent
DIR_ASSETS = DIR_BASE / "assets"
DIR_LOGOS = DIR_BASE / "logos_png"        # logos individuales
DIR_BANNERS = DIR_BASE / "banners_png"    # banners completos con fondo blanco
DIR_IMG = DIR_ASSETS / "img"

# Repositorio de recursos gráficos (GitHub).
URL_REPOSITORIO_GITLAB = "https://raw.githubusercontent.com/auditoriainternagco/auditoria_recursos_graficos/main"
RUTA_LOGOS_REMOTA = "logos_marcas/principal_png"
RUTA_BANNERS_REMOTA = "imagenes_banner"

FUENTE = "Arial, Helvetica, sans-serif"


def _a_png(nombre_archivo: str) -> str:
    """El config referencia el .svg original; para correo se usa su versión .png."""
    return Path(nombre_archivo).stem + ".png"


def cargar_imagen(nombre_archivo: str, tipo="img", modo="base64") -> str:
    """
    Carga un recurso gráfico.
    Modos disponibles:
      - 'url': URL pública del repositorio de GitHub (modo para producción/correo real).
      - 'base64': Embebe la imagen en el HTML.
      - 'local': Ruta del archivo en el sistema de archivos.
    """
    if tipo == "logos":
        nombre_archivo = _a_png(nombre_archivo)

    if modo == "url":
        if tipo == "banners":
            return f"{URL_REPOSITORIO_GITLAB}/{RUTA_BANNERS_REMOTA}/{nombre_archivo}"
        elif tipo == "logos":
            return f"{URL_REPOSITORIO_GITLAB}/{RUTA_LOGOS_REMOTA}/{nombre_archivo}"
        return f"{URL_REPOSITORIO_GITLAB}/{nombre_archivo}"

    if tipo == "banners":
        carpeta_path = DIR_BANNERS
    elif tipo == "logos":
        carpeta_path = DIR_LOGOS
    else:
        carpeta_path = DIR_IMG

    archivo_path = carpeta_path / nombre_archivo

    if not archivo_path.exists():
        return ""

    if modo == "local":
        return str(archivo_path)

    ext = archivo_path.suffix.lower().replace(".", "")
    mime_type = "image/jpeg" if ext == "jpg" else f"image/{ext}"
    with open(archivo_path, "rb") as f:
        datos_base64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime_type};base64,{datos_base64}"


def _ancho_logo(nombre_archivo: str, alto_objetivo: int = 30, ancho_max: int = 140, ancho_defecto: int = 120) -> int:
    """
    Ancho (px) con el que se muestra el logo de marca para que todos se vean parejos:
    alto aproximado de 'alto_objetivo' px, sin pasar de 'ancho_max'. Lee la proporción del PNG local.
    """
    ruta = DIR_LOGOS / _a_png(nombre_archivo)
    try:
        with open(ruta, "rb") as f:
            cabecera = f.read(24)
        ancho, alto = struct.unpack(">II", cabecera[16:24])
        return max(50, min(ancho_max, round(alto_objetivo * ancho / alto)))
    except Exception:
        return ancho_defecto


def _t(valor) -> str:
    """Texto seguro para HTML."""
    return escape(str(valor if valor is not None else ""))


def renderizar_plantilla_alerta(
    marca: str,
    hallazgos: list,
    periodo_inicio: str = "28 de Septiembre de 2026",
    periodo_fin: str = "05 de Octubre de 2026",
    modo_recursos: str = "url",
    link_gestion: str = "#gestionar-casos"
) -> str:
    """
    Genera el HTML completo del reporte de alertas para una marca dada.
    """
    config = obtener_config_marca(marca)
    total_alertas = len(hallazgos)
    nombre = _t(config["nombre_oficial"])

    banner_nombre = config.get("banner_archivo", f"banners_auditoria_{marca.lower().replace(' ', '').replace('-', '')}.png")
    banner_src = cargar_imagen(banner_nombre, tipo="banners", modo=modo_recursos)
    logo_gco_src = cargar_imagen("logo_gco.png", tipo="img", modo=modo_recursos)

    # ---- Estado de alertas (header) ----
    if total_alertas > 0:
        badge_estado_html = f"""
        <span style="display:inline-block;padding:6px 14px;border-radius:16px;background-color:#7f1d1d;border:1px solid #ef4444;color:#fecaca;font-size:12px;font-weight:bold;font-family:{FUENTE};">&#9679;&nbsp;{total_alertas} Alerta(s) activa(s)</span>
        <span style="font-size:11px;color:#94a3b8;font-family:{FUENTE};">&nbsp;&nbsp;Prioridad Alta &bull; Acci&oacute;n Requerida</span>"""
        badge_tabla = f"""<span style="display:inline-block;padding:2px 8px;border-radius:10px;background-color:#fef3c7;border:1px solid #fde68a;color:#92400e;font-size:11px;font-weight:bold;font-family:{FUENTE};">{total_alertas} Registro(s)</span>"""
    else:
        badge_estado_html = f"""
        <span style="display:inline-block;padding:6px 14px;border-radius:16px;background-color:#064e3b;border:1px solid #10b981;color:#a7f3d0;font-size:12px;font-weight:bold;font-family:{FUENTE};">&#9679;&nbsp;0 Alertas activas</span>
        <span style="font-size:11px;color:#6ee7b7;font-family:{FUENTE};">&nbsp;&nbsp;Sin Novedades &bull; Operaci&oacute;n Normal</span>"""
        badge_tabla = f"""<span style="display:inline-block;padding:2px 8px;border-radius:10px;background-color:#d1fae5;border:1px solid #a7f3d0;color:#065f46;font-size:11px;font-weight:bold;font-family:{FUENTE};">0 Registros</span>"""

    # ---- Sección de datos ----
    if total_alertas == 0:
        contenido_seccion_datos = f"""
        <table width="100%" cellpadding="0" cellspacing="0" border="0" role="presentation">
          <tr><td align="center" bgcolor="#ecfdf5" style="background-color:#ecfdf5;border:1px solid #a7f3d0;border-radius:12px;padding:30px 24px;font-family:{FUENTE};">
            <div style="font-size:26px;line-height:30px;color:#059669;font-weight:bold;">&#10003;</div>
            <div style="font-size:16px;font-weight:bold;color:#064e3b;padding-top:8px;">&iexcl;Excelente noticia! Sin inconsistencias detectadas</div>
            <div style="font-size:13px;color:#047857;line-height:1.6;padding-top:8px;">
              No se registraron alertas ni novedades de suplantaci&oacute;n en validaciones OTP para la marca <strong>{nombre}</strong> durante el ciclo evaluado ({_t(periodo_inicio)} &mdash; {_t(periodo_fin)}).
            </div>
          </td></tr>
        </table>"""
    else:
        estilo_td = f"padding:9px 8px;font-size:11px;font-family:{FUENTE};vertical-align:top;border-bottom:1px solid #e2e8f0;"
        filas_html = ""
        for i, h in enumerate(hallazgos):
            bg = "#f8fafc" if i % 2 == 1 else "#ffffff"
            tipo_contacto = h.get("Tipo_Contacto_Usado", "")
            detalle_contacto = f"({_t(tipo_contacto)})" if tipo_contacto else ""
            filas_html += f"""
            <tr bgcolor="{bg}" style="background-color:{bg};">
              <td style="{estilo_td}color:#0f172a;font-weight:bold;">{_t(h.get('Nombre_Empleado'))}</td>
              <td style="{estilo_td}color:#475569;">{_t(h.get('Cedula_Empleado'))}</td>
              <td style="{estilo_td}color:#475569;">{_t(h.get('Cargo_Empleado'))}</td>
              <td style="{estilo_td}color:#1e293b;">{_t(h.get('Nombre_Tienda'))}</td>
              <td bgcolor="#fff1f2" style="{estilo_td}background-color:#fff1f2;color:#be123c;font-weight:bold;">{_t(h.get('Dato_Contacto_Usado'))}<br><span style="font-size:10px;font-weight:normal;color:#e11d48;">{detalle_contacto}</span></td>
              <td style="{estilo_td}color:#0f172a;font-weight:bold;">{_t(h.get('Nombre_Cliente_Suplantado'))}</td>
              <td style="{estilo_td}color:#475569;">{_t(h.get('Cedula_Cliente_Suplantado'))}</td>
              <td style="{estilo_td}color:#64748b;">{_t(h.get('Numero_Cliente'))}</td>
            </tr>"""

        th = f"padding:10px 8px;font-size:10px;font-family:{FUENTE};text-align:left;text-transform:uppercase;letter-spacing:0.4px;color:#334155;border-bottom:1px solid #cbd5e1;"
        contenido_seccion_datos = f"""
        <table width="100%" cellpadding="0" cellspacing="0" border="0" role="presentation">
          <tr>
            <td style="font-family:{FUENTE};font-size:13px;font-weight:bold;color:#1e293b;text-transform:uppercase;letter-spacing:0.5px;padding-bottom:10px;">Detalle de Hallazgos Transaccionales</td>
            <td align="right" style="padding-bottom:10px;">{badge_tabla}</td>
          </tr>
          <tr><td colspan="2">
            <div style="overflow-x:auto;-webkit-overflow-scrolling:touch;">
             <table width="100%" cellpadding="0" cellspacing="0" border="0" style="min-width:620px;border:1px solid #e2e8f0;border-collapse:separate;border-radius:8px;">
              <thead>
                <tr bgcolor="#f1f5f9" style="background-color:#f1f5f9;">
                  <th style="{th}" width="15%">Nombre Empleado</th>
                  <th style="{th}" width="10%">C&eacute;dula Emp.</th>
                  <th style="{th}" width="12%">Cargo</th>
                  <th style="{th}" width="13%">Tienda</th>
                  <th bgcolor="#ffe4e6" style="{th}background-color:#ffe4e6;color:#9f1239;" width="13%">&#9888; Contacto Usado</th>
                  <th style="{th}" width="15%">Cliente Suplantado</th>
                  <th style="{th}" width="10%">C&eacute;dula Cliente</th>
                  <th style="{th}" width="12%">Contacto Cliente</th>
                </tr>
              </thead>
              <tbody>{filas_html}
              </tbody>
            </table>
            </div>
          </td></tr>
          <tr><td colspan="2" style="padding-top:10px;font-family:{FUENTE};font-size:11px;color:#64748b;line-height:1.5;">
            <strong>Contacto Usado:</strong> N&uacute;mero de tel&eacute;fono celular o direcci&oacute;n de correo electr&oacute;nico identificada durante la emisi&oacute;n del token OTP en la pasarela de punto de venta.
          </td></tr>
        </table>"""

    return f"""<!DOCTYPE html>
<html lang="es" xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<title>Reporte OTP - Auditor&iacute;a Digital GCO - {nombre}</title>
</head>
<body style="margin:0;padding:0;background-color:#f1f5f9;">
<table width="100%" cellpadding="0" cellspacing="0" border="0" role="presentation" bgcolor="#f1f5f9" style="background-color:#f1f5f9;">
<tr><td align="center" style="padding:24px 10px;">

  <!-- CONTENEDOR PRINCIPAL -->
  <table width="760" cellpadding="0" cellspacing="0" border="0" role="presentation" style="width:100%;max-width:760px;background-color:#ffffff;border:1px solid #e2e8f0;border-radius:14px;">

    <!-- HEADER DE MARCA -->
    <tr><td bgcolor="{config['bg_header']}" style="background-color:{config['bg_header']};padding:20px 24px;border-radius:14px 14px 0 0;">
      <table width="100%" cellpadding="0" cellspacing="0" border="0" role="presentation">
        <tr><td align="center">
          <img src="{banner_src}" alt="Auditor&iacute;a Digital GCO - {nombre}" width="700" style="display:block;width:100%;max-width:700px;height:auto;border:0;border-radius:10px;background-color:#ffffff;">
        </td></tr>
        <tr><td align="center" style="padding-top:16px;">{badge_estado_html}</td></tr>
      </table>
    </td></tr>

    <!-- CUERPO -->
    <tr><td style="padding:28px;">

      <div style="font-family:{FUENTE};font-size:11px;font-weight:bold;text-transform:uppercase;letter-spacing:0.8px;color:#1d4ed8;">&#9432; Notificaci&oacute;n Oficial de Auditor&iacute;a</div>
      <h1 style="margin:6px 0 18px 0;font-family:{FUENTE};font-size:22px;line-height:1.25;font-weight:bold;color:#0f172a;">Reporte OTP - Inconsistencias y Suplantaciones</h1>

      <!-- Tarjeta informativa -->
      <table width="100%" cellpadding="0" cellspacing="0" border="0" role="presentation">
        <tr><td bgcolor="#f1f5f9" style="background-color:#f1f5f9;border:1px solid #e2e8f0;border-radius:12px;padding:18px;font-family:{FUENTE};font-size:13.5px;color:#334155;line-height:1.6;">
          <p style="margin:0 0 10px 0;">Estimado equipo comercial,</p>
          <p style="margin:0 0 14px 0;">A trav&eacute;s del monitoreo continuo de los sistemas transaccionales y el protocolo de validaci&oacute;n de identidad por C&oacute;digo OTP en puntos de venta, el equipo de <strong>Auditor&iacute;a Digital GCO</strong> ha generado el reporte semanal correspondiente al ciclo evaluado:</p>
          <table width="100%" cellpadding="0" cellspacing="0" border="0" role="presentation">
            <tr><td bgcolor="#ffffff" style="background-color:#ffffff;border:1px solid #e2e8f0;border-radius:8px;padding:10px 14px;font-family:{FUENTE};">
              <div style="font-size:12px;font-weight:bold;color:#0f172a;">&#128197; Per&iacute;odo de Monitoreo Analizado:</div>
              <div style="font-size:12px;color:#475569;padding-top:2px;">{_t(periodo_inicio)} &mdash; {_t(periodo_fin)}</div>
            </td></tr>
          </table>
        </td></tr>
      </table>

      <div style="height:22px;line-height:22px;">&nbsp;</div>

      <!-- TABLA O MENSAJE DE CERO NOVEDADES -->
      {contenido_seccion_datos}

      <div style="height:22px;line-height:22px;">&nbsp;</div>

      <!-- RECOMENDACIÓN Y GESTIÓN -->
      <table width="100%" cellpadding="0" cellspacing="0" border="0" role="presentation">
        <tr><td bgcolor="#f1f5f9" style="background-color:#f1f5f9;border:1px solid #e2e8f0;border-radius:12px;padding:16px;">
          <table width="100%" cellpadding="0" cellspacing="0" border="0" role="presentation">
            <tr>
              <td valign="middle" style="font-family:{FUENTE};">
                <div style="font-size:12px;font-weight:bold;color:#1e293b;text-transform:uppercase;letter-spacing:0.6px;">Recomendaci&oacute;n</div>
                <div style="font-size:12px;color:#475569;line-height:1.6;padding-top:4px;">Validar con los equipos comerciales la causa de esta novedad. En caso de ser reincidente, escalar el caso a talento humano.</div>
              </td>
              <td valign="middle" align="right" style="padding-left:16px;">
                <a href="{link_gestion}" style="display:inline-block;padding:10px 20px;border-radius:20px;background-color:#1e3a8a;color:#f1f8ff;font-family:{FUENTE};font-size:12px;font-weight:bold;text-decoration:none;white-space:nowrap;">Gestionar Casos &rarr;</a>
              </td>
            </tr>
          </table>
        </td></tr>
      </table>

    </td></tr>

    <!-- LÍNEA INSTITUCIONAL 4 COLORES -->
    <tr><td style="font-size:0;line-height:0;">
      <table width="100%" cellpadding="0" cellspacing="0" border="0" role="presentation"><tr>
        <td width="25%" height="4" bgcolor="#2b509e" style="height:4px;font-size:0;line-height:0;">&nbsp;</td>
        <td width="25%" height="4" bgcolor="#f5a623" style="height:4px;font-size:0;line-height:0;">&nbsp;</td>
        <td width="25%" height="4" bgcolor="#a3d93b" style="height:4px;font-size:0;line-height:0;">&nbsp;</td>
        <td width="25%" height="4" bgcolor="#f25d69" style="height:4px;font-size:0;line-height:0;">&nbsp;</td>
      </tr></table>
    </td></tr>

    <!-- FOOTER CORPORATIVO -->
    <tr><td bgcolor="#f8fafc" style="background-color:#f8fafc;padding:20px 28px;border-radius:0 0 14px 14px;">
      <table width="100%" cellpadding="0" cellspacing="0" border="0" role="presentation">
        <tr>
          <td valign="middle" style="font-family:{FUENTE};">
            <img src="{logo_gco_src}" alt="GCO" height="28" style="height:28px;width:auto;border:0;vertical-align:middle;">
            <span style="font-size:11px;color:#475569;padding-left:10px;vertical-align:middle;">Auditor&iacute;a Interna Corporativa</span>
          </td>
          <td align="right" valign="middle" style="font-family:{FUENTE};font-size:12px;color:#475569;">
            Mesa de Ayuda Auditor&iacute;a:
            <a href="mailto:auditoria.interna@gco.com.co" style="color:#1e3a8a;font-weight:bold;text-decoration:none;">auditoria.interna@gco.com.co</a>
          </td>
        </tr>
      </table>
    </td></tr>

  </table>

</td></tr>
</table>
</body>
</html>
"""
