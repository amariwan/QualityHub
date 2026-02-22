from app.core.security.token_cipher import TokenCipher


def test_encrypt_decrypt_roundtrip():
    cipher = TokenCipher("unit-test-secret")
    token = "glpat-example-token"
    encrypted = cipher.encrypt(token)

    assert encrypted != token
    assert cipher.decrypt(encrypted) == token
