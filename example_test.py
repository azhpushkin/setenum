from enum import Enum


class Manufacturer(Enum):
    APPLE = 'apple'
    DELL = 'dell'
    ...


class AppleModels(Enum):
    MACBOOK_AIR = 'macbook_air'
    MACBOOK_PRO = 'macbook_pro'


class DellModels(Enum):
    XPS = 'xps'
    LATITUDE = 'latitude'


Models = 

@dataclass
class Laptop:
    manufacturer
