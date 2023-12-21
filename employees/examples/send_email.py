from email.mime.multipart import MIMEMultipart

from employees.examples.steps.send_email_steps import SendEmailSteps


class SendEmail(SendEmailSteps):
    def test_send_email_with_img(self):
        self.set_from_email('caongochuong0601@gmail.com')
        self.passkeys_from_email('wtth owce lykw wqlk')
        self.setup_server()
        self.set_to_email('caohuongtest@yopmail.com')
        self.add_img_to_email('/Users/huongcao/Code/gau.jpg')
        self.send_email()

    def test_send_email_with_content(self):
        self.set_from_email('caongochuong0601@gmail.com')
        self.passkeys_from_email('wtth owce lykw wqlk')
        self.setup_server()
        self.set_to_email('caohuongtest@yopmail.com')
        self.set_msg(MIMEMultipart())
        self.add_content_to_email('this is testing !!')
        self.send_email()

    def test_send_email_with_file(self):
        self.set_from_email('caongochuong0601@gmail.com')
        self.passkeys_from_email('wtth owce lykw wqlk')
        self.setup_server()
        self.set_to_email('caohuongtest@yopmail.com')
        self.set_msg(MIMEMultipart())
        self.add_file_to_email('/Users/huongcao/Code/file_test.txt')
        self.send_email()

    def test_send_email_with_customized(self):
        self.set_from_email('caongochuong0601@gmail.com')
        self.passkeys_from_email('wtth owce lykw wqlk')
        self.setup_server()
        text_content = """
                Hello {recruiter_name}, I hope you are doing well. I’m Jane Doe, an engineering graduate 
                with an Mtech in Computer Science and a specialization in Artificial Intelligence.

                I am writing to inquire regarding open roles in {job_role} at {organization}. I have experience 
                performing data analysis and modeling through my internships and research projects. I’m excited
                to have an opportunity to apply my skills and learn more in the {organization_sector}.

                I have attached my grade card and résumé below. Looking forward to hearing from you.

                Thanks,
                …… """
        self.send_multiple_customized_file_to_email(text_content)

    def test_send_multiple_private_emails(self):
        self.set_from_email('caongochuong0601@gmail.com')
        self.passkeys_from_email('wtth owce lykw wqlk')
        self.setup_server()
        text_content = """ Thanks """
        list_email = ["huongtest1@yopmail.com", "huongtest2@yopmail.com"]
        self.send_multiple_emails(list_email, text_content)

    def test_send_multiple_public_emails(self):
        self.set_from_email('caongochuong0601@gmail.com')
        self.passkeys_from_email('wtth owce lykw wqlk')
        self.setup_server()
        list_email = ["huongtest1@yopmail.com", "huongtest2@yopmail.com"]
        self.set_to_email(list_email)
        self.set_msg(MIMEMultipart())
        self.add_content_to_email('this is testing !!')
        self.send_email()
