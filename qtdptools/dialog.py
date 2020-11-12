
__all__ = ['BugReportDialog']

from qtpy.QtWidgets import QDialog, QVBoxLayout, QMessageBox
from qtpy.QtCore import Signal

from qtdptools.widget.EmailReport import EmailReport

class BugReportDialog(QDialog):
    bugIgnoredSignal = Signal()

    def __init__(self, info='', report='', toemail=None, fromemail=None, password=None, server=None, port=25, 
                        subject='Report', parent=None):
        super().__init__(parent=parent)

        mainLayout = QVBoxLayout(self)
        self.setWindowTitle('BUG!')

        self.emailReport = EmailReport(info=info, report=report, toemail=toemail, fromemail=fromemail,
                        password=password, server=server, port=25,
                        subject=subject, parent=self)
        self.emailReport.emailSentSignal.connect(self.close)

        mainLayout.addWidget(self.emailReport)
    
    def closeEvent(self, ev):
        reply = QMessageBox.question(self, '询问', '是否忽略此问题？',
                    QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.bugIgnoredSignal.emit()
        ev.accept()
