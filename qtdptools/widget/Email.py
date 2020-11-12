
__all__ = ['Email']

from qtpy.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QLabel, QHBoxLayout
from qtpy.QtCore import QRegExp
from qtpy.QtGui import QRegExpValidator

class Email(QWidget):

    def __init__(self, email=None, password=None, server=None, port=25, parent=None):
        super().__init__(parent=parent)

        self._email = email
        self._password = password
        self._server = server
        self._port = port

        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        # server widget
        serverportWidget = QWidget(self)
        serverportLayout = QHBoxLayout(serverportWidget)
        serverportLayout.setContentsMargins(10, 10, 10, 10)

        serverLabel = QLabel("SMTP服务器:")
        serverLabel.setStyleSheet("color:rgb(70,70,20); padding:10px;")

        self.serverLineEdit = QLineEdit(self._server)
        self.serverLineEdit.setValidator(QRegExpValidator(QRegExp(r"[\w\-_]+(\.[\w\-_]+)+")))
        self.serverLineEdit.setPlaceholderText("SMTP服务器地址")
        self.serverLineEdit.textChanged.connect(self._setServer)

        portLabel = QLabel("端口:")
        portLabel.setStyleSheet("color:rgb(70,70,20); padding:10px;")

        self.portLineEdit = QLineEdit(str(self._port))
        self.portLineEdit.setValidator(QRegExpValidator(QRegExp(r"^[0-9]+$")))
        self.portLineEdit.setPlaceholderText("端口号")
        self.portLineEdit.textChanged.connect(self._setPort)

        serverportLayout.addWidget(serverLabel)
        serverportLayout.addWidget(self.serverLineEdit)
        serverportLayout.addWidget(portLabel)
        serverportLayout.addWidget(self.portLineEdit)
        serverportLayout.setStretch(0, 1)
        serverportLayout.setStretch(1, 5)
        serverportLayout.setStretch(2, 1)
        serverportLayout.setStretch(3, 1)

        # email widget
        emailWidget = QWidget(self)
        emailLayout = QHBoxLayout(emailWidget)
        emailLayout.setContentsMargins(0, 0, 0, 0)

        emailLabel = QLabel("邮箱:")
        emailLabel.setStyleSheet("color:rgb(70,70,20); padding:10px;")

        self.emailLineEdit = QLineEdit(self._email)
        self.emailLineEdit.setValidator(QRegExpValidator(
            QRegExp("^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\\.[a-zA-Z0-9_-]+)+$")))
        self.emailLineEdit.setPlaceholderText("请输入邮箱地址")
        self.emailLineEdit.textChanged.connect(self._setEmail)

        emailLayout.addWidget(emailLabel)
        emailLayout.addWidget(self.emailLineEdit)

        # password widget
        passwordWidget = QWidget(self)
        passwordLayout = QHBoxLayout(passwordWidget)
        passwordLayout.setContentsMargins(0, 0, 0, 0)

        passwordLabel = QLabel("密码:")
        passwordLabel.setStyleSheet("color:rgb(70,70,20); padding:10px;")

        self.passwordLineEdit = QLineEdit(self._password)
        self.passwordLineEdit.setPlaceholderText("请输入密码")
        self.passwordLineEdit.textChanged.connect(self._setPassword)
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)

        passwordLayout.addWidget(passwordLabel)
        passwordLayout.addWidget(self.passwordLineEdit)

        # 插入widget
        mainLayout.addWidget(serverportWidget)
        mainLayout.addWidget(emailWidget)
        mainLayout.addWidget(passwordWidget)

    def server(self):
        return self._server

    def _setServer(self, server):
        self._server = server
    
    def setServer(self, server):
        self.serverLineEdit.setText(server)

    def port(self):
        return self._port

    def _setPort(self, port):
        self._port = int(port)
    
    def setPort(self, port):
        self.portLineEdit.setText(str(port))

    def email(self):
        return self._email

    def _setEmail(self, email):
        self._email = email
    
    def setEmail(self, email):
        self.emailLineEdit.setText(email)
    
    def password(self):
        return self._password

    def _setPassword(self, password):
        self._password = password
    
    def setPassword(self, password):
        self.passwordLineEdit.setText(password)


if __name__ == '__main__':
    import sys
    from qtpy.QtWidgets import QApplication

    app = QApplication(sys.argv)
    
    widget =  Email()

    widget.show()
    
    sys.exit(app.exec())