from typing import Protocol, Dict, Optional, Callable


# See: https://stackoverflow.com/questions/54668000/type-hint-for-an-instance-of-a-non-specific-dataclass
class NWSItem(Protocol):
    """A generic type that represents any dataclass in the nwsc data model"""
    __dataclass_fields__: Dict
    __dataclass_params__: Dict
    __post_init__: Optional[Callable]
