__all__ = ['NonstopDo', 'SingleDo', 'SuccessiveDo', 'ExtFileOpenThread']

import os

from qtpy.QtCore import QThread, Signal

# 持续更新的线程对象
class NonstopDo(QThread):
    """
    创建持续更新的线程对象，帮助持续更新目标函数

    proprety:
        working-工作状态，True可运行，False不可运行，类似于标准库中threading.Event
        fun-目标函数，无传递参数
        intervalms-更新的时间间隔，时间间隔必须大于0，否则无法启动

    method:
        __init__-初始化线程
        __del__-线程退出
        stopSafely-线程安全退出
        delSafely-线程安全退出
        restart-重新运行，主要用于设置工作状态working为True
        run-线程运行
    """

    def __init__(self, fun, intervalms=10):
        super(NonstopDo, self).__init__()
        self.working = True  # 线程退出标志
        self.fun = fun
        self.intervalms = intervalms

    def __del__(self):
        self.working = False
    
    def delSafely(self):
        self.working = False
        self.wait()
    
    def stopSafely(self):
        self.delSafely()
    
    def restart(self, priority=QThread.InheritPriority):
        self.working = True
        self.start(priority)

    def run(self):
        while self.working:
            self.fun()
            self.msleep(self.intervalms)


# 单次运行的线程对象
class SingleDo(QThread):
    """
    创建单次运行的线程对象，帮助运行耗时的IO读写操作

    proprety:
        fun-目标函数
        intervalms-更新的时间间隔
        args-传递的位置参数
        kwargs-传递的命名参数
        ret-函数返回值

    method:
         __init__-初始化线程
        __del__-线程安全退出
        run-线程运行
    """
    doneSignal = Signal(object)

    def __init__(self, fun, *args, **kwargs):
        super(SingleDo, self).__init__()
        self.fun = fun
        self.args = args
        self.kwargs = kwargs
        self.ret = None

    def run(self):
        self.ret = self.fun(*self.args, **self.kwargs)
        self.doneSignal.emit(self.ret)


# 相继运行几个步骤，直到运行到最终步骤的线程对象
class SuccessiveDo(QThread):
    """
    创建需要运行多步的线程对象

    proprety:
        working-工作状态，True可运行，False不可运行，类似于标准库中threading.Event
        prefun-前处理函数，无传递参数，运行一次
        fun-目标函数，无传递参数，多步骤运行，返回True或者False
        lastfun-后处理函数，无传递参数，运行一次
        intervalms-更新的时间间隔，时间间隔必须大于0，否则无法启动

    method:
         __init__-初始化线程
        __del__-线程退出
        stopSafely-线程安全退出
        delSafely-线程安全退出
        restart-重新运行，主要用于设置工作状态working为True
        run-线程运行
    """

    def __init__(self, fun, prefun=None, lastfun=None, intervalms=10):
        super(SuccessiveDo, self).__init__()
        self.fun = fun
        self.prefun = prefun
        self.lastfun = lastfun
        self.intervalms = intervalms
        self.working = True  # 线程退出标志

    def __del__(self):
        self.working = False
    
    def delSafely(self):
        self.working = False
        self.wait()

    def stopSafely(self):
        self.delSafely()

    def restart(self, priority=QThread.InheritPriority):
        self.working = True
        self.start(priority)

    def run(self):
        if self.prefun:
            self.prefun()
        while self.working:
            if self.fun():
                self.working = False
            self.msleep(self.intervalms)
        if self.lastfun:
            self.lastfun()


# 打开外部文件
class ExtFileOpenThread(QThread):
    """
    Thread which opens an extern file.
    """
    finishedSignal = Signal(object)
    fileNotFoundSignal = Signal()

    def __init__(self, filename):
        super().__init__()

        self.filename = filename

    def run(self):
        self.setPriority(QThread.LowPriority)
        if not os.path.isfile(self.filename):
            self.fileNotFoundSignal.emit()
        else:
            try:
                os.startfile(self.filename, operation='open')
            except:
                pass
        self.finishedSignal.emit(self)
        super().run()
