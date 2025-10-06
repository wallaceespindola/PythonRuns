def switch_case():
    lang = input("What's the programming language you want to learn? ")

    if lang is None:
        print(">> Please enter a language.")

    match lang.lower():
        case "javascript":
            print(">> You can become a web developer.")

        case "python":
            print(">> You can become a Data Scientist")

        case "php":
            print(">> You can become a backend developer")

        case "solidity":
            print(">> You can become a Blockchain developer")

        case "java":
            print(">> You can become a mobile app developer")

        case _:
            print(">> The language doesn't matter, what matters is solving problems.")


if __name__ == "__main__":
    switch_case()
