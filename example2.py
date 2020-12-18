from example import *


def foo(x: Dependencies):
    return x


def bar(x: PythonDependencies):
    return x


foo(PythonDependencies.DJANGO)
bar(Dependencies.DJANGO)
assert Dependencies.NGINX not in PythonDependencies
assert Dependencies.DJANGO in PythonDependencies



from enum import Enum
class Q(Enum):
    A = 1


Q(Q.A)
assert Q.A in Q