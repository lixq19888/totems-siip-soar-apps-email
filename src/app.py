"""
 安博通 www.abtnetworks.com
"""
import os

from SoarAction import SoarAction
from SoarUtils import output_handler

import smtplib
from email.header import Header
from email.utils import parseaddr, formataddr
from email.mime.text import MIMEText
from SoarDataModel import ResultStatusEnum

APP_NAME = "Email"
ACTION_LIST = ["TEXT"]
LogFile = "email.log"


class MailServer(SoarAction):
    __version__ = "1.0.0"
    subject = ''
    to_address = ''
    from_address = ''
    from_address_alias = ''
    mail_host = ''
    password = ''
    port = 465
    mail_debug = False

    def __init__(self, app_name, action_list, input_data, action_select):
        log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), LogFile)
        super(MailServer, self).__init__(app_name, log_path, action_list, input_data, action_select)

    @output_handler
    def PING(self):
        """
        实例测试
        :return:
        """
        self.params["subject"] = "测试邮件"
        self.params["content"] = "这是一封测试邮件"
        self.params["toAddress"] = self.setting_param_dict["fromAddress"]
        return self.TEXT()

    @output_handler
    def TEXT(self):
        """
        发送简单文本内容邮件
        :return:
        """
        self.subject = self.params["subject"]
        self.to_address = self.params["toAddress"]
        self.from_address = self.setting_param_dict["fromAddress"]
        self.from_address_alias = self.setting_param_dict["fromAddressAlias"]
        self.mail_host = self.setting_param_dict["host"]
        self.password = self.setting_param_dict["password"]
        self.port = self.setting_param_dict["port"]
        self.mail_debug = self.setting_param_dict["debug"]
        if self.subject != '' and self.to_address != '' \
                and self.params["content"] != '' and 0 < self.port < 65535:
            pass
        else:
            return self.get_error_response('param error!')
        self.logger.info("subject:" + self.subject + ", to_address:" + self.to_address)
        msg = MIMEText(self.params["content"], 'plain', 'utf-8')
        if self.from_address_alias:
            msg['From'] = MailServer.format_address('%s <%s>' % (self.from_address_alias, self.from_address))
        else:
            msg['From'] = MailServer.format_address(self.from_address)
        send_to = MailServer.format_address(self.to_address)
        msg['To'] = send_to
        msg['Subject'] = Header(self.subject, 'utf-8').encode()

        try:
            # 连接到服务器
            if self.port == 465:
                smtp_server = smtplib.SMTP_SSL(self.mail_host)
            else:
                smtp_server = smtplib.SMTP()
                smtp_server.connect(self.mail_host, self.port)
            # 调试日志
            if str(self.mail_debug).upper() == str('TURE'):
                smtp_server.set_debuglevel(1)
            # 登录到邮件服务器
            smtp_server.login(self.from_address, self.password)
            # 发送邮件
            smtp_server.sendmail(self.from_address, msg['To'].split(','), msg.as_string())
            # 退出
            smtp_server.quit()
            return self.get_response_json('send success')
        except smtplib.SMTPException as e:
            print('error', e)
        return self.get_error_response('send fail')

    @staticmethod
    def format_address(s):
        """
        格式化邮件地址
        :param s:
        :return:
        """
        to_address_str_list = s.split(',')
        to_address_list = []
        for to in to_address_str_list:
            name, address = parseaddr(to)
            to_address_list.append(formataddr((Header(name, 'utf-8').encode(), address)))
        return ','.join(to_address_list)


if __name__ == '__main__':
    # input_data = r'%7B%22appName%22%3A%22email%22%2C%22actions%22%3A%5B%7B%22name%22%3A%22TEXT%22%2C%22parameters%22%3A%5B%7B%22name%22%3A%22subject%22%2C%22value%22%3A%22%E9%82%AE%E4%BB%B6%E6%B5%8B%E8%AF%95%E4%B8%BB%E9%A2%981%22%2C%22defaultValue%22%3A%22www.baidu.com%22%2C%22schema%22%3A%7B%22type%22%3A%22STRING%22%7D%2C%22required%22%3Atrue%2C%22setting%22%3A%7B%22multiline%22%3Afalse%7D%7D%2C%7B%22name%22%3A%22toAddress%22%2C%22value%22%3A%22fanxiaole%40abtnetworks.com%22%2C%22defaultValue%22%3A%22fanxiaole%40abtnetworks.com%22%2C%22schema%22%3A%7B%22type%22%3A%22STRING%22%7D%2C%22required%22%3Atrue%2C%22setting%22%3A%7B%22multiline%22%3Afalse%7D%7D%2C%7B%22name%22%3A%22content%22%2C%22value%22%3A%22%E8%BF%99%E4%B8%AA%E6%98%AF%E9%82%AE%E4%BB%B6%E5%86%85%E5%AE%B91%22%2C%22defaultValue%22%3A%22www.baidu.com%22%2C%22schema%22%3A%7B%22type%22%3A%22STRING%22%7D%2C%22required%22%3Atrue%2C%22setting%22%3A%7B%22multiline%22%3Afalse%7D%7D%2C%7B%22name%22%3A%22host%22%2C%22value%22%3A%22%22%2C%22defaultValue%22%3A%22smtp.qq.com%22%2C%22schema%22%3A%7B%22type%22%3A%22STRING%22%7D%2C%22required%22%3Afalse%7D%2C%7B%22name%22%3A%22port%22%2C%22value%22%3A%22%22%2C%22defaultValue%22%3A%22465%22%2C%22schema%22%3A%7B%22type%22%3A%22INTEGER%22%7D%2C%22required%22%3Afalse%7D%2C%7B%22name%22%3A%22fromAddress%22%2C%22value%22%3A%22%22%2C%22defaultValue%22%3A%221964645988%40qq.com%22%2C%22schema%22%3A%7B%22type%22%3A%22STRING%22%7D%2C%22required%22%3Afalse%7D%2C%7B%22name%22%3A%22fromAddressAlias%22%2C%22value%22%3A%22%E5%AE%89%E5%8D%9A%E9%80%9A%E7%B3%BB%E7%BB%9F%E9%82%AE%E4%BB%B6%22%2C%22defaultValue%22%3A%22xxx%22%2C%22schema%22%3A%7B%22type%22%3A%22STRING%22%7D%2C%22required%22%3Afalse%7D%2C%7B%22name%22%3A%22password%22%2C%22value%22%3A%22%22%2C%22defaultValue%22%3A%22kpnkmqtronvmcefd%22%2C%22schema%22%3A%7B%22type%22%3A%22STRING%22%7D%2C%22required%22%3Afalse%7D%2C%7B%22name%22%3A%22debug%22%2C%22value%22%3A%22%22%2C%22defaultValue%22%3A%22False%22%2C%22schema%22%3A%7B%22type%22%3A%22BOOLEAN%22%7D%2C%22required%22%3Afalse%7D%5D%2C%22returns%22%3A%7B%22schema%22%3A%7B%22type%22%3A%22STRING%22%7D%2C%22example%22%3A%22success%22%2C%22description%22%3A%22XXXXXX%22%7D%7D%5D%7D'
    app = MailServer(APP_NAME, ACTION_LIST, None, None)
    app.do_action()
