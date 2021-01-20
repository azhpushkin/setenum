from setenum import SetEnum


class X(SetEnum):
    C: int = 3
    A = 'a'
    B = 1


a: int = X.C.value

