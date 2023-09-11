print("####### Testing python passing values from input in console #######")

# Take MCQ marks
mcq_marks = float(input("Enter the MCQ marks: "))
# Take theory marks
theory_marks = float(input("Enter the Theory marks: "))

# Check the passing condition using 'AND' and 'OR' operator
if (mcq_marks >= 40 and theory_marks >= 30) or (mcq_marks + theory_marks) >= 70:
    print("\nYou have passed")
else:
    print("\nYou have failed")

print("\nTo pass: (mcq_marks >= 40 and theory_marks >= 30) or (mcq_marks + theory_marks) >= 70")
