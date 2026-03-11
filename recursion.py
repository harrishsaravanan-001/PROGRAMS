# Python program using recursion to find factorial

def factorial(n):
    if n == 1 or n == 0:
        return 1
    else:
        return n * factorial(n-1)

num = int(input("Enter a number: "))

result = factorial(num)

print("Factorial is:", result)
