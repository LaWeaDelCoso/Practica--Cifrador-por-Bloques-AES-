import os
from typing import Optional

from models import AESModel, AESMode, MODE_CONFIG
from utils import (
    get_timestamp,
    build_key_filename,
    build_encrypted_filename,
    build_decrypted_filename,
)

class AESController:

    def __init__(self) -> None:
        self._model = AESModel()

    """Generación de Llaves"""
    def generate_and_save_key(self, directory: str) -> tuple[bool, str]:
        try:
            key = self._model.generate_key()
            filename = build_key_filename(get_timestamp())
            path = os.path.join(directory, filename)
            self._model.save_key(key, path)
            return True, f"Llave guardada exitosamente:\n{path}"
        except Exception as exc:
            return False, f"Error al generar la llave: {exc}"
        
    """Validación del IV"""
    def validate_iv(
        self, iv_text: str, mode: AESMode
    ) -> tuple[bool, str, Optional[bytes]]:
       
        iv_size = self._model.get_iv_size(mode)

        if iv_size == 0:
            return True, "", None

        if not iv_text:
            return False, f"{mode.value} requiere un IV de {iv_size} bytes.", None

        iv_bytes = iv_text.encode("utf-8")
        if len(iv_bytes) != iv_size:
            return (
                False,
                f"El IV para {mode.value} debe tener exactamente {iv_size} bytes "
                f"(actualmente: {len(iv_bytes)}).",
                None,
            )

        return True, "", iv_bytes
    
    """Cifrar"""
    def encrypt(
        self,
        input_path: str,
        key_path: str,
        mode: AESMode,
        iv_text: str,
        output_dir: str,
    ) -> tuple[bool, str]:
        
        # Validación de entradas
        if not input_path or not os.path.isfile(input_path):
            return False, "Seleccione un archivo de entrada válido."
        if not key_path or not os.path.isfile(key_path):
            return False, "Seleccione un archivo de clave válido."

        try:
            key = self._model.load_key(key_path)
        except Exception as exc:
            return False, str(exc)

        iv_valid, iv_error, iv_bytes = self.validate_iv(iv_text, mode)
        if not iv_valid:
            return False, iv_error

        output_path = os.path.join(
            output_dir, build_encrypted_filename(input_path, mode.value)
        )
        
        return self._model.encrypt_file(input_path, key, mode, iv_bytes, output_path)

    """Descifrar"""
    def decrypt(
        self,
        input_path: str,
        key_path: str,
        mode: AESMode,
        output_dir: str,
    ) -> tuple[bool, str]:
        
        # Validación de entradas
        if not input_path or not os.path.isfile(input_path):
            return False, "Seleccione un archivo cifrado válido."
        if not key_path or not os.path.isfile(key_path):
            return False, "Seleccione un archivo de clave válido."

        try:
            key = self._model.load_key(key_path)
        except Exception as exc:
            return False, str(exc)

        output_path = os.path.join(
            output_dir, build_decrypted_filename(input_path, mode.value)
        )

        return self._model.decrypt_file(input_path, key, mode, output_path)