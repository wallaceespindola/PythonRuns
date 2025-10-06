print("####### Testing python boolean from numbers #######")

# Boolean value
val1 = True
print(f"A true value: {val1}")
val1 = False
print(f"A false value: {val1}")


# Number to Boolean
number = 10
print(f"A number {number} gives: {bool(number)}")

number = -5
print(f"A number {number} gives: {bool(number)}")

number = 0
print(f"A number {number} gives: {bool(number)}")

number = 1000
print(f"A number {number} gives: {bool(number)}")

number = -1
print(f"A number {number} gives: {bool(number)}")

value = "A"
print(f"A value {value} gives: {bool(value)}")

value = "F"
print(f"A value {value} gives: {bool(value)}")

value = "T"
print(f"A value {value} gives: {bool(value)}")

value = "false"
print(f"A value {value} gives: {bool(value)}")

value = "true"
print(f"A value {value} gives: {bool(value)}")

# Boolean from comparison operator
val1 = 6
val2 = 3
print(f"A comparison on {val1} < {val2} gives: {val1 < val2}")
print(f"A comparison on {val1} > {val2} gives: {val1 > val2}")

# Boolean from comparison operator
val1 = "A"
val2 = "B"
print(f"A comparison on {val1} > {val2} gives: {val1 > val2}")
print(f"A comparison on {val1} < {val2} gives: {val1 < val2}")
