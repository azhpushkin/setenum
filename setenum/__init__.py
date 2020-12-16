from enum import Enum, EnumMeta



class SetEnumMeta(EnumMeta):

    def __init__(self, name, bases, dict):
        self._subsets_ = []
        self._supersets_ = []

    def __repr__(cls):
        return "<SetEnum %r>" % cls.__name__

    def __instancecheck__(self, instance):
        for cls in getattr(instance, '_owner_sets_', []):
            if cls == self:
                return True
        
        for cls in self._subsets_:
            if isinstance(instance, cls):
                return True
        
        return False


class SetEnum(Enum, metaclass=SetEnumMeta):
    # TODO: https://docs.python.org/3/reference/datamodel.html#customizing-instance-and-subclass-checks
    
    def __init__(self, *args, **kwargs):
        # Could be single value, but in case on intersections
        # value can be owner by multiple SetEnums
        self._owner_sets_ = [self.__class__, ]

    @classmethod
    def _missing_(cls, value):
        # _missing_ is used for looking up the values during __call__
        # this is a small check that makes this lookup work across super/sub sets
        if isinstance(value, cls):
            return value

        return super()._missing_(value)

    def __str__(self):
        if len(self._owner_sets_) == 1:
            owners = self.__class__.__name__
        else:
            owners = '(' + '|'.join(cls.__name__ for cls in self._owner_sets_) + ')'
        return "%s.%s" % (owners, self._name_)

    
def _copy_members_from_subset_to_superset(subset_cls, superset_cls):
    subset_cls._supersets_.append(superset_cls)
    superset_cls._subsets_.append(subset_cls)

    for name, obj in subset_cls._member_map_.items():
        setattr(superset_cls, name, obj)
        superset_cls._member_map_[name] = obj
        superset_cls._member_names_.append(name)
        superset_cls._value2member_map_[obj.value] = obj


def as_superset_of(subset_cls):
    def inner(superset_cls):
        _copy_members_from_subset_to_superset(subset_cls, superset_cls)
        return superset_cls
    return inner


def as_subset_of(superset_cls):
    def inner(subset_cls):
        _copy_members_from_subset_to_superset(subset_cls, superset_cls)
        return subset_cls
    return inner