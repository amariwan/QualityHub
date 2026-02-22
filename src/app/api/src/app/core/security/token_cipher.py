from __future__ import annotations

import base64
import hashlib

from cryptography.fernet import Fernet

from app.config.settings import get_settings


class TokenCipher:
    def __init__(self, secret: str | None = None):
        settings = get_settings()
        material = secret or settings.TOKEN_ENCRYPTION_KEY or settings.SESSION_SECRET
        key = self._build_fernet_key(material)
        self._fernet = Fernet(key)

    @staticmethod
    def _build_fernet_key(raw: str) -> bytes:
        digest = hashlib.sha256(raw.encode("utf-8")).digest()
        return base64.urlsafe_b64encode(digest)

    def encrypt(self, plaintext: str) -> str:
        return self._fernet.encrypt(plaintext.encode("utf-8")).decode("utf-8")

    def decrypt(self, ciphertext: str) -> str:
        return self._fernet.decrypt(ciphertext.encode("utf-8")).decode("utf-8")
