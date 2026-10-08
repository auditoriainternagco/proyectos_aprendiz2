# -*- coding: utf-8 -*-
"""
Configuración visual y de activos por marca de Grupo GCO.
Permite asociar a cada marca sus colores primarios, secundarios, bordes y logos oficiales.
"""

CONFIG_MARCAS = {
    "RIFLE": {
        "nombre_oficial": "Rifle",
        "logo_archivo": "rifle_U.svg",
        "banner_archivo": "banners_auditoria_rifle.png",
        "color_primario": "#2563eb",       # Azul corporativo Rifle
        "bg_header": "#111827",            # Fondo oscuro azulado/grafito
        "accent_badge": "#3b82f6",
        "border_color": "#1e3a8a",
    },
    "NAF NAF": {
        "nombre_oficial": "Naf Naf",
        "logo_archivo": "nafnaf_U.svg",
        "banner_archivo": "banners_auditoria_nafnaf.png",
        "color_primario": "#e11d48",       # Fucsia/rojo oscuro Naf Naf
        "bg_header": "#18181b",            # Zinc oscuro
        "accent_badge": "#f43f5e",
        "border_color": "#be123c",
    },
    "AMERICANINO": {
        "nombre_oficial": "Americanino",
        "logo_archivo": "americanino_G.svg",
        "banner_archivo": "banners_auditoria_americanino.png",
        "color_primario": "#d97706",       # Tono ocre/tierra Americanino
        "bg_header": "#1c1917",            # Piedra oscura
        "accent_badge": "#f59e0b",
        "border_color": "#b45309",
    },
    "CHEVIGNON": {
        "nombre_oficial": "Chevignon",
        "logo_archivo": "chevignon_G.svg",
        "banner_archivo": "banners_auditoria_chevignon.png",
        "color_primario": "#b91c1c",       # Rojo clásico Chevignon
        "bg_header": "#18181b",
        "accent_badge": "#ef4444",
        "border_color": "#991b1b",
    },
    "AMERICAN EAGLE": {
        "nombre_oficial": "American Eagle",
        "logo_archivo": "american_eagle_U.svg",
        "banner_archivo": "banners_auditoria_americaneagle.png",
        "color_primario": "#0284c7",       # Azul cielo American Eagle
        "bg_header": "#0f172a",
        "accent_badge": "#0ea5e9",
        "border_color": "#0369a1",
    },
    "ESPRIT": {
        "nombre_oficial": "Esprit",
        "logo_archivo": "esprit_G.svg",
        "banner_archivo": "banners_auditoria_esprit.png",
        "color_primario": "#dc2626",       # Rojo Esprit
        "bg_header": "#1f2937",
        "accent_badge": "#f87171",
        "border_color": "#b91c1c",
    },
    "MANGO": {
        "nombre_oficial": "Mango",
        "logo_archivo": "mango_U.svg",
        "banner_archivo": "banners_auditoria_mango.png",
        "color_primario": "#000000",       # Negro minimalista Mango
        "bg_header": "#111827",
        "accent_badge": "#4b5563",
        "border_color": "#374151",
    },
    "G-STAR": {
        "nombre_oficial": "G-Star Raw",
        "logo_archivo": "g_star_U.svg",
        "banner_archivo": "banners_auditoria_gstar.png",
        "color_primario": "#1e293b",
        "bg_header": "#0f172a",
        "accent_badge": "#64748b",
        "border_color": "#334155",
    },
    "BRANDSTORE": {
        "nombre_oficial": "Brandstore",
        "logo_archivo": "brandstore_G.svg",
        "banner_archivo": "banners_auditoria_brandstore.png",
        "color_primario": "#4f46e5",
        "bg_header": "#111827",
        "accent_badge": "#6366f1",
        "border_color": "#4338ca",
    },
    "AMERICAN BRANDS": {
        "nombre_oficial": "American Brands",
        "logo_archivo": "american_brands_U.png",
        "banner_archivo": "banners_auditoria_americanbrands.png",
        "color_primario": "#1e3a8a",
        "bg_header": "#0f172a",
        "accent_badge": "#3b82f6",
        "border_color": "#1e40af",
    },
    "VIVANT": {
        "nombre_oficial": "Vivant",
        "logo_archivo": "vivant_U.png",
        "banner_archivo": "banners_auditoria_vivant.png",
        "color_primario": "#0f766e",
        "bg_header": "#134e4a",
        "accent_badge": "#14b8a6",
        "border_color": "#0f766e",
    },
    "MOFT": {
        "nombre_oficial": "Moft",
        "logo_archivo": "moft_U.png",
        "banner_archivo": "banners_auditoria_moft.png",
        "color_primario": "#111827",
        "bg_header": "#111827",
        "accent_badge": "#4b5563",
        "border_color": "#374151",
    },
    "DEFAULT": {
        "nombre_oficial": "Grupo GCO",
        "logo_archivo": "rifle_U.svg",
        "banner_archivo": "banners_auditoria_rifle.png",
        "color_primario": "#2563eb",
        "bg_header": "#111827",
        "accent_badge": "#3b82f6",
        "border_color": "#1e3a8a",
    }
}

def obtener_config_marca(marca: str) -> dict:
    """Devuelve la configuración gráfica de la marca solicitada."""
    if not marca:
        return CONFIG_MARCAS["DEFAULT"]
    marca_normalizada = marca.strip().upper()
    return CONFIG_MARCAS.get(marca_normalizada, CONFIG_MARCAS["DEFAULT"])
