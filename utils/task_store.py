from queue import Queue
from threading import Lock, Event

task_queue = Queue()
tasks = {}

tasks_lock = Lock()
stop_event = Event()
