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
    AESMode.ECB: {"requires_iv": False, "iv_size": 0,  "padding": True,  "description": "Electronic Codebook"},
    AESMode.CBC: {"requires_iv": True,  "iv_size": 16, "padding": True,  "description": "Cipher Block Chaining"},
    AESMode.CFB: {"requires_iv": True,  "iv_size": 16, "padding": False, "description": "Cipher Feedback"},
    AESMode.OFB: {"requires_iv": True,  "iv_size": 16, "padding": False, "description": "Output Feedback"},
    AESMode.CTR: {"requires_iv": True,  "iv_size": 16, "padding": False, "description": "Counter Mode"},
    AESMode.GCM: {"requires_iv": True,  "iv_size": 12, "padding": False, "description": "Galois/Counter Mode (Authenticated)"},
}

#  Tamaño del tag de autenticación para GCM (Galois/Counter Mode) El NIST recomienda: 16 bytes / 128 bits
GCM_TAG_SIZE = 16

# Contenedor para el resultado de las operaciones
@dataclass
class CryptoResult:
    success: bool
    message: str
    output_path: Optional[str] = None

