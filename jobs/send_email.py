import email, os, smtplib

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate


def default_email(send_from, send_to, subject, attachment):
    """
    Sends report email

    :param send_from: email address to send from
    :param send_to: email address(es) to send to
    :param subject: email subject
    :param attachment: attachments to include

    """

    smtpserver = os.getenv("SMTPSERVER")
    smtpport = os.getenv("SMTPPORT")

    # Create a multipart message and set headers
    msg = MIMEMultipart()
    msg["From"] = send_from
    msg["To"] = str(send_to)
    msg["Date"] = formatdate(localtime=True)
    msg["Subject"] = subject

    # Add body to email
    body = "Hello,\nPlease see the attached " + subject.lower() + " breakdown."
    msg.attach(MIMEText(body, "plain"))

    filename = os.path.basename(attachment)

    part = MIMEBase("application", "octet-stream")
    part.set_payload(open(attachment, "rb").read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", "attachment; filename=" + filename)
    msg.attach(part)

    # Send the email
    server = smtplib.SMTP(smtpserver, smtpport)
    server.sendmail(msg["From"], msg["To"].split(","), msg.as_string())

    server.quit()
