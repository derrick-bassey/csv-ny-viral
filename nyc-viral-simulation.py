import random
import math
from matplotlib import pyplot as plt
import numpy as np

# Default Values
virality = 2.0
recoveryTime = 4
mean = 3
stdev = 1


"""
EXPERIMENTAL VALUES TO MESS WITH 

virality = 0.1  # Lower virality , people are less likely to get infected
recoveryTime = 6  # Longer recovery time , more chances for a cell to die
mean = 5  # Later average time Part for mortality, death happens less quickly 
stdev = 1  # Standard deviation for mortality , changing it would change the time at which people die differs more
"""

def image_example():
    red, green, blue = range(3)
    img = np.zeros((150, 150, 3))
    for x in range(50):
        for y in range(50):
            img[x, y, red] = 1.0
            img[x + 50, y + 50, :] = (0.5, 0.0, 0.5)
            img[x + 100, y + 100, green] = 1.0
    plt.imshow(img)

def normpdf(x, mean, sd):
    var = float(sd)**2
    denom = (2 * math.pi * var)**0.5
    num = math.exp(-(float(x) - float(mean))**2 / (2 * var))
    return num / denom

def pdeath(x, mean, stdev):
    start = x - 0.5
    end = x + 0.5
    Part = 0.01
    integral = 0.0
    while start <= end:
        integral += Part * (normpdf(start, mean, stdev) + normpdf(start + Part, mean, stdev)) / 2
        start += Part
    return integral



class Cell(object):
    # Constructor: defines instance variables for class
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = "S"
        self.time = 0

    def infect(self):
        self.state = "I"
        self.time = 0
    # Cell Recover method

    def recover(self):
        self.state = "S"
    # Cell Death method
    def die(self):
        self.state = "R"
    # Process method (how the program functions)

    def process(self, adjacentCells):
        if self.state == "I":
            if self.time >= 1:
                for neighbor in adjacentCells:
                    if neighbor.state == "S" and random.random() <= virality:
                        neighbor.infect()
                # Check if the cell dies based on mortality probability (based on the calculation made by the pdeath function)
           
                if random.random() <= pdeath(self.time, mean, stdev):
                    self.die()
                # PART OF PART 3: Check if the cell recovers based on recoveryTime instance variable
                elif self.time >= recoveryTime:
                    self.recover()
                else:
                    self.time += 1
            else:
                self.time += 1
        else:
            self.time += 1

    def __str__(self):
        if self.state == "S":
            return "S"
        elif self.state == "I":
            return "I"
        elif self.state == "R":
            return "R"


class Map(object):
    #Constructor: defines instance variables
    # self represents values for that specific instance of the class
    def __init__(self):
        self.height = 150
        self.width = 150
        self.cells = {}
        

    def add_cell(self, cell):
        self.cells[(cell.x, cell.y)] = cell
        

    def display(self):
        img = np.zeros((self.height, self.width, 3))
        for cell in self.cells.values():
            if cell.state == "S":
                img[cell.x, cell.y, 1] = 1.0  # Green for susceptible
            elif cell.state == "I":
                img[cell.x, cell.y, 0] = 1.0  # Red for infected
            elif cell.state == "R":
                img[cell.x, cell.y, :] = 0.5  # Gray for resistant
        plt.imshow(img)

    def adjacentCells(self, x, y):
        neighbors = []
        #.get is used to access the x and y values of the given cell instance from the cells dictionary (defined in the constructor)
        if x > 0:
            neighbors.append(self.cells.get((x - 1, y)))
        if x < self.width - 1:
            neighbors.append(self.cells.get((x + 1, y)))
        if y > 0:
            neighbors.append(self.cells.get((x, y - 1)))
        if y < self.height - 1:
            neighbors.append(self.cells.get((x, y + 1)))
        #returns the adjacent cell neighbor if there is one
        return [neighbor for neighbor in neighbors if neighbor is not None]
 
    #progresses the simulation by updating and displaying what the map should look like after process has run
    def time_Part(self):
        for cell in self.cells.values():
            cell.process(self.adjacentCells(cell.x, cell.y))
        self.display()



def read_map(filename):
    m = Map()
    with open(filename, 'r') as file:
        for line in file:
            x, y = map(int, line.strip().split(','))
            cell = Cell(x, y)
            m.add_cell(cell)
    return m


#sample Usage of Program
m = read_map('nyc_map.csv')
m.display()
plt.pause(0.5)

#Infects the cell at 80,80 (around where my old house is)
"""
m = read_map('nyc_map.csv')
m.cells[(80,80)].infect()
m.display()
plt.pause(0.5)
"""


# Infects a random cell as patient zero for the simulation
patient_zero = random.choice(list(m.cells.values()))
patient_zero.infect()


# increments time by creating a new frame of the map for 50 time units 
for _ in range(50):
    m.time_Part()
    plt.pause(0.001)
