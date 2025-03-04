import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

class SendMailService:
    def __init__(self, message, receiver) -> None:
        self.s = smtplib.SMTP('smtp.gmail.com', 587)
        self.s.starttls()

        self.s.login(os.getenv('APP_EMAIL'), os.getenv('APP_PASSWORD'))
        self.message = message
        self.receiver = receiver
    
    def send(self):
        # sending the mail
        self.s.sendmail(os.getenv('APP_EMAIL'), self.receiver, self.message)
        # terminating the session
        self.s.quit()