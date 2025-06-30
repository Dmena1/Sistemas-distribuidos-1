#!/usr/bin/env python3
"""
Script para verificar que los archivos de datos existan y tengan el formato correcto
"""

import os
import sys

def verificar_archivo(ruta, nombre):
    """Verifica que un archivo exista y tenga contenido"""
    if not os.path.exists(ruta):
        print(f"❌ ERROR: No se encuentra el archivo {nombre}: {ruta}")
        return False
    
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = f.read().strip()
            if not contenido:
                print(f"❌ ERROR: El archivo {nombre} está vacío: {ruta}")
                return False
            print(f"✅ OK: {nombre} encontrado con {len(contenido.splitlines())} líneas")
            return True
    except Exception as e:
        print(f"❌ ERROR: No se puede leer {nombre}: {e}")
        return False

def main():
    print("🔍 Verificando archivos de datos...")
    
    archivos = [
        ("data/conteo_por_comuna/part-r-00000", "Datos de conteo por comuna"),
        ("data/conteo_por_tipo/part-r-00000", "Datos de conteo por tipo"),
        ("eventos_region_metropolitana.json", "Eventos JSON"),
        ("eventos_limpios.csv", "Eventos CSV limpios"),
        ("eventos_convertidos.csv", "Eventos CSV convertidos")
    ]
    
    errores = 0
    for ruta, nombre in archivos:
        if not verificar_archivo(ruta, nombre):
            errores += 1
    
    print(f"\n📊 Resumen: {len(archivos) - errores}/{len(archivos)} archivos OK")
    
    if errores == 0:
        print("🎉 Todos los archivos están correctos!")
        return 0
    else:
        print(f"⚠️  {errores} archivos con problemas")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 