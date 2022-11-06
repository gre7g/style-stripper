"""Just making sure we'll be able to import an old pickle when/if we upgrade the classes underneath"""
from dataclasses import dataclass
import pickle


@dataclass
class MyClass:
    a: int = 1
    b: int = 2
    c: int = 3
    # x: str = "a new value"


if __name__ == "__main__":
    # obj = MyClass(b=10)
    # print(obj)
    # print(pickle.dumps(obj))

    pickled = (
        b"\x80\x04\x952\x00\x00\x00\x00\x00\x00\x00\x8c\x08__main__\x94\x8c\x07MyClass\x94\x93\x94)\x81\x94}\x94(\x8c"
        b"\x01a\x94K\x01\x8c\x01b\x94K\n\x8c\x01c\x94K\x03ub."
    )
    obj = pickle.loads(pickled)
    print(obj)
