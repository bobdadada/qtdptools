"""
使用NonstopDo此线程子类完成定时显示时间的功能
"""

import datetime
from qtpy import QtWidgets

from qtdptools.thread import NonstopDo

# 创建Application
app = QtWidgets.QApplication([])
w = QtWidgets.QDialog()
ly = QtWidgets.QVBoxLayout(w)

# 创建文本框和停止按钮
textbrowser = QtWidgets.QTextBrowser()
button = QtWidgets.QPushButton('STOP')
ly.addWidget(textbrowser)
ly.addWidget(button)

# 每隔2s更新日期
def f():
    textbrowser.append(str(datetime.datetime.now()))
nonstop = NonstopDo(f, 2000)

# 停止更新时间
def g():
    nonstop.working = False
    textbrowser.append('stop')
button.clicked.connect(g)

# 显示窗口
w.show()

# 启动NonstopDo线程
nonstop.start()

app.exec()
