print("\n####### Happy Teacher's day !!! #######")


def calc(x, y):
    return ((x * 0.05) ** 2 + (y * 0.1) ** 2 - 1) ** 3 - (x * 0.05) ** 2 * (y * 0.1) ** 3 <= 0


def print_teacher():
    print(
        "\n".join(
            [
                "".join([("Teachers"[(x - y) % 8] if calc(x, y) else " ") for x in range(-30, 30)])
                for y in range(15, -15, -1)
            ]
        )
    )


if __name__ == "__main__":
    print_teacher()
