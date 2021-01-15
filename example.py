from setenum import SetEnum

class PythonDependencies(SetEnum):
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



def asd(x: str):
    pass

asd(Dependencies.DJANGO.value)