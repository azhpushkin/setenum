import pytest
from setenum import SetEnum

# Example SetEnums

# Different ways to create the same Enum structure

def create_via_subset():
    class PythonDependencies(SetEnum):
        DJANGO = 'django'
        FLASK = 'flask'

    class Dependencies(SetEnum):
        __subsets__ = [PythonDependencies, ]
        NGINX = 'nginx'
        NODEJS = 'nodejs'
    
    return PythonDependencies, Dependencies


def create_via_superset():
    class Dependencies(SetEnum):
        NGINX = 'nginx'
        NODEJS = 'nodejs'

    class PythonDependencies(SetEnum):
        __supersets__ = [Dependencies, ]
        DJANGO = 'django'
        FLASK = 'flask'

    return PythonDependencies, Dependencies

    
@pytest.fixture(params=['__subsets__', '__supersets__'])
def setenum_factory(request):
    return create_via_subset if request.param == '__subsets__' else create_via_superset


def test_values(setenum_factory):
    PythonDependencies, Dependencies = setenum_factory()

    assert len(PythonDependencies) == 2
    assert len(Dependencies) == 4
    assert set(obj.value for obj in PythonDependencies) == set(['django', 'flask'])
    assert set(obj.value for obj in Dependencies) == set(['django', 'flask', 'nginx', 'nodejs'])


def test_compare_to_superset(setenum_factory):
    PythonDependencies, Dependencies = setenum_factory()

    assert PythonDependencies.DJANGO in Dependencies
    assert PythonDependencies.DJANGO == Dependencies.DJANGO
    

def test_lookup_superset_in_subset(setenum_factory):
    PythonDependencies, Dependencies = setenum_factory()
    
    assert Dependencies.DJANGO in PythonDependencies
    assert Dependencies.NGINX not in PythonDependencies


def test_is_operator(setenum_factory):
    PythonDependencies, Dependencies = setenum_factory()

    assert PythonDependencies.DJANGO is Dependencies.DJANGO


def test_insinstance(setenum_factory):
    PythonDependencies, Dependencies = setenum_factory()

    assert isinstance(PythonDependencies.DJANGO, Dependencies)


def test_call(setenum_factory):
    PythonDependencies, Dependencies = setenum_factory()

    assert PythonDependencies('django') is PythonDependencies.DJANGO
    assert Dependencies('django') is PythonDependencies.DJANGO
    
    assert Dependencies(PythonDependencies.DJANGO) is PythonDependencies.DJANGO
    assert Dependencies(Dependencies.DJANGO) is PythonDependencies.DJANGO

    assert PythonDependencies(PythonDependencies.DJANGO) is PythonDependencies.DJANGO
    assert PythonDependencies(Dependencies.DJANGO) is PythonDependencies.DJANGO
    