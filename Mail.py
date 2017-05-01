from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
from email.mime.base import MIMEBase
import smtplib
import time
import os

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def SendMail(receiver,to_addr,content,papers):
    from_addr = "miunhelper@gmail.com"
    password = "sundsvall"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    #title of email
    title='Portal Information('+time.asctime(time.localtime(time.time()))+')'

    #email object
    msg = MIMEMultipart()
    msg['From'] = _format_addr('MIUN Helper <%s>' % from_addr)
    msg['To'] = _format_addr('%s <%s>' % (receiver, to_addr))
    msg['Subject'] = Header(title, 'utf-8').encode()

    #main body of email is MIMEText
    content+="<p><img src='cid:0'></p>"
    msg.attach(MIMEText(content,"html","utf-8"))

    with open("logo.jpg", 'rb') as f:
        # set attachment's MIMIE and filename
        mime = MIMEBase('image', 'jpg', filename="logo.jpg")
        # add necessary header info
        mime.add_header('Content-Disposition', 'attachment', filename="logo.jpg")
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')
        # read the binary content of file
        mime.set_payload(f.read())
        # encode with base64
        encoders.encode_base64(mime)
        # add to MIMEMultipart:
        msg.attach(mime)

    index=0
    for paper in papers:
        with open(paper,'rb') as f:
            index+=1
            #get the filename from path
            name=os.path.split(paper)[1]
            # set attachment's MIMIE and filename
            mime = MIMEBase('image', 'pdf', filename=name)
            # add necessary header info
            mime.add_header('Content-Disposition', 'attachment', filename=name)
            mime.add_header('Content-ID', '<'+str(index)+'>')
            mime.add_header('X-Attachment-Id', str(index))
            # read the binary content of file
            mime.set_payload(f.read())
            # encode with base64
            encoders.encode_base64(mime)
            # add to MIMEMultipart:
            msg.attach(mime)

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()#start tls connection
    server.set_debuglevel(0)
    server.login(from_addr, password)#authenticate
    server.sendmail(from_addr, [to_addr], msg.as_string())#start sending mail
    server.quit()





