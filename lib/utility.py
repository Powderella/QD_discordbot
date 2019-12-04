import time
import functools
def processingTimeDecorator(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        run = time.time()
        result = f(*args, **kwargs)
        elapse = time.time() - run
        print(f"{f.__name__}は{elapse:.4}秒かかりました。")
        return result
    return wrapper