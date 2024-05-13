import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

gmail_username = 'kinekids2324'
gmail_app_password = 'Bab1lonia' 
sent_from = 'kinekids2324@gmail.com'
sent_to = ['kinekids2324@gmail.com']
sent_subject_low_press_1K = "Low Pressure!"
sent_body_low_press_1K = ("Miao!\n\n"
             "Maio!!\n"
             "\n"
             "Cheers,\n"
             "Riccardo\n")

# Constructing the email message
msg = MIMEMultipart()
msg['From'] = sent_from
msg['To'] = ', '.join(sent_to)
msg['Subject'] = sent_subject_low_press_1K
msg.attach(MIMEText(sent_body_low_press_1K, 'plain'))

email_text = msg.as_string()

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_username, gmail_app_password)
    server.sendmail(sent_from, sent_to, email_text)
    server.close()
    print('Email alert sent!')
except Exception as exception:
    print("Error: %s!\n\n" % exception)