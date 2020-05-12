import smtplib
from email.mime.text import MIMEText
import os
from email.mime.multipart import MIMEMultipart


class SendMail:
    report = "report.html"

    @classmethod
    def send_mail_to_all(cls):
        html = open(cls.report, 'rb').read()
        msg = MIMEMultipart('alternative')
        # msg = MIMEMultipart()
        msg['Subject'] = 'Sisense API Monitoring report'
        # set the 'from' address,
        from_addr = os.getenv('from_addr')
        msg['From'] = from_addr
        # set the 'to' addresses
        to_addr = os.getenv('to_addr')
        # msg['To'] = ", ".join(to_addr)
        msg['To'] = to_addr
        from_password = os.getenv('from_password')
        # setup the email server,
        part1 = MIMEText(html, 'html', 'utf-8')
        msg.attach(part1)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        print(from_addr)
        server.login(from_addr, from_password)
        # send the email
        server.sendmail(from_addr, to_addr, msg.as_string())
        # disconnect from the server
        server.quit()
        return

SendMail.send_mail_to_all()
