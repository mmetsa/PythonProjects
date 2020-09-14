"""Geometry program that calculates the area of a square, circle or a triangle."""
import math
# Ask which shape to calculate the area for
shape = input("Please insert geometric shape:")
if shape == "circle":  # if the shape is circle ask for radius
    radius = float(input("Please insert radius in cm:"))
    print("The area is " + str(round(radius ** 2 * math.pi, 2)) + " cm^2")
elif shape == "square" or shape == "triangle":  # if the shape is either square or triangle ask for side length
    side_length_in_cm = float(input("Please insert side length in cm:"))
    if shape == "square":  # if the shape is square, calculate the area for a square
        print("The area is " + str(round(side_length_in_cm ** 2, 2)) + " cm^2")
    else:  # if it is not square, it must be a triangle, so calculate the area for a triangle
        print("The area is " + str(round(side_length_in_cm ** 2 * math.sqrt(3) / 4, 2)) + " cm^2")
else:  # if it was not a supported shape
    print("Shape is not supported.")
