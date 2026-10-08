# -*- coding: utf-8 -*-
"""
Script de Envío de Pruebas Reales por SMTP Office 365
Destinatario ÚNICO: aprendiz.auditoriainterna2@gco.com.co
"""

import sys
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from config_marcas import CONFIG_MARCAS
from generador_html import renderizar_plantilla_alerta
import main

CORREO_ORIGEN = "auditoria.interna@gco.com.co"
CORREO_CONTRASENA = "Colombia.24*"
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587

CORREO_DESTINO_UNICO = "aprendiz.auditoriainterna2@gco.com.co"

# Lista de todas las marcas configuradas (12 marcas)
MARCAS = [k for k in CONFIG_MARCAS.keys() if k != "DEFAULT"]

def obtener_datos_ejemplo(marca):
    # Algunos con alertas y otros sin alertas para ver ambos estados
    if marca in ["RIFLE", "CHEVIGNON", "ESPRIT"]:
        return main.MOCK_HALLAZGOS_RIFLE
    elif marca in ["NAF NAF", "AMERICAN EAGLE", "G-STAR", "VIVANT"]:
        return main.MOCK_HALLAZGOS_NAF_NAF
    else:
        return []  # 0 hallazgos para ver tarjeta verde

def enviar_pruebas():
    print(f"Iniciando conexión SMTP con {SMTP_SERVER}:{SMTP_PORT}...")
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=20)
        server.starttls()
        server.login(CORREO_ORIGEN, CORREO_CONTRASENA)
        print("Autenticación SMTP exitosa con Office 365.\n")
    except Exception as e:
        print(f"Error de autenticación SMTP: {e}")
        return

    for i, marca in enumerate(MARCAS, 1):
        datos = obtener_datos_ejemplo(marca)
        total = len(datos)
        asunto = f"[PRUEBA {i}/{len(MARCAS)}] Reporte OTP - {marca} ({total} Alerta(s))"
        html = renderizar_plantilla_alerta(
            marca=marca,
            hallazgos=datos,
            modo_recursos="url"
        )

        msg = MIMEMultipart("alternative")
        msg["From"] = f"Auditoría Interna GCO <{CORREO_ORIGEN}>"
        msg["To"] = CORREO_DESTINO_UNICO
        msg["Subject"] = asunto

        msg.attach(MIMEText(html, "html", "utf-8"))

        try:
            server.sendmail(CORREO_ORIGEN, [CORREO_DESTINO_UNICO], msg.as_string())
            print(f"[{i}/{len(MARCAS)}] Enviado con éxito: {marca} -> {CORREO_DESTINO_UNICO}")
            time.sleep(1.5)  # Breve pausa para no saturar el conector SMTP
        except Exception as err:
            print(f"[{i}/{len(MARCAS)}] Error enviando {marca}: {err}")

    server.quit()
    print("\nProceso de envío de pruebas finalizado con éxito.")

if __name__ == "__main__":
    enviar_pruebas()

