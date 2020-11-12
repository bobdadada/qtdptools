__all__ = ['tightenWindow']

from qtpy.QtWidgets import QStyle
from qtpy.QtCore import Qt, QSize

def tightenWindow(window, width, height, wscale=0.9, hscale=0.9):
    """
    窗口居中，且设置合适尺寸
    """
    availableScreenQrect = window.screen().availableGeometry()
    width0, height0 = availableScreenQrect.width(), availableScreenQrect.height()

    width = min(width, int(width0*wscale))
    height = min(height, int(height0*hscale))

    geometry = QStyle.alignedRect(Qt.LeftToRight, 
                        Qt.AlignCenter, 
                        QSize(width,height), 
                        availableScreenQrect)
    window.setGeometry(geometry)