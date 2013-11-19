import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from asl.application.service_application import service_application as app
from asl.utils.injection_helper import inject

def send_email(sender, receivers, subject, text = None, html = None, charset = 'utf-8'):
    '''
    Sends an email.

    @param sender: Sender as string or None for default got from config.
    @param receivers: String or array of recipients.
    @param subject: Subject.
    @param text: Plain text message.
    @param html: Html message.
    @param charset: Charset.
    '''
    smtp_config = app.config['SMTP']

    # Receivers must be an array.
    if not isinstance(receivers, list) and not isinstance(receivers, tuple):
        receivers = [receiveres]

    # Create the messages
    msgs = []
    if text is not None:
        msgs.append(MIMEText(text, 'plain', charset))

    if html is not None:
        msgs.append(MIMEText(html, 'html', charset))

    if len(msgs) == 0:
        raise Exception("No message is given.")

    if len(msgs) == 1:
        msg = msgs[0]
    else:
        msg = MIMEMultipart()
        for m in msgs:
            msg.attach(m)

    # Default sender.
    if sender is None:
        sender = smtp_config['SENDER']

    # Fill the info.
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ", ".join(receivers)

    # Send.
    smtpServer = smtplib.SMTP(**(smtp_config['SERVER']))
    smtpServer.sendmail(sender, receivers, msg.as_string())
    smtpServer.quit()