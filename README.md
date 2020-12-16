### So I've heard you wanted to merge multiple Enums

This project allows you  to represent simple set-like
relations between different enums. Currently in development.

For now, here is the simple demo:
```python
from setenum import SetEnum, as_superset_of


class PythonDependencies(SetEnum):
    DJANGO = 'django'
    FLASK = 'flask'

@as_superset_of(PythonDependencies)
class Dependencies(SetEnum):
    NGINX = 'nginx'
    NODEJS = 'nodejs'


# Superset contains all values
assert [obj.value for obj in PythonDependencies] == ['django', 'flask']
assert [obj.value for obj in Dependencies] == ['nginx', 'nodejs', 'django', 'flask']

# bool operators works just like set should work
assert PythonDependencies.DJANGO in Dependencies 
assert Dependencies.FLASK in PythonDependencies

# in fact, objects that repeat are the same ones in different sets
assert PythonDependencies.DJANGO is Dependencies.DJANGO
```


Currently under investigation:
[ ] implicit intersections (define type in X, then in Y)
  (alternative - force defining intersection as explicit SetEnum)
[ ] `__subsets__` and `__supersets__` looks like a better choice than decorators
[ ] ensure Django tests are working fine
[ ] is there a way to get rid of SetEnum and leave only metaclass?
  (right now SetEnum is needed for `_missing_` only)
  Probably appending `dict` argument of `__new__` may work