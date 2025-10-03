"""
Hello World module - Basic example for PythonRuns project.
"""


def say_hello(name: str = "World") -> str:
    """
    Return a greeting message.

    :param name: Name to greet
    :return: Greeting message
    """
    return f"Hello, {name}!"


def main():
    """Main function to run the hello world example."""
    print(say_hello())
    print(say_hello("Python"))
    print(say_hello("PythonRuns"))


if __name__ == "__main__":
    main()

