# -*- coding: utf-8 -*-
"""
Convierte los logos SVG del repositorio auditoria_recursos_graficos (logos_marcas/principal)
a PNG con fondo transparente, usando Chrome/Edge headless.

Motivo: Gmail y Outlook no renderizan SVG en correos; PNG sí es compatible.

Uso:
    python generar_logos_png.py <ruta_a_logos_marcas/principal>

Salida: carpeta ./logos_png (subir al repo como logos_marcas/principal_png/).
"""
import re
import sys
import struct
import subprocess
import tempfile
from pathlib import Path

NAVEGADORES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
]
ANCHO_PX = 600  # resolución alta; en el HTML se muestra a ~140px (nítido en pantallas retina)
DIR_SALIDA = Path(__file__).resolve().parent / "logos_png"


def encontrar_navegador() -> str:
    for ruta in NAVEGADORES:
        if Path(ruta).exists():
            return ruta
    raise SystemExit("No se encontró Edge ni Chrome.")


def proporcion(svg_texto: str) -> float:
    m = re.search(r'viewBox="([\d.\s-]+)"', svg_texto)
    if m:
        _, _, w, h = [float(x) for x in m.group(1).split()]
        return h / w
    w = float(re.search(r'width="([\d.]+)"', svg_texto).group(1))
    h = float(re.search(r'height="([\d.]+)"', svg_texto).group(1))
    return h / w


def proporcion_avif(ruta: Path) -> float:
    """Lee ancho/alto del AVIF desde la caja 'ispe'."""
    datos = ruta.read_bytes()
    i = datos.find(b"ispe")
    w, h = struct.unpack(">II", datos[i + 8:i + 16])
    return h / w


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    origen = Path(sys.argv[1])
    DIR_SALIDA.mkdir(exist_ok=True)
    navegador = encontrar_navegador()

    archivos = sorted(list(origen.glob("*.svg")) + list(origen.glob("*.avif")))
    for svg in archivos:
        es_blanco = "white" in svg.name  # logos blancos: se oscurecen para verse sobre fondo claro
        if svg.suffix == ".avif":
            ratio = proporcion_avif(svg)
        else:
            ratio = proporcion(svg.read_text(encoding="utf-8"))
        alto = round(ANCHO_PX * ratio) + 2
        filtro = "filter:brightness(0);" if es_blanco else ""
        nombre_salida = svg.stem.replace("_white", "") + ".png"
        with tempfile.TemporaryDirectory() as tmp:
            html = Path(tmp) / "x.html"
            html.write_text(
                f'<html><body style="margin:0;background:transparent">'
                f'<img src="{svg.resolve().as_uri()}" style="width:{ANCHO_PX}px;height:{alto - 2}px;display:block;{filtro}"></body></html>',
                encoding="utf-8",
            )
            destino = DIR_SALIDA / nombre_salida
            subprocess.run([
                navegador, "--headless", "--disable-gpu", "--hide-scrollbars",
                "--default-background-color=00000000",
                f"--window-size={ANCHO_PX},{alto}",
                f"--screenshot={destino}", html.as_uri(),
            ], capture_output=True, timeout=60)
        print(("OK  " if destino.exists() else "FALLO ") + destino.name)


if __name__ == "__main__":
    main()
