__all__ = ['TimingUpdater']

from qtpy.QtCore import QTimer

class TimingUpdater(QTimer):
    """
    以定时器的方式启动一系列任务，任务不易过大

    proprety:
        _tasks-保存的任务列表，任务以函数的形式存在

    method:
        add_task-添加任务
        del_task-删除任务
        tasks-获取任务表
        runTasksOnce-运行一次任务
        stopAndRunTasksOnce-停止定时器并运行一次任务表
    """
    def __init__(self, tasks=None, parent=None):
        super().__init__(parent=parent)
        
        if tasks is None:
            self._tasks = set()
        else:
            self._tasks = set(tasks)

        self.timeout.connect(self.runTasksOnce)
    
    def add_task(self, task):
        self._tasks.add(task)
        return task
    
    def del_task(self, task):
        if task in self._tasks:
            self._tasks.remove(task)

    def tasks(self):
        return self._tasks.copy()

    def runTasksOnce(self):
        tasks = self._tasks.copy()
        for task in tasks:
            task()

    def stopAndRunTasksOnce(self):
        self.stop()
        self.runTasksOnce()
