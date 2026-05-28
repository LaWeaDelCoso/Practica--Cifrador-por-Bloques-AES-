import os
from datetime import datetime

"""
Estructuras establecidad para nombres de archivos
"""

# Devuelve una timestamp en formato DD/MM/YYYY_HH-MM
def get_timestamp() -> str:
    now = datetime.now()
    return now.strftime("%d-%m-%Y_%H-%M")

# Devuelve el nombre para la llave generada
def build_key_filename(timestamp: str) -> str:
    return f"AES_KEY_{timestamp}.key"

# Estructura del nombre del archivo de salida al cifrar [NOMBRE ORIGINAL]_enc_[MODO].[EXTENSIÓN]
def build_encrypted_filename(original_path: str, mode_name: str) -> str:
    base = os.path.basename(original_path)
    name, ext = os.path.splitext(base)
    return f"{name}_enc_{mode_name}{ext}"

# Estructura del nombre del archivo de salida al descifrar [NOMBRE ORIGINAL]_dec_[MODO].[EXTENSIÓN]
def build_decrypted_filename(original_path: str, mode_name: str) -> str:
    base = os.path.basename(original_path)
    name, ext = os.path.splitext(base)
    return f"{name}_dec_{mode_name}{ext}"