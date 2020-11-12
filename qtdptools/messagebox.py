__all__ = ['AutoCloseMessageBox']

from qtpy.QtCore import QTimer
from qtpy.QtWidgets import QMessageBox

# Auto close MessageBox
class AutoCloseMessageBox(QMessageBox):
    """
    Message box that can be closed automatically after a certain period of time.
    """
    def __init__(self, timeout=5000, title="", text="", icon=QMessageBox.NoIcon,
                    parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setText(text)
        self.setWindowTitle(title)
        self.setIcon(icon)

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)

        self.timer.singleShot(timeout, self.close)  # 默认显示5s
