__all__ = ['open_lockfile', 'QSharedApplication', 'QSingleApplication']

from contextlib import contextmanager

from qtpy.QtCore import QLockFile, QSharedMemory, Signal, Qt, QTextStream
from qtpy.QtNetwork import QLocalServer, QLocalSocket
from qtpy.QtWidgets import QApplication

@contextmanager
def open_lockfile(lockfilename):
    lockfile = QLockFile(lockfilename)
    try:
        yield lockfile
    finally:
        lockfile.unlock()

class QSharedApplication(QApplication):
    """
    See https://github.com/PyQt5/PyQt/blob/master/Demo/Lib/Application.py
    
    Example:
    ```
    import sys, os
    print(os.getpid())

    appid = 'F3FF80BA-BA05-4277-8063-82A6DB9245A2'
    app = QSharedApplication(appid, sys.argv)
    if app.isRunning():
        sys.exit(0)

    w = Widget()
    w.show()
    sys.exit(app.exec_())
    ```
    """

    def __init__(self, appid, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._isRunning = False
        self._memory =  QSharedMemory('SharedApplication:'+appid, self)

        # 如果进程附加在共享内存上，先取消进程附加在共享内存，以防系统错误时进程没清理干净
        if self._memory.isAttached():
            self._memory.detach()
        
        if self._memory.create(1) and self._memory.error() != QSharedMemory.AlreadyExists:
            # 创建共享内存。如果创建失败，则说明已经创建，否则未创建
            pass
        else:
            self._isRunning = True
            del self._memory  # 计数减一
    
    def isRunning(self):
        return self._isRunning

class QSingleApplication(QApplication):
    """
    See https://github.com/PyQt5/PyQt/blob/master/Demo/Lib/Application.py
    and https://stackoverflow.com/questions/12712360/qtsingleapplication-for-pyside-or-pyqt
    
    Example:
    ```
    import sys
    from PySide.QtGui import *

    appid = 'F3FF80BA-BA05-4277-8063-82A6DB9245A2'
    app = QSingleApplication(appid, sys.argv)
    if app.isRunning():
        sys.exit(0)

    w = QWidget()
    w.show()
    app.setActivationWindow(w)
    sys.exit(app.exec_())
    ```
    """
    messageReceived = Signal(str)

    def __init__(self, appid, *args, **kwargs):
        
        super().__init__(*args, **kwargs)

        self._socketName = 'SingleApplication:'+appid
        self._activationWindow = None
        self._activateOnMessage = False
        self._socketServer = None
        self._socketIn = None
        self._streamIn = None
        self._socketOut = None
        self._streamOut = None
        self._isRunning = False

        # 先尝试连接
        self._socketOut = QLocalSocket(self)
        self._socketOut.connectToServer(self._socketName)
        self._socketOut.error.connect(self.handleError)
        self._isRunning = self._socketOut.waitForConnected()

        if self._isRunning:  # 程序运行
            self._streamOut = QTextStream(self._socketOut)
            self._streamOut.setCodec('utf-8')
        else:
            self._socketOut.close()
            self._socketOut = None
            self._socketServer = QLocalServer(self)
            self._socketServer.listen(self._socketName)
            self._socketServer.newConnection.connect(self._onNewConnection)
            self.aboutToQuit.connect(self.removeServer)
    
    def handleError(self, message):
        print("handleError message:", message)

    def isRunning(self):
        return self._isRunning

    def activationWindow(self):
        return self._activationWindow

    def setActivationWindow(self, activationWindow, activateOnMessage=True):
        self._activationWindow = activationWindow
        self._activateOnMessage = activateOnMessage

    def activateWindow(self):
        if not self._activationWindow:
            return
        self._activationWindow.setWindowState(
            self._activationWindow.windowState() & ~Qt.WindowMinimized)
        self._activationWindow.raise_()
        self._activationWindow.activateWindow()

    def sendMessage(self, message, msecs=5000):
        if not self._streamOut:
            return False
        self._streamOut << message << '\n'
        self._streamOut.flush()
        if not self._socketOut.waitForBytesWritten(msecs):
            raise RuntimeError("Bytes not written within %ss"%(msecs/1000))
        return True

    def _onNewConnection(self):
        if self._socketIn:
            self._socketIn.readyRead.disconnect(self._onReadyRead)
        self._socketIn = self._socketServer.nextPendingConnection()
        if not self._socketIn:
            return
        self._streamIn = QTextStream(self._socketIn)
        self._streamIn.setCodec('utf-8')
        self._socketIn.readyRead.connect(self._onReadyRead)
        if self._activateOnMessage:
            self.activateWindow()
    
    def _onReadyRead(self):
        while True:
            message = self._streamIn.readLine()
            if not message:
                break
            self.messageReceived.emit(message)

    def removeServer(self):
        self._socketServer.close()
        self._socketServer.removeServer(self._socketName)
