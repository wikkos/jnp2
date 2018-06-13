from __future__ import absolute_import, unicode_literals

from django.conf import settings

# from .models import Submission

settings.configure()

import pika
import time
from celery import Celery, shared_task

#local testing: @127.0.0.1
app = Celery('tasks', broker='amqp://guest:guest@message-broker:5672//')
app.config_from_object('django.conf:settings')
print("INSIDE TASKS")

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    print("periodic")
    test.delay()
    #sender.add_periodic_task(2.0, test.s(), name='add every 10')

@app.task
@shared_task
def test():
    print("starting update task")
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='message-broker'))
    channel = connection.channel()

    channel.exchange_declare(exchange='exec_results',
                             exchange_type='fanout')

    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='exec_results',
                       queue=queue_name)

    def callback(ch, method, properties, body):
        print("Received!")
        print(" [x] %r" % body)
        sid = int(body)
        #Submission.objects.get(id=sid).update(status=Submission.OK)
        print("Finished callback")

    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)
    print("Listeningg")
    while True:
        print("Consuming", flush=True)
        channel.start_consuming()
