import pytest
from setenum import SetEnum, includes

# test enums

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


@pytest.mark.skip(reason='No idea how to implement this yet')
def test_is():
    assert PythonDependencies.DJANGO is Dependencies.DJANGO
