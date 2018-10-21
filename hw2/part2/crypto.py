from Crypto.Cipher import AES
from Crypto.Hash import HMAC
from Crypto.Hash import SHA256 as sha256

# h = HMAC.new(secret, digestmode=SHA256)
hash = sha256.new()
hash2 = sha256.new()

class Crypto():
    def __init__(self):
        pass

    def encrypt(self, msg, conf_key, auth_key):
        msg = msg[:-1]
        new_hash = sha256.new()
        if len(msg) <= 16:
            padding = 16 - len(msg)
        else:
            padding = len(msg) % 16
        if padding > 0:
            msg = msg + (' ' * (16 - padding))
        conf_key = new_hash.update(conf_key)
        pad = AES.block_size - len(msg) % AES.block_size
        msg = msg + pad * chr(pad)
        iv = '16byte iv length'
        cypher = AES.new(new_hash.digest(), AES.MODE_CBC, iv)
        encrypted_msg = cypher.encrypt(msg)
        signature = HMAC.new(auth_key, '' , sha256)
        final_encrypt = encrypted_msg + signature.hexdigest()
        return final_encrypt

    def compare_hmac(self, client_hmac, msg_signature):
        client_hmac = client_hmac.hexdigest()
        if len(client_hmac) != len(msg_signature):
            print "invalid MAC size"
            return False
        result = 0

        for x, y in zip(client_hmac, msg_signature):
            result |= ord(x) ^ ord(y)

        return result == 0

    def decrypt(self, encrypted_msg, conf_key, auth_key):
        new_hash = sha256.new()
        test_signature = encrypted_msg[-64:]
        encrypted_msg = encrypted_msg[:-64]
        iv = '16byte iv length'
        if not self.compare_hmac(HMAC.new(auth_key, '' , sha256), test_signature):
            exit()
        conf_key = new_hash.update(conf_key)
        cypher = AES.new(new_hash.digest(), AES.MODE_CBC, iv)
        decrypted_msg = cypher.decrypt(encrypted_msg)
        return decrypted_msg[:-ord(decrypted_msg[-1])]
