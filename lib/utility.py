import time
import functools
import os
import asyncio
import aiohttp

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

async def download(session, url, savepath, max_size, chunk_size=1024):
    """maxsize:単位KB
    """
    downloaded_size = 0
    async with session.get(url, timeout=None) as r:
        with open(savepath, "wb") as f:
            while True:
                chunk = await r.content.read(chunk_size)
                if not chunk or (downloaded_size / 1024) > max_size:
                    break
                f.write(chunk)
                downloaded_size += chunk_size
                print(f"{downloaded_size}/{len(r.content)}")