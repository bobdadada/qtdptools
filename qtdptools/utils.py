__all__ = ['CurAbsPathFrom', 'ValueReturnedError', 'validateRet', 'selectFile', 'saveBakeupFile']

import os
import shutil

class CurAbsPathFrom:
    """
    Class get the absolute path starting from a certain path.

    example:
    ```
    curAbsPathfunc = CurAbsPathFrom('.')
    print(curAbsPathfunc('test'))
    ```
    """
    def __init__(self, startpath):
        self.startpath = os.path.abspath(startpath)

    def __call__(self, *paths):
        return os.path.join(self.startpath, *paths)

class ValueReturnedError(Exception):
    """
    raise ReturnError when a function return values with wrong types
    """

def validateRet(var, errinfo='', types=None, default=None, except_ok=False):
    """
    valudate the value returned by a function
    """
    if types is None:
        if var is None:
            if not except_ok:
                raise ValueReturnedError(errinfo)
            else:
                return default
        else:
            return var
    else:
        if not isinstance(var, types):
            if not except_ok:
                raise ValueReturnedError(errinfo)
            else:
                return default
        else:
            return var

def selectFile(files, notfound_ok=True):
    """
    Select one file in files which exists. If notfound_ok is True, then last file path will 
    be selected will be select if none of files exists. Else FileNotFoundError will be raised.
    """
    if not files:
        raise Exception('the argument files must be a sequence contain path objects')

    for file in files:
        if os.path.isfile(file):
            return file
    else:
        if notfound_ok:
            return file
        else:
            raise FileNotFoundError('file not found')

def saveBakeupFile(file, bakfile=None, exist_ok=True):
    """
    Back up important files to prevent operating errors.
    """
    if bakfile is None:
        bakfile = file + '.bak'
    if (not exist_ok) and os.path.exists(bakfile):
        raise FileExistsError(bakfile+' exists')
    shutil.copy(file, bakfile)
