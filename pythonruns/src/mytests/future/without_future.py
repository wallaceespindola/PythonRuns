def without_future_annotations(x: int) -> str:
    return str(x)


print(without_future_annotations.__annotations__)
# {'x': <class 'int'>, 'return': <class 'str'>}
# Notice that the types are now class of int and class of strings, not real str and int objects.

if __name__ == "__main__":
    print(without_future_annotations(42))
    # 42 ==> {'x': <class 'int'>, 'return': <class 'str'>}
