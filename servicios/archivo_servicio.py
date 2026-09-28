import json
from pathlib import Path


class ArchivoServicio:
    @staticmethod
    def obtener_ruta(nombre_archivo):
        return Path(__file__).resolve().parent.parent / "datos" / nombre_archivo

    @staticmethod
    def leer_json(nombre_archivo):
        ruta = ArchivoServicio.obtener_ruta(nombre_archivo)
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def guardar_json(nombre_archivo, datos):
        ruta = ArchivoServicio.obtener_ruta(nombre_archivo)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
