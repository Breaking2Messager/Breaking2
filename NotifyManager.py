from email.mime.text import MIMEText
import smtplib
import requests


class NotifyManager:

    # constructor
    def __init__(self):
        self.__webex_flag__ = 0
        self.__email_flag__ = 0

        # webex teams parameters
        self.__webex_url__ = ""
        self.__webex_space__ = ""
        self.__webex_token__ = ""

        # email parameters
        self.__email_host__ = ""
        self.__email_receiver_list__ = []
        self.__email_sender__ = ""
        self.__email_user__ = ""
        self.__email_passwd__ = ""

    def set_webex_para(self,
                       webex_dict):

        """
        initilize webex teams notification parameter

        Keyword arguments:
        webex_dict: webex teams parameter
        """

        self.__webex_flag__ = 1

        # webex teams
        self.__webex_url__ = webex_dict["webex_url"]
        self.__webex_space__ = webex_dict["webex_space"]
        self.__webex_token__ = webex_dict["webex_token"]

        print("NotifyManager Webex Teams Space=%s"
              % self.__webex_space__)
        print("NotifyManager Webex Teams URL=%s"
              % self.__webex_url__)
        return

    def set_email_para(self,
                       email_dict):

        """
        initilize email notification parameter

        Keyword arguments:
        email_dict: email parameter
        """

        self.__email_flag__ = 1

        # email
        self.__email_host__ = email_dict["email_host"]
        self.__email_receiver_list__ = email_dict["email_recv_list"]
        self.__email_sender__ = email_dict["email_sender_mailbox"]
        self.__email_user__ = email_dict["email_username"]
        self.__email_passwd__ = email_dict["email_password"]

        print("NotifyManager email host=%s"
              % self.__email_host__)
        print("NotifyManager email sender mailbox=%s"
              % self.__email_sender__)
        print("NotifyManager email receiver mailbox=%s"
              % self.__email_receiver_list__)

        return

    def send_msg(self, text):

        """
        send message by webex, mail, sms, and so on

        Keyword arguments:
        text: message content
        """

        if self.__webex_flag__ == 1:
            self.__send_msg_by_webex__(text)

        if self.__webex_flag__ == 1:
            self.__send_msg_by_mail__(text)

        return

    def __send_msg_by_mail__(self, text):

        """
        send message to mail box

        Keyword arguments:
        text: message content
        """

        print("NotifyManager __send_msg_by_mail__ enters")
        print("message=%s" % text)

        subject = "One ERROR message From Kipchoge with Breaking 2 pace!"
        content1 = "Hi, \n\n"
        content2 = "    One ERROR message is recived. Detail content is :\n\n"
        content = content1 + content2 + text
        
        message = MIMEText(content, "plain", "utf-8")
        message["Subject"] = subject
        message["From"] = self.__email_sender__
        message["To"] = ",".join(self.__email_receiver_list__)

        try:
            smtp_obj = smtplib.SMTP()
            smtp_obj = smtplib.SMTP_SSL(self.__email_host__)
            smtp_obj.login(
                self.__email_user__,
                self.__email_passwd__)
            smtp_obj.sendmail(
                self.__email_sender__,
                self.__email_receiver_list__,
                message.as_string())
            smtp_obj.quit()
        except smtplib.SMTPException as e:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("Error! Exception is found to post message by email")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(e)

        return

    def __send_msg_by_webex__(self, text):

        """
        send message to webex team space

        Keyword arguments:
        text: message content
        """

        print("NotifyManager __send_msg_by_webex__ enters")

        # http header
        http_header = {"Content-type": "application/json",
                       "Authorization": "Bearer " + self.__webex_token__}

        # http body
        body = {"roomId": self.__webex_space__,
                "text": text}

        try:
            response = requests.post(
                url=self.__webex_url__,
                json=body,
                headers=http_header)
            print(response.status_code)
        except Exception as e:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("Error! Exception is found to post message over webex teams")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(e)
            return

        if response.status_code == 200:
            pass
        elif response.status_code == 401:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("Webex Team Token Expired")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        else:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("Fail to send message=%s" % text)
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(response.status_code)
            print(response.text)

        return
