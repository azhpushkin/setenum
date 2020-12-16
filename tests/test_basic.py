import pytest
from setenum import SetEnum, as_superset_of

# Example SetEnums

class PythonDependencies(SetEnum):
    DJANGO = 'django'
    FLASK = 'flask'
    FASTAPI = 'fastapi'


@as_superset_of(PythonDependencies)
class Dependencies(SetEnum):
    NGINX = 'nginx'
    NODEJS = 'nodejs'


print(isinstance(PythonDependencies.DJANGO, Dependencies))


def test_compare_to_superset():
    assert PythonDependencies.DJANGO in Dependencies
    assert PythonDependencies.DJANGO == Dependencies.DJANGO
    

def test_lookup_superset_in_subset():
    assert Dependencies.DJANGO in PythonDependencies
    assert Dependencies.NGINX not in PythonDependencies


def test_is():
    assert PythonDependencies.DJANGO is Dependencies.DJANGO


def test_insinstance():
    assert isinstance(PythonDependencies.DJANGO, Dependencies)
