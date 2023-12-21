import csv
import smtplib
import unittest
from email.mime.application import MIMEApplication

from seleniumbase import BaseCase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


class SendEmailSteps(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initialize_variables()

    def __initialize_variables(self):
        self.from_email = ''
        self.password_keys = ''
        self.my_server = None
        self.to_email = ''
        self.text_content = ''
        self.message = MIMEMultipart("alternative")

    def set_from_email(self, from_email):
        self.from_email = from_email

    def passkeys_from_email(self, password_keys):
        self.password_keys = password_keys

    def setup_server(self):
        # SMTP Server and port no for GMAIL.com
        gmail_server = "smtp.gmail.com"
        gmail_port = 587

        # Starting connection
        my_server = smtplib.SMTP(gmail_server, gmail_port)
        my_server.ehlo()
        my_server.starttls()

        # Login with your email and password
        my_server.login(self.from_email, self.password_keys)
        self.my_server = my_server

    def set_to_email(self, to_email):
        self.to_email = to_email

    def set_msg(self, message):
        self.message = message

    def add_img_to_email(self, grade_card_path):
        # Read the image from location
        grade_card_img = open(grade_card_path, 'rb').read()

        # Attach your image
        self.message.attach(MIMEImage(grade_card_img, name=os.path.basename(grade_card_path)))

    def add_content_to_email(self, text_content):
        self.message.attach(MIMEText(text_content))

    def add_file_to_email(self, resume_file):
        # Read the file from location
        with open(resume_file, 'rb') as f:
            file = MIMEApplication(
                f.read(),
                name=os.path.basename(resume_file)
            )
            file['Content-Disposition'] = f'attachment;filename = "{os.path.basename(resume_file)}"'
            self.message.attach(file)

    def send_multiple_customized_file_to_email(self, text_content):
        with open("/Users/huongcao/Code/SeleniumBaseLearning/employees/examples/steps/job_contacts.csv") as csv_file:
            jobs = csv.reader(csv_file)
            next(jobs)  # Skip header row

            for recruiter_name, organization, organization_sector, job_role, to_email in jobs:
                email_text = text_content.format(recruiter_name=recruiter_name, organization=organization,
                                                 organization_sector=organization_sector, job_role=job_role)
                # Attaching the personalized text to our message
                self.message.attach(MIMEText(email_text))

                self.set_to_email(to_email)
                self.my_server.sendmail(
                    from_addr=self.from_email,
                    to_addrs=self.to_email,
                    msg=self.message.as_string()
                )
            self.my_server.quit()

    def send_multiple_emails(self, list_email, text_content):
        for to_emails in list_email:
            self.my_server.sendmail(
                from_addr=self.from_email,
                to_addrs=to_emails,
                msg=text_content
            )
        self.my_server.quit()

    def send_email(self):
        self.my_server.sendmail(
            from_addr=self.from_email,
            to_addrs=self.to_email,
            msg=self.message.as_string()
        )
        self.my_server.quit()

