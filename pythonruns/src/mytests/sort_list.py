# Import the sys module
import sys

print("----------------------------------------")

# Define a list of numeric values
my_list = [5, 2, 9, 7, 4, 1]

# Print the original list
print("Original list:", my_list)

# Sort the list in ascending order
my_list.sort()
print("Sorted list (ascending):", my_list)

# Sort the list in descending order
my_list.sort(reverse=True)
print("Sorted list (descending):", my_list)

print("----------------------------------------")

# Define a list of numeric values
my_list2 = []

# Loop through the command line arguments starting from index 1
for i in range(1, len(sys.argv)):
    # Convert each argument to an integer and append it to the list
    my_list2.append(int(sys.argv[i]))

# Print the original list
print("Original list 2:", my_list2)

# Sort the list in ascending order
my_list2.sort()
print("Sorted list 2 (ascending):", my_list2)

# Sort the list in descending order
my_list2.sort(reverse=True)
print("Sorted list 2 (descending):", my_list2)

print("----------------------------------------")
