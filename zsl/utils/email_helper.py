"""
:mod:`zsl.utils.email_helper`
-----------------------------
"""

from __future__ import unicode_literals
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from zsl import inject, Config, Injected


@inject(config=Config)
def send_email(sender, receivers, subject, text=None, html=None, charset='utf-8', config=Injected):
    """Sends an email.

    :param sender: Sender as string or None for default got from config.
    :param receivers: String or array of recipients.
    :param subject: Subject.
    :param text: Plain text message.
    :param html: Html message.
    :param charset: Charset.
    :param config: Current configuration
    """
    smtp_config = config['SMTP']

    # Receivers must be an array.
    if not isinstance(receivers, list) and not isinstance(receivers, tuple):
        receivers = [receivers]

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
    smtp_server = smtplib.SMTP(**(smtp_config['SERVER']))
    smtp_server.sendmail(sender, receivers, msg.as_string())
    smtp_server.quit()
