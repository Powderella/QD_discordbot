import time
import functools
import os

def processingTimeDecorator(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        run = time.time()
        result = f(*args, **kwargs)
        elapse = time.time() - run
        print(f"{f.__name__}は{elapse:.4}秒かかりました。")
        return result
    return wrapper

def setupDirectory(filepath):
    dirpath = os.path.split(filepath)[0]
    if dirpath is None:
        return
    os.makedirs(dirpath, exist_ok=True)
