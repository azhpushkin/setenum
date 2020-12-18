class SupportContains(type):
    def __contains__(self, member: object) -> bool: ...


class Dependencies(metaclass=SupportContains):
    DJANGO: X
    FLASK: X
    NGINX: Dependencies
    NODEJS: Dependencies


class PythonDependencies(metaclass=SupportContains):
    DJANGO: X
    FLASK: X


class X(Dependencies, PythonDependencies):
    pass




