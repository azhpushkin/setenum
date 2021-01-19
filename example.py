from setenum import SetEnum


# Example file, that showcases some basic functionality
# Also used to validate mypy plugin

class JavascriptDependencies(SetEnum):
    REACT = 'react'


# This creates Dependencies.REACT value
# Here subset is defined before bigger superset
class Dependencies(SetEnum):
    __subsets__ = (JavascriptDependencies, )
    NGINX = 'nginx'


# This creates Dependencies.FLASK and Dependencies.DJANGO
# Here subset is defined after superset
class PythonDependencies(SetEnum):
    __supersets__ = (Dependencies, )
    DJANGO = 'django'
    FLASK = 'flask'


# Simple comparision validations
assert Dependencies.REACT is JavascriptDependencies.REACT
assert Dependencies.FLASK is PythonDependencies.FLASK

assert Dependencies.REACT == JavascriptDependencies.REACT
assert Dependencies.FLASK == PythonDependencies.FLASK

# __in__ checks
assert Dependencies.FLASK in PythonDependencies
assert Dependencies.FLASK not in JavascriptDependencies
assert Dependencies.REACT in JavascriptDependencies
assert Dependencies.REACT not in PythonDependencies

assert JavascriptDependencies.REACT in Dependencies
assert PythonDependencies.FLASK in Dependencies

### MYPY CHECKS, THAT SHOULD PASS ###
py_dep: Dependencies = PythonDependencies.FLASK
js_dep: Dependencies
js_dep = JavascriptDependencies.REACT

# Just an other way to test the same
py_dep_temp = PythonDependencies.FLASK
dep_temp: Dependencies  = py_dep_temp


def foo(dep: Dependencies):
    pass


foo(Dependencies.NGINX)
foo(PythonDependencies.DJANGO)
foo(JavascriptDependencies.REACT)


### MYPY CHECKS THAT HAVE TO FAIL

bad_dep: PythonDependencies
bad_dep = Dependencies.DJANGO  # just pass original ones, if needed

def foo_2(dep: PythonDependencies):
    pass

foo_2(JavascriptDependencies.REACT)
foo_2(Dependencies.NGINX)