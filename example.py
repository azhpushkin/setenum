from setenum import SetEnum

class PythonDependencies(SetEnum):
    DJANGO = 'django'
    FLASK = 'flask'


class Dependencies(SetEnum):
    __subsets__ = [PythonDependencies, ]
    NGINX = 'nginx'
    NODEJS = 'nodejs'


