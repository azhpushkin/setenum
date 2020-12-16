import pytest
from setenum import SetEnum, as_superset_of
from datetime import date, datetime

# test enums


@pytest.mark.parametrize(
    'datatype, values',
    [
        (int, [1, 2, 3, 4]),
        (datetime, [datetime(day=day, month=1, year=2020) for day in range(1, 5)]),
        (date, [date(day=day, month=1, year=2020) for day in range(1, 5)]),
        (tuple, [(1, 2), (2, 3), (4, 5), (6, 7)]),
    ]
)
def test_bool_operators_with_custom_datatype(datatype, values):
    a, b, c, d = values

    class Subset(SetEnum):
        BASE_A = a
        BASE_B = b

    @as_superset_of(Subset)
    class Superset(SetEnum):
        SUPER_C = c
        SUPER_D = d

    assert Subset.BASE_A in Superset
    assert Subset.BASE_A == Superset.BASE_A
    assert Subset.BASE_A is Superset.BASE_A

    assert Superset.BASE_B in Subset
    assert Superset.SUPER_C not in Subset
