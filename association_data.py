'''
ICSI 531 - Data Mining
Amith Kumar Singh
'''
import csv
from time import strftime
from dateutil import parser
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main():
    print "Association Rule - NYPD Collision data"
    sum1 = 0
    borough = ["BRONX", "QUEENS", "MANHATTAN", "BROOKLYN", "STATEN ISLAND"]
    for region in borough:
        filename = region
        file1 = open("data/" + filename + ".txt", "a")
        c = 0
        with open ("data/NYPD_Motor_Vehicle_Collisions.csv") as f:
            reader = csv.reader (f)
            firstline = True
            for row in reader:
                if row[2] == region:
                    c = c + 1
                    if firstline:  # skip first line
                        firstline = False
                        continue
                    # if row[18] not in ["SPORT UTILITY / STATION WAGON", "Driver Inattention/Distraction", "Unspecified", "PASSENGER VEHICLE"]:
                        # data = '"' + row[2] + row[3] + ',' + row[18] + ',' + row[24] + '"'
                    data = row[18] + ',' + row[24]
                    file1.write(data + "\n")
        file1.close()
        print region, c


if __name__ == '__main__':
    main()