def float_numbers():
    print("####### Testing python float number formatting #######")

    # Use of String Formatting
    float1 = 563.78453
    print(f"Original: {float1}")
    print("Formatted 2 decimals: {:3.1f}".format(float1))
    print("Formatted 2 decimals: {:5.2f}".format(float1))

    print("---------------------------")

    # Use of String Interpolation
    float2 = 12.3456
    print(f"Original: {float2}")
    print("Formatted 2 decimals: %5.2f" % float2)


if __name__ == "__main__":
    float_numbers()
