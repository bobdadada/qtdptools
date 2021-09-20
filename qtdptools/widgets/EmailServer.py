
from qtpy.QtWidgets import QWidget, QCheckBox, QLineEdit, QVBoxLayout, QLabel, QHBoxLayout
from qtpy.QtCore import QRegExp
from qtpy.QtGui import QRegExpValidator

__all__ = ['EmailServer']

class EmailServer(QWidget):

    def __init__(self, email=None, password=None, server=None, port=25, SSL=False, parent=None):
        super().__init__(parent=parent)

        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        # server widget
        serverportWidget = QWidget(self)
        serverportLayout = QHBoxLayout(serverportWidget)
        serverportLayout.setContentsMargins(10, 10, 10, 10)

        serverLabel = QLabel("SMTP服务器:")
        serverLabel.setStyleSheet("color:rgb(70,70,20); padding:10px;")

        self.serverLineEdit = QLineEdit()
        self.serverLineEdit.setValidator(QRegExpValidator(QRegExp(r"[\w\-_]+(\.[\w\-_]+)+")))
        self.serverLineEdit.setPlaceholderText("SMTP服务器地址")
        self.serverLineEdit.setText(server)

        portLabel = QLabel("端口:")
        portLabel.setStyleSheet("color:rgb(70,70,20); padding:10px;")

        self.portLineEdit = QLineEdit()
        self.portLineEdit.setValidator(QRegExpValidator(QRegExp(r"^[0-9]+$")))
        self.portLineEdit.setPlaceholderText("端口号")
        self.portLineEdit.setText(str(port))

        self.SSLCheckBox = QCheckBox("SSL")
        self.SSLCheckBox.setChecked(SSL)

        serverportLayout.addWidget(serverLabel)
        serverportLayout.addWidget(self.serverLineEdit)
        serverportLayout.addWidget(portLabel)
        serverportLayout.addWidget(self.portLineEdit)
        serverportLayout.addWidget(self.SSLCheckBox)
        serverportLayout.setStretch(0, 1)
        serverportLayout.setStretch(1, 5)
        serverportLayout.setStretch(2, 1)
        serverportLayout.setStretch(3, 1)
        serverportLayout.setStretch(4, 1)

        # email widget
        emailWidget = QWidget(self)
        emailLayout = QHBoxLayout(emailWidget)
        emailLayout.setContentsMargins(0, 0, 0, 0)

        emailLabel = QLabel("邮箱:")
        emailLabel.setStyleSheet("color:rgb(70,70,20); padding:10px;")

        self.emailLineEdit = QLineEdit()
        self.emailLineEdit.setValidator(QRegExpValidator(
            QRegExp("^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\\.[a-zA-Z0-9_-]+)+$")))
        self.emailLineEdit.setPlaceholderText("请输入邮箱地址")
        self.emailLineEdit.setText(email)

        emailLayout.addWidget(emailLabel)
        emailLayout.addWidget(self.emailLineEdit)

        # password widget
        passwordWidget = QWidget(self)
        passwordLayout = QHBoxLayout(passwordWidget)
        passwordLayout.setContentsMargins(0, 0, 0, 0)

        passwordLabel = QLabel("密码:")
        passwordLabel.setStyleSheet("color:rgb(70,70,20); padding:10px;")

        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setPlaceholderText("请输入密码")
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        self.passwordLineEdit.setText(password)

        passwordLayout.addWidget(passwordLabel)
        passwordLayout.addWidget(self.passwordLineEdit)

        # 插入widget
        mainLayout.addWidget(serverportWidget)
        mainLayout.addWidget(emailWidget)
        mainLayout.addWidget(passwordWidget)

    def server(self):
        return self.serverLineEdit.text()
    
    def setServer(self, server):
        self.serverLineEdit.setText(server)

    def port(self):
        return int(self.portLineEdit.text())

    def setPort(self, port):
        self.portLineEdit.setText(str(port))
    
    def SSL(self):
        return self.SSLCheckBox.isChecked()
    
    def setSSL(self, SSL):
        self.SSLCheckBox.setChecked(SSL)

    def email(self):
        return self.emailLineEdit.text()
    
    def setEmail(self, email):
        self.emailLineEdit.setText(email)
    
    def password(self):
        return self.passwordLineEdit.text()
    
    def setPassword(self, password):
        self.passwordLineEdit.setText(password)


if __name__ == '__main__':
    import sys
    from qtpy.QtWidgets import QApplication

    app = QApplication(sys.argv)

    widget = EmailServer(email='name@domian', password='testPassword', server='domain', port=25, SSL=True)

    widget.show()

    assert widget.server() == 'domain'
    assert widget.port() == 25
    assert widget.email() == 'name@domian'
    assert widget.password() == 'testPassword'
    assert widget.SSL() == True
    
    sys.exit(app.exec())
