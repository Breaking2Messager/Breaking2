from email.mime.text import MIMEText
import smtplib
import requests


class NotifyManager:

    # constructor
    def __init__(self):
        self.__webex_flag__ = 0
        self.__email_flag__ = 0
        pass

    def set_webex_para(self,
                       webex_dict={}):

        self.__webex_flag__ = 1

        # webex teams
        self.__webex_url__ = webex_dict["webex_url"]
        self.__webex_space__ = webex_dict["webex_space"]
        self.__webex_token__ = webex_dict["webex_token"]

        print("NotifyManager Webex Teams Space=%s"
              % self.__webex_space__)
        print("NotifyManager Webex Teams URL=%s"
              % self.__webex_url__)


    def set_email_para(self,
                       email_dict={}):
        
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

    # deconstructor
    def __del__(self):
        pass
     
    def send_msg(self, text):

        """
        send message by webex, mail, sms, and so on

        Keyword arguments:
        text: message content
        """
        self.__send_msg_by_webex__(text)
        self.__send_msg_by_mail__(text)
        self.__send_msg_by_sms__(text)
        self.__send_msg_by_wechat__(text)

    def __send_msg_by_wechat__(self, text):
        """
        send message to SMS

        Keyword arguments:
        text: message content
        """
        pass

    def __send_msg_by_sms__(self, text):

        """
        send message to SMS

        Keyword arguments:
        text: message content
        """
        pass

    def __send_msg_by_mail__(self, text):

        """
        send message to mail box

        Keyword arguments:
        text: message content
        """

        print("NotifyManager __send_msg_by_mail__ enters")
        print("message=%s" % text)

        message = MIMEText(text, 'plain', 'utf-8')
        message['Subject'] = 'Error alert from Hunter Project'
        message['From'] = self.__email_sender__
        message['To'] = ','.join(self.__email_receiver_list__)

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
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print('Error! Exception is found to post message by email')
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
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
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print('Error! Exception is found to post message over webex teams')
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print(e)
            return

        if response.status_code == 200:
            pass
        elif response.status_code == 401:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print('Webex Team Token Expired')
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        else:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print('Fail to send message=%s' % text)
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print(response.status_code)
            print(response.text)

        return
