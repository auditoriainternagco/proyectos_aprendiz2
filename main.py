# -*- coding: utf-8 -*-
"""
Script principal para generar reportes de auditoría OTP por marca.
"""

import os
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # evita UnicodeEncodeError con emojis en consolas Windows
from pathlib import Path
from generador_html import renderizar_plantilla_alerta

DIR_BASE = Path(__file__).resolve().parent
DIR_OUTPUT = DIR_BASE / "output"
DIR_OUTPUT.mkdir(exist_ok=True)

# Por defecto: vista previa local (imágenes embebidas, requiere carpeta logos_png/).
# Con `python main.py --url`: logos desde GitHub (requiere haber subido logos_png/ al repo).
MODO_RECURSOS = "url" if "--url" in sys.argv else "base64"

# Datos de prueba simulados
MOCK_HALLAZGOS_RIFLE = [
    {
        "Nombre_Empleado": "Carlos Mendoza R.", "Cedula_Empleado": "1.020.455.890",
        "Cargo_Empleado": "Asesor Comercial", "Nombre_Tienda": "Rifle Unicentro",
        "Tipo_Contacto_Usado": "Tel. Asesor", "Dato_Contacto_Usado": "311 450 9988",
        "Nombre_Cliente_Suplantado": "Mariana Gómez V.", "Cedula_Cliente_Suplantado": "43.892.104",
        "Numero_Cliente": "300 219 4433"
    },
    {
        "Nombre_Empleado": "Andrea Ruiz P.", "Cedula_Empleado": "1.152.190.432",
        "Cargo_Empleado": "Cajera Principal", "Nombre_Tienda": "Rifle El Tesoro",
        "Tipo_Contacto_Usado": "Email Personal", "Dato_Contacto_Usado": "andrea.r@gmail.com",
        "Nombre_Cliente_Suplantado": "Felipe Castro O.", "Cedula_Cliente_Suplantado": "71.398.220",
        "Numero_Cliente": "314 882 1109"
    },
    {
        "Nombre_Empleado": "Jorge L. Henao", "Cedula_Empleado": "1.037.662.119",
        "Cargo_Empleado": "Asesor Comercial", "Nombre_Tienda": "Rifle Santafé",
        "Tipo_Contacto_Usado": "Tel. Asesor", "Dato_Contacto_Usado": "320 655 4321",
        "Nombre_Cliente_Suplantado": "Gloria Inés Duque", "Cedula_Cliente_Suplantado": "32.450.912",
        "Numero_Cliente": "310 994 2200"
    }
]

MOCK_HALLAZGOS_NAF_NAF = [
    {
        "Nombre_Empleado": "Maria Lopez", "Cedula_Empleado": "1.034.567.890",
        "Cargo_Empleado": "Asesora de Ventas", "Nombre_Tienda": "Naf Naf Tesoro",
        "Tipo_Contacto_Usado": "Celular", "Dato_Contacto_Usado": "300 123 4567",
        "Nombre_Cliente_Suplantado": "Andrea Gomez", "Cedula_Cliente_Suplantado": "43.219.876",
        "Numero_Cliente": "310 987 6543"
    }
]

MOCK_HALLAZGOS_AMERICANINO = []  # Para probar caso de Cero Hallazgos


def generar_reportes_prueba():
    casos = [
        ("RIFLE", MOCK_HALLAZGOS_RIFLE),
        ("NAF NAF", MOCK_HALLAZGOS_NAF_NAF),
        ("AMERICANINO", MOCK_HALLAZGOS_AMERICANINO),
    ]

    for marca, datos in casos:
        html = renderizar_plantilla_alerta(
            marca=marca,
            hallazgos=datos,
            periodo_inicio="28 de Septiembre de 2026",
            periodo_fin="05 de Octubre de 2026",
            modo_recursos=MODO_RECURSOS
        )

        nombre_archivo = f"reporte_otp_{marca.lower().replace(' ', '_')}.html"
        ruta_salida = DIR_OUTPUT / nombre_archivo

        with open(ruta_salida, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"✅ Reporte generado para {marca}: {ruta_salida}")


if __name__ == "__main__":
    generar_reportes_prueba()
