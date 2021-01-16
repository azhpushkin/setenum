from setenum import SetEnum


class PythonDependencies(SetEnum):
    # __supersets__ = (Dependencies, )
    DJANGO = 'django'
    FLASK = 'flask'
    
class Dependencies(SetEnum):
    __subsets__ = (PythonDependencies, )
    NGINX = 'nginx'
    NODEJS = 'nodejs'



def foo(x: Dependencies):
    return x


def bar(x: PythonDependencies):
    return x


foo(PythonDependencies.DJANGO)
bar(PythonDependencies.DJANGO)
assert Dependencies.NGINX not in PythonDependencies
assert Dependencies.DJANGO in PythonDependencies


# TODO: how this check works?
from enum import Enum
class X(Enum):
    A, B = range(2)
    C, D = ('asd' for _ in range(2))

def asd(x: int):
    pass

asd(X.A.value)