#!/usr/bin/python

#Import libraries
import math

#Define a class for 2d Vectors
class Vector2f:
    #Define the constructor
    def __init__(self, x, y):
        self.x = x
        self.y = y

    #Define the + operator
    def __add__(self, other):
        return Vector2f(self.x + other.x, self.y + other.y)

    #Define the += operator
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    #Define the - operator
    def __sub__(self, other):
        return Vector2f(self.x - other.x, self.y - other.y)

    #Define the -= operator
    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    #Define the * operator
    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return Vector2f(self.x * other.x, self.y * other.y)
        elif isinstance(other, float):
            return Vector2f(self.x * other, self.y * other)

    #Define the *= operator
    def __imul__(self, other):
        if isinstance(other, self.__class__):
            self.x *= other.x
            self.y *= other.y
        elif isinstance(other, float):
            self.x *= other
            self.y *= other

        return self

    #Define the / operator
    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            return Vector2f(self.x / other.x, self.y / other.y)
        elif isinstance(other, float):
            return Vector2f(self.x / other, self.y / other)

    #Define the /= operator
    def __idiv__(self, other):
        if isinstance(other, self.__class__):
            self.x /= other.x
            self.y /= other.y
        elif isinstance(other, float):
            self.x /= other
            self.y /= other

        return self

    #Define the == operator
    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True

        return False

    #Define the != operator
    def __ne__(self, other):
        if self.x != other.x or self.y != other.y:
            return True

        return False

    #Get the Vector length
    def getLength(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    #Get the Vector length squared
    def getLengthSQ(self):
        return self.x * self.x + self.y * self.y

    #Get the Vector length between this vector and the other
    def getLengthTo(self, other):
        deltaX = other.x - self.x
        deltaY = other.y - self.y
        return math.sqrt(deltaX * deltaX + deltaY * deltaY)

    #Get the Vector length between this vector and the other squared
    def getLengthToSQ(self, other):
        deltaX = other.x - self.x
        deltaY = other.y - self.y
        return deltaX * deltaX + deltaY * deltaY

    #Remove length from the Vector
    def removeMagnitude(self, lengthToRemove):
        #Get the current length
        length = self.getLength()

        #If the Vector has length to remove, do so
        if length > lengthToRemove:
            self.setLength(length - lengthToRemove)
        #Otherwise set the Vector length to 0
        else:
            self.x = 0
            self.y = 0

    #Set the Vector length
    def setLength(self, length):
        #Check the Vector2f has length, otherwise its not scalable
        if self.x != 0 or self.y != 0:
            #Get the factor to scale the Vector2f to length
            factor = length / self.getLength()

            #Scale the Vector to length
            self.x *= factor
            self.y *= factor

    #Conver the Vector to a String
    def toString(self):
        return str(self.x) + ", " + str(self.y)



