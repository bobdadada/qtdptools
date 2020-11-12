"""
使用SingleDo此线程子类完成显示时间的功能
"""

import datetime
from qtpy import QtWidgets

from qtdptools.thread import SingleDo

# 创建Application
app = QtWidgets.QApplication([])
w = QtWidgets.QDialog()
ly = QtWidgets.QVBoxLayout(w)

# 创建文本框和停止按钮
textbrowser = QtWidgets.QTextBrowser()
button = QtWidgets.QPushButton('PUSH')
ly.addWidget(textbrowser)
ly.addWidget(button)


# 按钮事件
def button_event():
    def f():        
        return str(datetime.datetime.now())
    def g(s):
        textbrowser.append(s)
    singledo = SingleDo(f)
    singledo.doneSignal.connect(g)
    singledo.start()
    singledo.wait()
button.clicked.connect(button_event)

# 显示窗口
w.show()

app.exec()
