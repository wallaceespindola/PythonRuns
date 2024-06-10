import argparse
import re


# Example: getValue -> get_value
def camel_2_snake_case(s):
    if s.isdigit() or not s.strip():
        return s  # Nothing to be done

    regex = (
        "(?<=[a-z])(?=[0-9A-Z])|"  # Handles transitions like a1 or aA
        "(?<=[0-9])(?=[a-zA-Z])"  # Handles transitions like 0a or 1B
        # "|(?<=[A-Z0-9]{3,})(?=[a-z])" # Handles transitions for Acronyms like SGCUfinished --> re.error: look-behind requires fixed-width pattern
    )
    replacement = "_"
    s = re.sub(regex, replacement, s).lower()
    return s


# Parsing command line arguments
parser = argparse.ArgumentParser(description="Coverts an input value from camel case to snake case.")
parser.add_argument("value", type=str, help="Value to be converted from camel case to snake case.")

args = parser.parse_args()

# Call the split_file function
value = camel_2_snake_case(args.value)
print(value)
