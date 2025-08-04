import os
import re
import pandas as pd
import easyocr
from pdf2image import convert_from_path

class FacturaProcessor:
    def __init__(self):
        self.reader = easyocr.Reader(['es', 'en'], gpu=True)

    def extract_text(self, file_path):
        text = ""
        if file_path.lower().endswith('.pdf'):
            images = convert_from_path(file_path)
            for img in images:
                result = self.reader.readtext(img)
                text += "\n".join([det[1] for det in result])
        else:  # Imágenes (PNG/JPG)
            result = self.reader.readtext(file_path)
            text = "\n".join([det[1] for det in result])
        return text

    def extract_fields(self, text):
        patterns = {
            "número_factura": r"(N°|Factura|Nº)\s*[:]?\s*([A-Z0-9-]+)",
            "total": r"(Total|TOTAL|Importe)\s*[:]?\s*(\d+,\d{2})\s*EUR",
            "iva": r"(IVA|I.V.A.)\s*[:]?\s*(\d+,\d{2})\s*EUR",
            "fecha": r"(Fecha|FECHA)\s*[:]?\s*(\d{2}/\d{2}/\d{4})",
            "cliente": r"(Cliente|Customer)\s*[:]?\s*([A-Za-z\s]+)",
            "iva_porcentaje": r"(IVA|I.V.A.)\s*(\d{2})%"
        }
        fields = {}
        for field, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            fields[field] = match.group(2).strip() if match and match.group(2) else "No detectado"
        return fields

    def process_folder(self, folder_path):
        data = []
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.pdf', '.png', '.jpg')):
                file_path = os.path.join(folder_path, filename)
                text = self.extract_text(file_path)
                fields = self.extract_fields(text)
                fields["archivo"] = filename
                data.append(fields)
        return pd.DataFrame(data)