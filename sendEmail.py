import json
import smtplib
import time
from email.mime.text import MIMEText
from email.header import Header

class email:

    # 初始化 发件人 发件人密码 收件人(组)
    def __init__(self):
        self.msg_from = '962655354@qq.com'  # 发送方邮箱
        self.password = ''
        with open(r'./userInfo.json',mode='r',encoding='utf-8') as userFile:
            self.password = json.load(userFile)["emailPassword"]
        self.msg_to = ['962655354@qq.com', '1617943934@qq.com']  # 收件人邮箱
        # msg_to = '616564099@qq.com'  # 收件人邮箱

    # 发送邮件
    def send(self,subject,content):
        self.__init__()
        # subject = "邮件标题"  # 主题
        # content = "邮件内容，我是邮件内容，哈哈哈"
        # 生成一个MIMEText对象（还有一些其它参数）
        msg = MIMEText(content)
        # 放入邮件主题
        msg['Subject'] = subject
        # 也可以这样传参
        # msg['Subject'] = Header(subject, 'utf-8')
        # 放入发件人
        msg['From'] = self.msg_from
        # 放入收件人
        # msg['To'] = '616564099@qq.com'
        # msg['To'] = '发给你的邮件啊'
        s = None
        try:
            # 通过ssl方式发送，服务器地址，端口
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)
            # 登录到邮箱
            s.login(self.msg_from, self.password)
            # 发送邮件：发送方，收件方，要发送的消息
            s.sendmail(self.msg_from, self.msg_to, msg.as_string())
            print('成功')
        except smtplib.SMTPException as e:
            print("错误信息：",e)
            self.writeError("邮件发送错误:\n"+str(e))
        finally:
            if s is not None:
                s.quit()

    # 写入发送错误日志
    def writeError(self, errorContent):
        file_handle = open('log.txt', mode='r+',encoding='utf-8')
        old = file_handle.read()
        file_handle.seek(0)
        file_handle.write('\n')
        file_handle.write('='*100)
        file_handle.write('\n')
        file_handle.write(time.ctime())
        file_handle.write('\n')
        file_handle.write(errorContent)
        file_handle.write('\n')
        file_handle.write('='*100)
        file_handle.write('\n')
        file_handle.write(old)
        file_handle.close()

if __name__ == '__main__':
    mail = email()
    subject = "吴晓涵大傻逼"  # 主题
    content = "邮件内容，吴晓涵是大傻逼，哈哈哈"
    mail.send(subject,content)
