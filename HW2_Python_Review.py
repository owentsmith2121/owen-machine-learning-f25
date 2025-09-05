### Assignment 00 ###
from math import sqrt

# Task 01

foo = 3
bar = 3.14
myname = "Owen"

print(f"The value of foo is {foo} and its type is {type(foo)}")
print(f"The value of bar is {bar} and its type is {type(bar)}")
print(f"The value of myname is {myname} and its type is {type(myname)}")

# Task 02

# Part a
if foo < bar:
    print(f"foo {foo} is smaller than bar {bar}")
else:
    print(f"foo {foo} is NOT smaller than bar {bar}")

# Part b
for i in range(1,11):
    print(f"Number: {i} - Squared value: {i**2}")

# Part c
for i in range(1,11):
    if i == 7:
        continue
    print(f"Number: {i} - Squared value: {i**2}")


# Task 03

def isPrime(num: int) -> bool:
    for i in range(2, int(sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

test = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

for n in test:
    print(f"Is the number {n} prime?: {isPrime(n)}")

# Task 04

class Vertex:
    def __init__(self, x_coordinate, y_coordinate):
        self.x = x_coordinate
        self.y = y_coordinate

def Distance(v1: Vertex, v2: Vertex):
    return sqrt((v2.x - v1.x) ** 2 + (v2.y - v1.y) ** 2)

class Triangle:

    def __init__(self, v1: Vertex, v2: Vertex, v3: Vertex):

        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    def area(self) -> float:

        a = Distance(self.v1, self.v2)
        b = Distance(self.v2, self.v3)
        c = Distance(self.v3, self.v1)
        s = (a + b + c) / 2
        return sqrt(s * (s - a) * (s - b) * (s - c))

# Test for Task 04
v1 = Vertex(11, 2)
v2 = Vertex(3, 8)
v3 = Vertex(17, 3)

triangle = Triangle(v1, v2, v3)
print(f"Area of the triangle is: {triangle.area()}")