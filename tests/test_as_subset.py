import pytest
from setenum import SetEnum, as_subset_of


class Dependencies(SetEnum):
    NGINX = 'nginx'
    NODEJS = 'nodejs'


@as_subset_of(Dependencies)
class PythonDependencies(SetEnum):
    DJANGO = 'django'
    FLASK = 'flask'
    FASTAPI = 'fastapi'


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
