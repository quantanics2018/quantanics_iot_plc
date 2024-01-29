import asyncio

def abc():

    for i in range(100):

        print(i)

def defg():

    for i in range(10):

        print(i)

task1 = asyncio.create_task(abc())
task2 = asyncio.create_task(defg())
results = asyncio.gather(task1, task2)