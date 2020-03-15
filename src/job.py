import asyncio
from datetime import datetime
from task import Task

last_id = 0


class Job:
    STATUS_WAIT = 'waiting'
    STATUS_RUN = 'running'

    @staticmethod
    def generateId():
        global last_id

        last_id += 1
        return last_id

    def __init__(self, task: Task):
        self._task = task
        self._number = Job.generateId()
        self._status = Job.STATUS_WAIT
        self._current_value = None
        self._start_date = str(datetime.now())

    async def execute(self):
        task = self._task
        self._status = Job.STATUS_RUN
        self._current_value = task.n1

        for _ in range(2, task.n + 1):
            print("sleep in execute", self)
            await asyncio.sleep(task.interval)

            # TODO Improve for IEEE 754
            self._current_value += task.d

        print("job finished with value ", self._current_value)

    def to_dict(self):
        return {
            "number": self._number,
            "status": self._status,
            "n": self._task.n,
            "d": self._task.d,
            "n1": self._task.n1,
            "interval": self._task.interval,
            "current_value": self._current_value,
            "start_date": self._start_date
        }

    def __str__(self):
        return "Job({}/{}/{})".format(self._number, self._status, self._current_value)
