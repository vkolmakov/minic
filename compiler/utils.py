from datetime import datetime


def is_iterable(obj):
    return hasattr(obj, '__iter__')


class Logger:
    def __init__(self, write_fn=print, to_file=None):  # noqa
        if not to_file:
            self.write_output = write_fn
        else:
            file_obj = open(to_file, 'w+')
            self.write_output = file_obj.write

    def log_result(self, event):
        '''Used as a decorator'''
        def wrapper(f):
            def log_wrapped(*args, **kwargs):
                msg = f(*args, **kwargs)
                self.log(event, msg)
                return msg
            return log_wrapped
        return wrapper

    def log(self, event, msg=''):
        header = '[{}]-{}\n'.format(datetime.now(), event)
        separator = '*' * (len(header) - 1) + '\n'
        self.write_output(
            separator +
            header +
            separator +
            str(msg) +
            '\n'
        )
