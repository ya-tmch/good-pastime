class Task:
    def __init__(self, n, d, n1, interval):
        self.n = n
        self.d = d
        self.n1 = n1
        self.interval = interval

    def __str__(self):
        return "Task({}/{}/{}/{})".format(self.n, self.d, self.n1, self.interval)
