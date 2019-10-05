from invoke import Collection, Program
from guilder import tasks

namespace = Collection.from_module(tasks)
program = Program(namespace=namespace, version='0.1')
