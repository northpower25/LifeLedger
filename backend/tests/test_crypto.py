import pytest
from cryptography.exceptions import InvalidTag

from lifeledger.crypto import (
    decrypt_bytes,
    derive_key,
    encrypt_bytes,
    new_salt,
)


def test_argon2id_and_aes_gcm_are_salted_and_authenticated():
    salt = new_salt()
    key = derive_key("synthetic-test-password", salt)
    assert key == derive_key("synthetic-test-password", salt)
    assert key != derive_key("synthetic-test-password", new_salt())

    ciphertext = encrypt_bytes(key, b"synthetic-payload", b"table:opaque-id")
    assert decrypt_bytes(key, ciphertext, b"table:opaque-id") == b"synthetic-payload"
    with pytest.raises(InvalidTag):
        decrypt_bytes(key, ciphertext, b"table:other-id")

    modified = ciphertext[:-1] + bytes([ciphertext[-1] ^ 1])
    with pytest.raises(InvalidTag):
        decrypt_bytes(key, modified, b"table:opaque-id")
