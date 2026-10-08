# -*- coding: utf-8 -*-
"""
Script: alerta_correo_otp.py
Ubicación: Datos_Personales/alerta_correo_otp.py
Descripción: Reporte automatizado de Auditoría OTP con correos independientes por marca,
aprovechando el módulo centralizado de notificaciones de Office 365.

Adaptación: el HTML ahora se genera con la plantilla corporativa (generador_html.py +
config_marcas.py) y los logos se leen desde el repositorio de GitHub
auditoria_recursos_graficos (logos_marcas/principal).
"""
import os
import sys
import logging
from datetime import datetime, timedelta

# Forzar ruta absoluta a la raíz del proyecto para encontrar notificaciones.py
sys.path.insert(0, '/home/etl_auditoria/auditoria-python')
# Asegurar que se encuentren generador_html.py y config_marcas.py (misma carpeta)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pyodbc
import pandas as pd
# 'notificaciones' se importa solo si se ejecuta con --enviar (ver bloque principal)
from generador_html import renderizar_plantilla_alerta

OS_LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(OS_LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(OS_LOG_DIR, "alerta_correo_otp.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("AlertaCorreoOTP")

CORREOS_DESTINO = ["aprendiz.auditoriainterna2@gco.com.co"]
MARCAS_OBJETIVO = ["Naf Naf", "Rifle"]

MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
         "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]


def formatear_fecha(fecha: datetime) -> str:
    return f"{fecha.day:02d} de {MESES[fecha.month - 1]} de {fecha.year}"


def consultar_alertas_semanales():
    user_sql = 'etl_auditoria'
    pass_sql = 'AuditoriaInterna'
    conexion_str = (
        f'DRIVER={{ODBC Driver 18 for SQL Server}};'
        f'SERVER=sersqldwcorp;'
        f'DATABASE=DW;'
        f'UID={user_sql};'
        f'PWD={pass_sql};'
        f'TrustServerCertificate=yes;'
    )
    logger.info("Consultando alertas de Naf Naf y Rifle en SQL Server...")
    try:
        conn = pyodbc.connect(conexion_str)
        query = """
        SELECT
            CONVERT(VARCHAR(10), Fecha_OTP, 103) AS Fecha_OTP,
            Nombre_Empleado,
            Cedula_Empleado,
            Cargo_Empleado,
            Nombre_Tienda,
            Marca,
            Tipo_Contacto_Usado,
            Dato_Contacto_Usado,
            Nombre_Cliente_Suplantado,
            Cedula_Cliente_Suplantado,
            Numero_Cliente,
            ISNULL(Correo_Cliente, 'NO REGISTRA') AS Correo_Cliente
        FROM [gc_auditoria].[auditoria_datos_personales]
        WHERE Fecha_OTP >= DATEADD(DAY, -7, GETDATE())
          AND LTRIM(RTRIM(Marca)) IN ('Naf Naf', 'NAF NAF', 'Rifle', 'RIFLE')
        ORDER BY Marca, Fecha_OTP DESC;
        """
        df = pd.read_sql(query, conn)
        conn.close()
        logger.info(f"Consulta completada. Registros totales encontrados: {len(df)}")
        return df
    except Exception as e:
        logger.error(f"Error consultando SQL Server: {e}")
        raise


def generar_html_por_marca(df_marca, nombre_marca, periodo_inicio, periodo_fin):
    """Genera el HTML con la plantilla corporativa; los logos se cargan desde GitHub."""
    hallazgos = df_marca.to_dict(orient="records") if len(df_marca) > 0 else []
    return renderizar_plantilla_alerta(
        marca=nombre_marca,
        hallazgos=hallazgos,
        periodo_inicio=periodo_inicio,
        periodo_fin=periodo_fin,
        modo_recursos="base64" if "--local" in sys.argv else "url",
    )


def datos_mock():
    """Datos simulados para probar sin conexión a SQL Server."""
    return pd.DataFrame([
        {"Fecha_OTP": "05/10/2026", "Nombre_Empleado": "Carlos Mendoza R.", "Cedula_Empleado": "1.020.455.890",
         "Cargo_Empleado": "Asesor Comercial", "Nombre_Tienda": "Rifle Unicentro", "Marca": "Rifle",
         "Tipo_Contacto_Usado": "Tel. Asesor", "Dato_Contacto_Usado": "311 450 9988",
         "Nombre_Cliente_Suplantado": "Mariana Gómez V.", "Cedula_Cliente_Suplantado": "43.892.104",
         "Numero_Cliente": "300 219 4433", "Correo_Cliente": "NO REGISTRA"},
        {"Fecha_OTP": "04/10/2026", "Nombre_Empleado": "Maria Lopez", "Cedula_Empleado": "1.034.567.890",
         "Cargo_Empleado": "Asesora de Ventas", "Nombre_Tienda": "Naf Naf Tesoro", "Marca": "Naf Naf",
         "Tipo_Contacto_Usado": "Celular", "Dato_Contacto_Usado": "300 123 4567",
         "Nombre_Cliente_Suplantado": "Andrea Gomez", "Cedula_Cliente_Suplantado": "43.219.876",
         "Numero_Cliente": "310 987 6543", "Correo_Cliente": "NO REGISTRA"},
    ])


if __name__ == "__main__":
    # MODO PRUEBA POR DEFECTO: no se envía ningún correo.
    #   python alerta_correo_otp.py            -> consulta SQL y guarda HTML en output/
    #   python alerta_correo_otp.py --mock     -> datos simulados (sin SQL) y guarda HTML
    #   python alerta_correo_otp.py --enviar   -> ENVÍA correos (solo cuando se autorice)
    ENVIAR = "--enviar" in sys.argv
    USAR_MOCK = "--mock" in sys.argv
    DIR_OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(DIR_OUTPUT, exist_ok=True)

    logger.info(f"=== INICIO DEL PROCESO DE ALERTAMIENTO | envío={'SÍ' if ENVIAR else 'NO (modo prueba)'} ===")
    try:
        df_completo = datos_mock() if USAR_MOCK else consultar_alertas_semanales()
        notifier = None
        if ENVIAR:
            from notificaciones import notificaciones
            notifier = notificaciones()

        hoy = datetime.now()
        periodo_inicio = formatear_fecha(hoy - timedelta(days=7))
        periodo_fin = formatear_fecha(hoy)

        for marca in MARCAS_OBJETIVO:
            df_submarca = (
                df_completo[df_completo['Marca'].str.strip().str.upper() == marca.upper()]
                if not df_completo.empty else pd.DataFrame()
            )
            asunto_marca = f"🚨 [AUDITORÍA INTERNA] Reporte OTP - {marca} ({len(df_submarca)} Alerta(s))"
            html_marca = generar_html_por_marca(df_submarca, marca, periodo_inicio, periodo_fin)

            if ENVIAR:
                notifier.notificacion_correo(
                    asunto=asunto_marca,
                    cuerpo_correo=html_marca,
                    intentos=2,
                    espera_segundos=5
                )
            else:
                ruta = os.path.join(DIR_OUTPUT, f"reporte_otp_{marca.lower().replace(' ', '_')}.html")
                with open(ruta, "w", encoding="utf-8") as f:
                    f.write(html_marca)
                logger.info(f"[PRUEBA] HTML guardado (sin enviar): {ruta} | Asunto: {asunto_marca}")
        logger.info("=== CORREOS ENVIADOS ===" if ENVIAR else "=== PRUEBA FINALIZADA: NO SE ENVIÓ NINGÚN CORREO ===")
    except Exception as error:
        logger.critical(f"El proceso falló: {error}")
