def lazy(fn):
    def wrapper(*args, **kwargs):
        return lambda: fn(*args, **kwargs)

    return wrapper
