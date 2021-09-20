
import textwrap
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from PyQt5.QtWidgets import QTextEdit

from qtpy.QtWidgets import QWidget, QLineEdit, QFrame, QMessageBox, QProgressBar, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
from qtpy.QtCore import Qt, Signal
from qtpy.QtGui import QFont

from qtdptools.widgets.EmailServer import EmailServer
from qtdptools.show_utils import showQuickMessage

__all__ = ['Email']


class Email(QWidget):
    emailSentSignal = Signal()

    def __init__(self, content='', subject='Report', toemail=None, fromemail=None, password=None, server=None,
                 port=25, SSL=False, parent=None):
        super().__init__(parent=parent)

        self._content = str(content)
        self._subject = str(subject)
        self._toemail = str(toemail)

        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        self.setStyleSheet("background-color: white;")

        # subject
        self.subjectText = QLineEdit()
        self.subjectText.setPlaceholderText('email subject')
        self.subjectText.setText(str(subject))

        # content
        self.contentText = QTextEdit()
        self.contentText.setText(str(content))

        # 邮件地址
        self.emailWidget = EmailServer(
            email=fromemail, password=password, server=server, port=port, SSL=SSL, parent=self)

        # 邮件发送按钮
        buttonLayout = QHBoxLayout()
        buttonLayout.setContentsMargins(10, 10, 10, 10)
        buttonLayout.setSpacing(0)
        buttonLayout.setAlignment(Qt.AlignHCenter)

        emailSendButton = QPushButton()
        emailSendButton.setText("发送邮件")
        # 绑定点击事件处理函数
        emailSendButton.clicked.connect(self.sendEmail)
        emailSendButton.setStyleSheet(
            "QPushButton{font:63 11pt 微软雅黑;border:0px; border-radius:3px; color:#FFFFFF; background-color:#2278C6}"
            "QPushButton:hover{font:63 11pt 微软雅黑;border:0px; border-radius:3px;background-color:#1891FF;}"
        )

        buttonLayout.addWidget(emailSendButton)

        # 进度条
        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0, 10)
        self.progressBar.setTextVisible(False)
        self.progressBar.setMaximumHeight(5)

        # 将控件放入布局中
        mainLayout.addWidget(self.subjectText)
        mainLayout.addWidget(self.contentText)
        mainLayout.addWidget(self.emailWidget)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addWidget(self.progressBar)

    def sendEmail(self):
        successFlag = True

        subject = self.subject()
        content = self.content()
        toemail = self.toemail()
        server = self.server()
        port = self.port()
        SSL = self.SSL()
        fromemail = self.fromemail()
        password = self.password()
        self.progressBar.setValue(2)

        if successFlag:
            try:
                message = MIMEText(content, 'plain', 'utf-8')
                message['From'] = Header(formataddr(
                    ('Reporter', fromemail)), 'utf-8')   # 发送者
                message['To'] = Header(formataddr(
                    ('Handler', toemail)), 'utf-8')    # 接收者
                message['Subject'] = Header(subject, 'utf-8')
                self.progressBar.setValue(4)
            except:
                showQuickMessage(title='error', text='请输入合法的邮件内容',
                                 icon=QMessageBox.Critical, parent=self)
                successFlag = False

        if successFlag:                
            try:
                if SSL:
                    smtpObj = smtplib.SMTP_SSL(server, port)
                else:
                    smtpObj = smtplib.SMTP(server, port)
                smtpObj.login(fromemail, password)
                self.progressBar.setValue(6)
                smtpObj.sendmail(fromemail, [toemail], message.as_string())
                self.progressBar.setValue(10)
                showQuickMessage(title='info', text="邮件发送完成",
                                 icon=QMessageBox.Information, parent=self)
                smtpObj.close()
            except:
                showQuickMessage(title='error',
                                 text=textwrap.dedent("""
                            邮件发送失败，请检查
                            1)网络是否连接。
                            2)邮箱账号密码是否输入正确
                            3)邮箱是否与服务器对应"""),
                                 icon=QMessageBox.Critical,
                                 parent=self)
                successFlag = False


        if successFlag:
            self.emailSentSignal.emit()

        self.progressBar.reset()

    def subject(self):
        return self.subjectText.text()

    def setSubject(self, subject):
        self.subjectText.setText(str(subject))

    def content(self):
        return self.contentText.toPlainText()

    def setContent(self, content):
        self.contentText.setText(str(content))

    def server(self):
        return self.emailWidget.server()

    def setServer(self, server):
        self.emailWidget.setServer(server)

    def port(self):
        return self.emailWidget.port()

    def setPort(self, port):
        self.emailWidget.setPort(port)
    
    def SSL(self):
        return self.emailWidget.SSL()
    
    def setSSL(self, SSL):
        self.emailWidget.setSSL(SSL)

    def fromemail(self):
        return self.emailWidget.email()

    def setFromemail(self, email):
        self.emailWidget.setEmail(email)

    def toemail(self):
        return self._toemail

    def setToemail(self, email):
        self._toemail = email

    def password(self):
        return self.emailWidget.password()

    def setPassword(self, password):
        self.emailWidget.setPassword(password)


if __name__ == '__main__':
    import sys
    from qtpy.QtWidgets import QApplication, QMainWindow

    app = QApplication(sys.argv)

    window = QMainWindow()

    widget = Email()
    widget.setSubject('Email类测试')
    widget.setContent("""
    测试长文本!
    测试长文本
    测试长文
    测试长
    测试
    测
    """)
    widget.setToemail("baoxy@mail.ustc.edu.cn")
    widget.setServer("mail.ustc.edu.cn")
    widget.setPort(465)
    widget.setSSL(True)
    widget.setFromemail("baoxy@mail.ustc.edu.cn")

    window.setCentralWidget(widget)
    window.show()

    sys.exit(app.exec())
