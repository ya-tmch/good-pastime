import asyncio
from aiohttp import web
from task import Task
from job import Job

WORKERS_COUNT = 1

queue = []
events = {}
workers_is_up = False
routes = web.RouteTableDef()


@routes.post('/api/v1/tasks')
async def add_task(request):
    """Add task to queue"""

    # TODO Input validator
    task = Task(
        int(request.query.getone("n")),
        float(request.query.getone("d")),
        float(request.query.getone("n1")),
        float(request.query.getone("interval"))
    )

    await asyncio.shield(emit_new_job(Job(task)))

    return web.json_response({}, status=202)


@routes.get('/api/v1/tasks')
async def get_tasks(request):
    """Get tasks"""
    data = []
    for job in queue:
        data.append(job.to_dict())

    return web.json_response({'data': data})


async def emit_new_job(job):
    """Emit new job"""
    global events
    global workers_is_up
    global queue

    print("Added new job: ", job)
    queue.append(job)

    if workers_is_up:
        print("Wake up all workers")
        for _, v in events.items():
            v.set()

        return
    else:
        workers_is_up = True

    print("Up workers")
    loop = asyncio.get_event_loop()

    for number in range(WORKERS_COUNT):
        worker_name = "worker_" + str(number)
        events[worker_name] = asyncio.Event()
        loop.create_task(start_worker(worker_name, queue, events[worker_name]))
        print("Added worker with name ", worker_name)


def get_waited_job(queue):
    """Get waited job"""
    print("Finding job...")
    for job in queue:
        print(job)

    for job in queue:
        if job._status == Job.STATUS_WAIT:
            print("Found!")
            print("")
            return job

    print("Not found!")
    print("")
    return None


async def start_worker(worker_name, queue, event):
    """Start worker with name"""
    print("Start worker: ", worker_name)

    while True:
        job = get_waited_job(queue)

        if job == None:
            print("Await event before: ", worker_name)
            event.clear()
            await event.wait()
            print("Await event end: ", worker_name)
            print("")
        else:
            print("Do job begin: ", worker_name)
            await job.execute()
            print("Do job end: ", worker_name)
            print("Remove job: ", job)
            print("")
            queue.remove(job)

if __name__ == '__main__':
    # TODO Graceful shutdown
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app)
