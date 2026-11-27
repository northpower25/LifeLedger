"""Cryptographic primitives and versioned encrypted payloads for the local slice."""

from __future__ import annotations

import base64
import json
import os
from typing import Any

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError
from argon2.low_level import Type, hash_secret_raw
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ARGON2_TIME_COST = 3
ARGON2_MEMORY_KIB = 65_536
ARGON2_PARALLELISM = 1
ARGON2_HASH_LENGTH = 32
NONCE_LENGTH = 12
_password_hasher = PasswordHasher(
    time_cost=ARGON2_TIME_COST,
    memory_cost=ARGON2_MEMORY_KIB,
    parallelism=ARGON2_PARALLELISM,
    hash_len=ARGON2_HASH_LENGTH,
    salt_len=16,
)


def new_data_key() -> bytes:
    return AESGCM.generate_key(bit_length=256)


def new_salt() -> bytes:
    return os.urandom(16)


def derive_key(password: str, salt: bytes) -> bytes:
    return hash_secret_raw(
        secret=password.encode("utf-8"),
        salt=salt,
        time_cost=ARGON2_TIME_COST,
        memory_cost=ARGON2_MEMORY_KIB,
        parallelism=ARGON2_PARALLELISM,
        hash_len=ARGON2_HASH_LENGTH,
        type=Type.ID,
    )


def hash_password(password: str) -> str:
    return _password_hasher.hash(password)


def verify_password(password_hash: str, password: str) -> bool:
    try:
        return _password_hasher.verify(password_hash, password)
    except (VerifyMismatchError, InvalidHashError, VerificationError):
        return False


def encrypt_bytes(key: bytes, plaintext: bytes, associated_data: bytes) -> bytes:
    nonce = os.urandom(NONCE_LENGTH)
    return nonce + AESGCM(key).encrypt(nonce, plaintext, associated_data)


def decrypt_bytes(key: bytes, ciphertext: bytes, associated_data: bytes) -> bytes:
    if len(ciphertext) < NONCE_LENGTH + 16:
        raise ValueError("Invalid encrypted payload")
    nonce = ciphertext[:NONCE_LENGTH]
    return AESGCM(key).decrypt(nonce, ciphertext[NONCE_LENGTH:], associated_data)


def encrypt_json(key: bytes, value: Any, associated_data: bytes) -> bytes:
    plaintext = json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return encrypt_bytes(key, plaintext, associated_data)


def decrypt_json(key: bytes, ciphertext: bytes, associated_data: bytes) -> Any:
    return json.loads(decrypt_bytes(key, ciphertext, associated_data))


def b64encode(value: bytes) -> str:
    return base64.b64encode(value).decode("ascii")


def b64decode(value: str) -> bytes:
    return base64.b64decode(value, validate=True)
