__all__ = ['showQuickMessage', 'showMessage', 'openExtFile']

from qtpy.QtWidgets import QMessageBox
from qtpy.QtGui import QIcon
from qtdptools.messagebox import AutoCloseMessageBox
from qtdptools.thread import ExtFileOpenThread

class SubThreadsPool(object):
    def __init__(self):
        self._subthreads = set([])

    def add(self, thread):
        self._subthreads.add(thread)
    
    def remove(self, thread):
        if not thread.isFinished():
            thread.exit()
        self._subthreads.remove(thread)
    
    def removeAll(self):
        for t in self._subthreads:
            t.exit()
        self._subthreads.clear()
    
    def __del__(self):
        self.removeAll()

# private threads pool
_SUBTHREADSPOOL = SubThreadsPool()

def showQuickMessage(timeout=5000, title="", text="", icon=QMessageBox.NoIcon,
                    parent=None, *args, **kwargs):
    """
    Show a message box that can be closed automatically after a certain period of time.
    """
    msg = AutoCloseMessageBox(timeout=timeout, title=title, text=text,
                    icon=icon, parent=parent, *args, **kwargs)
    msg.exec()

def showMessage(title='', text='', icon=QMessageBox.NoIcon, windowIcon=QIcon(''), parent=None):
    """
    Show a message box.
    """
    message = QMessageBox(parent=parent)
    message.setWindowIcon(windowIcon)
    message.setIcon(icon)
    message.setWindowTitle(title)
    message.setText(text)
    message.setStandardButtons(QMessageBox.Ok)
    message.exec()

def openExtFile(filename, windowIcon=QIcon('')):
    """
    Open extern file by os.startfile.
    """
    def showFileNotFoundMessage():
        showMessage(title="Error", 
                text="本地没有文件%s"%filename,
                icon=QMessageBox.Warning,
                windowIcon=windowIcon)

    thr = ExtFileOpenThread(filename)
    thr.fileNotFoundSignal.connect(showFileNotFoundMessage)

    _SUBTHREADSPOOL.add(thr)
    thr.finishedSignal.connect(_SUBTHREADSPOOL.remove)

    thr.start()
