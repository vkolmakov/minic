from datetime import datetime


def is_iterable(obj):
    return hasattr(obj, '__iter__')


class Logger:
    def __init__(self, write_fn=print, to_file=None):
        if not to_file:
            self.write_output = write_fn
        else:
            file_obj = open(to_file, 'w+')
            self.write_output = file_obj.write

    def log(self, event):
        def wrapper(f):
            def log_wrapped(*args, **kwargs):
                msg = f(*args, **kwargs)
                self.write_output(
                    '[{}]-{}\n'.format(datetime.now(), event) +
                    str(msg) +
                    '\n'
                )
                return msg
            return log_wrapped
        return wrapper
