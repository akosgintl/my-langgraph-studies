# TypedDict Optional
from typing import Optional, TypedDict

# Optional
# https://docs.python.org/3/library/typing.html#typing.Optional
# Optional[T] is equivalent to Union[T, None].

# Union
# https://docs.python.org/3/library/typing.html#typing.Union
# Union[T, U] is the union of T and U.

# Literal
# https://docs.python.org/3/library/typing.html#typing.Literal
# Literal[T] is a literal type that can only be one of the specified values.

# Annotated
# https://docs.python.org/3/library/typing.html#typing.Annotated
# Annotated[T, X] is a type that is annotated with X.

# Required
# https://docs.python.org/3/library/typing.html#typing.Required
# Required[T] is equivalent to T.

# NotRequired
# https://docs.python.org/3/library/typing.html#typing.NotRequired
# NotRequired[T] is equivalent to Optional[T].

# TypedDict
# https://docs.python.org/3/library/typing.html#typing.TypedDict
# TypedDict is a dictionary that maps strings to values of a specified type.
class AllOptionalTypedDictState(TypedDict):
    key01: str
    key02: Optional[str]
    key03: int   
    key04: Optional[int]
    key05: float
    key06: Optional[float]
    key07: bool
    key08: Optional[bool]
    key09: list[str]
    key10: Optional[list[str]]
    key11: dict[str,str]
    key12: Optional[dict[str,str]]

class ParentTypedDictState(TypedDict):
    key01: str
    key02: int

class ChildTypedDictState(ParentTypedDictState):
    key03: float
    key04: bool

class SimpleTypedDictState(TypedDict):
    key01: str
    key02: int

class ComplexTypedDictState(TypedDict):
    key03: SimpleTypedDictState
    key04: list[SimpleTypedDictState]
    key05: dict[str,str] # dictionary of strings
    key06: dict[str,SimpleTypedDictState] # dictionary of SimpleTypedDictState
    key07: dict[str,list[str]] # dictionary of lists of strings
    key08: dict[str,list[SimpleTypedDictState]] # dictionary of lists of SimpleTypedDictState
    key09: dict[str,dict[str,str]] # dictionary of dictionaries of strings
    key10: dict[str,dict[str,SimpleTypedDictState]] # dictionary of dictionaries of SimpleTypedDictState
    key11: dict[str,list[dict[str,str]]] # dictionary of lists of dictionaries of strings
    key12: dict[str,list[dict[str,SimpleTypedDictState]]] # dictionary of lists of dictionaries of SimpleTypedDictState

# Simple example
out1_0 = AllOptionalTypedDictState(key01="value01", 
                                   key02="value02", 
                                   key03=1, 
                                   key04=2, 
                                   key05=3.0, 
                                   key06=4.0, 
                                   key07=True, 
                                   key08=False, 
                                   key09=["value09"], 
                                   key10=["value10"], 
                                   key11={"key11_0": "value11_0", "key11_1": "value11_1"})

# Simple example
out1_1 = AllOptionalTypedDictState(key01="value01", 
                                   key02=None,
                                   key03=1, 
                                   key04=None,
                                   key05=3.0, 
                                   key06=None,
                                   key07=True, 
                                   key08=None,
                                   key09=["value09"], 
                                   key10=None,
                                   key11={"key11_0": "value11_0", "key11_1": "value11_1"}, 
                                   key12=None)

# Complex example
out2 = ComplexTypedDictState(key03=SimpleTypedDictState(key01="value03_01", key02=3), 
                             key04=[SimpleTypedDictState(key01="value04_01", key02=4), SimpleTypedDictState(key01="value04_02", key02=5)], 
                             key05={"key05_0": "value05_0", "key05_1": "value05_1"}, 
                             key06={"key06_0": SimpleTypedDictState(key01="value06_01", key02=6), "key06_1": SimpleTypedDictState(key01="value06_11", key02=7)}, 
                             key07={"key07_0": ["value07_01", "value07_02"], "key07_1": ["value07_11", "value07_12"]}, 
                             key08={"key08_0": [SimpleTypedDictState(key01="value08_01", key02=8), SimpleTypedDictState(key01="value08_02", key02=9)], "key08_1": [SimpleTypedDictState(key01="value08_11", key02=10), SimpleTypedDictState(key01="value08_12", key02=11)]}, 
                             key09={"key09_0": {"key09_01": "value09_01", "key09_02": "value09_02"}, "key09_1": {"key09_11": "value09_11", "key09_12": "value09_12"}}, 
                             key10={"key10_0": {"key10_01": SimpleTypedDictState(key01="value10_01", key02=12), "key10_02": SimpleTypedDictState(key01="value10_02", key02=13)}, "key10_1": {"key10_11": SimpleTypedDictState(key01="value10_11", key02=14), "key10_12": SimpleTypedDictState(key01="value10_12", key02=15)}}, 
                             key11={"key11_0": [{"key11_01": "value11_01", "key11_02": "value11_02"}, {"key11_03": "value11_03", "key11_04": "value11_04"}], "key11_1": [{"key11_11": "value11_11", "key11_12": "value11_12"}, {"key11_13": "value11_13", "key11_14": "value11_14"}]}, 
                             key12={"key12_0": [{"key12_01": SimpleTypedDictState(key01="value12_01", key02=16), "key12_02": SimpleTypedDictState(key01="value12_02", key02=17)}, {"key12_03": SimpleTypedDictState(key01="value12_03", key02=18), "key12_04": SimpleTypedDictState(key01="value12_04", key02=19)}], "key12_1": [{"key12_11": SimpleTypedDictState(key01="value12_11", key02=20), "key12_12": SimpleTypedDictState(key01="value12_12", key02=21)}, {"key12_13": SimpleTypedDictState(key01="value12_13", key02=22), "key12_14": SimpleTypedDictState(key01="value12_14", key02=23)}]})

# Parent example
out3 = ParentTypedDictState(key01="parent01", key02=1)

# Child example
out4 = ChildTypedDictState(key01="child01", key02=1, key03=2.0, key04=True)

print("---json.dumps(indent=2)---")
import json
print("---AllOptionalTypedDictState all keys present---") # All keys are optional
print(json.dumps(out1_0, indent=2))
print("---AllOptionalTypedDictState some keys missing---") # All keys are optional
print(json.dumps(out1_1, indent=2))
print("---ComplexTypedDictState---") # Complex nested structure
print(json.dumps(out2, indent=2))
print("---ParentTypedDictState---") # Parent class
print(json.dumps(out3, indent=2))
print("---ChildTypedDictState---") # Child class
print(json.dumps(out4, indent=2))
