def print_text_heart(text):
    print(f"\n####### {text} te amo !!! #######")
    print(
        "\n".join(
            [
                "".join([(f"{text}!"[(x - y) % 8] if calc(x, y) else " ") for x in range(-30, 30)])
                for y in range(15, -15, -1)
            ]
        )
    )


def calc(x, y):
    return ((x * 0.05) ** 2 + (y * 0.1) ** 2 - 1) ** 3 - (x * 0.05) ** 2 * (y * 0.1) ** 3 <= 0


if __name__ == "__main__":
    print_text_heart("Janaina")  # str must be 7 characters
