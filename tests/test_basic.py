import pytest
from setenum import SetEnum, includes

# Example SetEnums

class PythonDependencies(SetEnum):
    DJANGO = 'django'
    FLASK = 'flask'
    FASTAPI = 'fastapi'


@includes(PythonDependencies)
class Dependencies(SetEnum):
    NGINX = 'nginx'
    NODEJS = 'nodejs'


def test_compare_to_superset():
    assert PythonDependencies.DJANGO in Dependencies
    assert PythonDependencies.DJANGO == Dependencies.DJANGO
    

def test_lookup_superset_in_subset():
    assert Dependencies.DJANGO in PythonDependencies
    assert Dependencies.NGINX not in PythonDependencies


def test_is():
    assert PythonDependencies.DJANGO is Dependencies.DJANGO


@pytest.mark.xfail(reason='Not implemented yet')
def test_insinstance():
    assert isinstance(PythonDependencies.DJANGO, Dependencies)
    assert issubclass(PythonDependencies, Dependencies)
