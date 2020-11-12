
import textwrap
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

from qtpy.QtWidgets import QWidget, QFrame, QMessageBox, QProgressBar, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
from qtpy.QtCore import Qt, Signal
from qtpy.QtGui import QFont

from qtdptools.widget.Email import Email
from qtdptools.show_utils import showQuickMessage

__all__ = ['EmailReport']

class EmailReport(QWidget):
    emailSentSignal = Signal()
    
    def __init__(self, info='', report='', toemail=None, fromemail=None, password=None, server=None, port=25, 
                        subject='Report', parent=None):
        super().__init__(parent=parent)

        self._info = str(info)  # infomation reported
        self._report  = str(report)  # report
        self._toemail = str(toemail)
        self._subject = str(subject)

        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        self.setStyleSheet("background-color: white;")

        # information
        self.infoText = QLabel(self._info)
        self.infoText.setWordWrap(True)
        self.infoText.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.infoText.setFont(QFont('Mcorsoft YaHei', 11, 50))
        self.infoText.setStyleSheet("color:rgb(130,130,130); padding:10px;")
        self.infoText.setFrameStyle(QFrame.Box|QFrame.Raised)

        # report
        self.reportText = QLabel(self._report)
        self.reportText.setWordWrap(True)
        self.reportText.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.reportText.setFont(QFont('Mcorsoft YaHei', 11, 50))
        self.reportText.setStyleSheet("color:rgb(130,130,130); padding:10px;")
        self.reportText.setFrameStyle(QFrame.Box|QFrame.Raised)
        self.reportText.hide()

        # 邮件地址
        self.emailWidget = Email(email=fromemail, password=password, server=server, port=port, parent=self)

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
        mainLayout.addWidget(self.infoText)
        mainLayout.addWidget(self.reportText)
        mainLayout.addWidget(self.emailWidget)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addWidget(self.progressBar)

    def sendEmail(self):
        successFlag = True

        subject = self.subject()
        report = self.report()
        toemail = self.toemail()
        server = self.server()
        port = self.port()
        fromemail = self.fromemail()
        password = self.password()
        self.progressBar.setValue(2)

        if successFlag:
            try:
                message = MIMEText(report, 'plain', 'utf-8')
                message['From'] = Header(formataddr(('Reporter', fromemail)), 'utf-8')   # 发送者
                message['To'] =  Header(formataddr(('Handler', toemail)), 'utf-8')    # 接收者
                message['Subject'] = Header(subject, 'utf-8')
                self.progressBar.setValue(4)
            except:
                showQuickMessage(title='error', text='请输入合法的邮箱', icon=QMessageBox.Critical, parent=self)
                successFlag = False

        if successFlag:
            try:
                with smtplib.SMTP() as smtpObj:
                    smtpObj.connect(server, port)
                    smtpObj.login(fromemail, password)
                    self.progressBar.setValue(6)
                    smtpObj.sendmail(fromemail, [toemail], message.as_string())
                    self.progressBar.setValue(10)
                showQuickMessage(title='info', text="邮件发送完成", icon=QMessageBox.Information, parent=self)
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
        return self._subject

    def setSubject(self, subject):
        self._subject = str(subject)

    def info(self):
        return self._info

    def setInfo(self, info):
        self._info = str(info)
        self.infoText.setText(self._info)
    
    def report(self):
        return self._report
    
    def setReport(self, report):
        self._report = str(report)
        self.reportText.setText(self._report)

    def setReportVisible(self, visible=True):
        if visible:
            self.reportText.show()
        else:
            self.reportText.hide()

    def showReport(self):
        self.setReportVisible(True)
    
    def hideReport(self):
        self.setReportVisible(False)
    
    def server(self):
        return self.emailWidget.server()
    
    def setServer(self, server):
        self.emailWidget.setServer(server)

    def port(self):
        return self.emailWidget.port()
    
    def setPort(self, port):
        self.emailWidget.setPort(port)

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
    
    widget =  EmailReport()
    widget.setInfo("""
    测试长文本!
    测试长文本
    测试长文
    测试长
    测试
    测
    """)
    widget.setToemail("baoxy@mail.ustc.edu.cn")
    widget.setServer("mail.ustc.edu.cn")
    #widget.setFromemail("baoxy@mail.ustc.edu.cn")

    widget.setReport("""
    秘密文本
    """)
    widget.setReportVisible(True)

    window.setCentralWidget(widget)
    window.show()
    
    sys.exit(app.exec())