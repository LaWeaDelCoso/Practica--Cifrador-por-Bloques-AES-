from enum import Enum
from dataclasses import dataclass
from typing import Optional

from Crypto.Cipher import AES
from Crypto.Random  import get_random_bytes
from Crypto.Util.Padding import pad, unpad

"""
Modos de operación que soporta AES de 
acuerdo con NIST SP 800-38A/38D.
"""
class AESMode(Enum):
    ECB = "ECB"
    CBC = "CBC"
    CFB = "CFB"
    OFB = "OFB"
    CTR = "CTR"
    GCM = "GCM"

# Metadatos de cada modo
MODE_CONFIG = {
    AESMode.ECB: {"iv_size": 0, "description": "Electronic Codebook"},
    AESMode.CBC: {"iv_size": 16, "description": "Cipher Block Chaining"},
    AESMode.CFB: {"iv_size": 16, "description": "Cipher Feedback"},
    AESMode.OFB: {"iv_size": 16, "description": "Output Feedback"},
    AESMode.CTR: {"iv_size": 16, "description": "Counter Mode"},
    AESMode.GCM: {"iv_size": 12, "description": "Galois/Counter Mode (Authenticated)"},
}

#  Tamaño del tag de autenticación para GCM (Galois/Counter Mode) El NIST recomienda: 16 bytes / 128 bits
GCM_TAG_SIZE = 16


class AESModel:

    KEY_SIZE = 32
    
    """
    Generación, guardado y carga de llaves
    """
    def generate_key(self) -> bytes:
        return get_random_bytes(self.KEY_SIZE)

    def save_key(self, key: bytes, path: str) -> None:
        with open(path, "wb") as f:
            f.write(key)

    # Sólo se considera como valida una de 32 bits
    def load_key(self, path: str) -> bytes:
        with open(path, "rb") as f:
            key = f.read()
        if len(key) != self.KEY_SIZE:
            raise ValueError(
                f"Llave inválida: se esperaban 32 bytes; "
                f"se obtuvieron {len(key)}."
            )
        return key
    

    """ 
    Identificar Modo
    """
    def get_iv_size(self, mode: AESMode) -> int:
        return MODE_CONFIG[mode]["iv_size"]

    def requires_iv(self, mode: AESMode) -> bool:
        return MODE_CONFIG[mode]["iv_size"] > 0
    
    """
    Cifrar
    """
    def encrypt_file(
        self,
        input_path: str,
        key: bytes,
        mode: AESMode,
        iv: Optional[bytes],
        output_path: str,
    ) -> tuple[bool, str]:
        
        try:
            with open(input_path, "rb") as f:
                plaintext = f.read()

            if mode == AESMode.ECB:
                # ECB no usa IV; cada bloque se cifra de forma independiente.
                # NIST SP 800-38A Sección 6.1
                cipher = AES.new(key, AES.MODE_ECB)
                output = cipher.encrypt(pad(plaintext, AES.block_size))

            elif mode == AESMode.CBC:
                # CBC: El IV se usa para encadenar bloques. 
                # NIST SP 800-38A Sección 6.2
                cipher = AES.new(key, AES.MODE_CBC, iv=iv)
                output = iv + cipher.encrypt(pad(plaintext, AES.block_size))

            elif mode == AESMode.CFB:
                # CFB128: Segmento de 128 bits. 
                # NIST SP 800-38A Sección 6.3
                cipher = AES.new(key, AES.MODE_CFB, iv=iv, segment_size=128)
                output = iv + cipher.encrypt(plaintext)

            elif mode == AESMode.OFB:
                # OFB: Convierte el cifrador de bloque en flujo. 
                # NIST SP 800-38A Sección 6.4
                cipher = AES.new(key, AES.MODE_OFB, iv=iv)
                output = iv + cipher.encrypt(plaintext)

            elif mode == AESMode.CTR:
                # CTR: El IV funciona como valor inicial del contador. 
                # NIST SP 800-38A Sección 6.5
                initial_value = int.from_bytes(iv, byteorder="big")
                cipher = AES.new(key, AES.MODE_CTR, initial_value=initial_value, nonce=b"")
                output = iv + cipher.encrypt(plaintext)

            elif mode == AESMode.GCM:
                # GCM: cifrado autenticado. El tag garantiza integridad. 
                # NIST SP 800-38D
                cipher = AES.new(key, AES.MODE_GCM, nonce=iv, mac_len=GCM_TAG_SIZE)
                ciphertext, tag = cipher.encrypt_and_digest(plaintext)
                output = iv + ciphertext + tag  # nonce || ciphertext || tag

            with open(output_path, "wb") as f:
                f.write(output)

            return True, f"Archivo cifrado exitosamente con AES-{mode.value}."

        except Exception as exc:
            return False, f"Error al cifrar: {exc}"

    """
    Descifrar
    """
    def decrypt_file(
        self,
        input_path: str,
        key: bytes,
        mode: AESMode,
        output_path: str,
    ) -> tuple[bool, str]:
        
        try:
            with open(input_path, "rb") as f:
                data = f.read()

            if mode == AESMode.ECB:
                cipher = AES.new(key, AES.MODE_ECB)
                plaintext = unpad(cipher.decrypt(data), AES.block_size)

            elif mode == AESMode.CBC:
                iv, ciphertext = data[:16], data[16:]
                cipher = AES.new(key, AES.MODE_CBC, iv=iv)
                plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

            elif mode == AESMode.CFB:
                iv, ciphertext = data[:16], data[16:]
                cipher = AES.new(key, AES.MODE_CFB, iv=iv, segment_size=128)
                plaintext = cipher.decrypt(ciphertext)

            elif mode == AESMode.OFB:
                iv, ciphertext = data[:16], data[16:]
                cipher = AES.new(key, AES.MODE_OFB, iv=iv)
                plaintext = cipher.decrypt(ciphertext)

            elif mode == AESMode.CTR:
                iv, ciphertext = data[:16], data[16:]
                initial_value = int.from_bytes(iv, byteorder="big")
                cipher = AES.new(key, AES.MODE_CTR, initial_value=initial_value, nonce=b"")
                plaintext = cipher.decrypt(ciphertext)

            elif mode == AESMode.GCM:
                # Extraer nonce, ciphertext y tag de sus posiciones fijas
                nonce      = data[:12]
                tag        = data[-GCM_TAG_SIZE:]
                ciphertext = data[12:-GCM_TAG_SIZE]
                cipher = AES.new(key, AES.MODE_GCM, nonce=nonce, mac_len=GCM_TAG_SIZE)
                # decrypt_and_verify lanza ValueError si el tag no coincide
                plaintext = cipher.decrypt_and_verify(ciphertext, tag)

            with open(output_path, "wb") as f:
                f.write(plaintext)

            return True, f"Archivo descifrado exitosamente con AES-{mode.value}."

        except ValueError as exc:
            # Padding incorrecto o tag GCM inválido implican clave o modo incorrectos
            return False, f"Error de integridad o clave incorrecta: {exc}"
        except Exception as exc:
            return False, f"Error al descifrar: {exc}"