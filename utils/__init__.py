import time


def log(*args, **kwargs):
    formats = '%y-%m-%d-%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(formats, value)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


def format_time():
    formats = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(formats, value)
    return dt


def paginate(ds, page=1, pre_page=8):
    if page in (None, 0):
        page = 1
    start = page * pre_page - pre_page
    end = start + pre_page
    items = []
    for i in range(start, end):
        if i >= len(ds):
            break
        items.append(ds[i])
    r = dict(
        sum_page=int(len(ds) / 8) + 1,
        current_page=page,
        items=items
    )
    return r
