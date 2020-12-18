import pytest

from setenum import SetEnum

def test_simple_cycle():
    class A(SetEnum):
        pass

    with pytest.raises(RuntimeError):
        class B(SetEnum):
            __supersets__ = [A]
            __subsets__ = [A]
