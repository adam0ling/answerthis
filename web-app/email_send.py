import smtplib 

def send_email(message):
    gmail_user = 'user@gmail.com'  # change to actual user
    gmail_pass = 'password'  # change to actual pass

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_pass)
        server.sendmail(gmail_user, gmail_user, message)
    except:
        print('Email didnt work...')