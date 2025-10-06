from __future__ import annotations


def with_future_annotations(x: int) -> str:
    return str(x)


print(with_future_annotations.__annotations__)
# {'x': 'int', 'return': 'str'}
# Notice that the types are now real int and real string, not class objects.

if __name__ == "__main__":
    print(with_future_annotations(42))
    # 42 ==> {'x': 'int', 'return': 'str'}
