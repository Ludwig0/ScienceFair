import threading


class RestartableThread(threading.Thread):
    ''' A thread that can clone itself so that it can "restart"

    Made out of the fact that a thread cannot start again after it has called join()

    Usage:
    use the clone() method to effectively recreate the same thread

    Example Code:
    x = RestartableThread()
    // implementation omitted //
    x.join()
    x = x.clone()
    x.start()

    '''
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        super().__init__(*args, **kwargs)

    def clone(self):
        return RestartableThread(*self.args, **self.kwargs)