num1 = int(input("Enter the first number: "))
num2 = int(input("Enter the second number: "))

while num1 % num2 != 0:
    print(f"{num1} is not divisible by {num2}. Please try again.")
    num1 = int(input("Enter the first number: "))
    num2 = int(input("Enter the second number: "))

print(f"{num1} is divisible by {num2}!")
