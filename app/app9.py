import openpyxl
import glob
import os
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# === CONFIGURACIÓN ===
# Carpeta donde están los Excel
CARPETA_EXCEL = "/home/tu_usuario/entrada"
CARPETA_SALIDA = "/home/tu_usuario/salida"


# Aseguramos que exista la carpeta de salida
os.makedirs(CARPETA_SALIDA, exist_ok=True)

# === FUNCIÓN PRINCIPAL ===
def procesar_excel(ruta_excel):
    print(f"Procesando: {ruta_excel}")
    wb = openpyxl.load_workbook(ruta_excel, data_only=True)
    
    # Accedemos a la hoja esperada (igual que Worksheets("web"))
    hoja = wb["web"]

    # === EJEMPLO DE LECTURA DE DATOS ===
    # Puedes extender esta parte con más celdas según tu VBA
    bono = [
        hoja["M11"].value,
        hoja["N11"].value,
        hoja["O11"].value,
        hoja["P11"].value,
        hoja["Q11"].value,
        hoja["R11"].value,
    ]

    fecha_actual = hoja["AX42"].value  # fecha en Excel
    if isinstance(fecha_actual, datetime):
        fecha_prev = fecha_actual - relativedelta(months=3)
    else:
        fecha_prev = None

    # === GENERAR TEXTO DE SALIDA ===
    header = (
        "mccf version: 1.0\n"
        "sender: Titulización de Activos\n"
        "phone: +34 917020808\n"
        "autorelease: replace\n"
    )

    texto = [header]
    texto.append(f"Fecha actual: {fecha_actual:%m/%d/%Y}" if fecha_actual else "Fecha no válida")
    texto.append(f"Fecha previa: {fecha_prev:%m/%d/%Y}" if fecha_prev else "")
    texto.append("Bonos:")

    for i, b in enumerate(bono, start=1):
        texto.append(f"  Bono {i}: {b}")

    salida = "\n".join(texto)

    # === GUARDAR EN TXT ===
    nombre_txt = os.path.splitext(os.path.basename(ruta_excel))[0] + ".txt"
    ruta_salida = os.path.join(CARPETA_SALIDA, nombre_txt)

    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(salida)

    print(f"Archivo generado: {ruta_salida}\n")


# === BUCLE PRINCIPAL ===
def main():
    # Busca todos los Excel en la carpeta (aunque haya solo uno)
    ficheros = glob.glob(os.path.join(CARPETA_EXCEL, "*.xlsx"))

    if not ficheros:
        print("No se encontraron ficheros Excel en la carpeta.")
        return

    for fichero in ficheros:
        procesar_excel(fichero)

    print("✅ Proceso completado.")


if __name__ == "__main__":
    main()
