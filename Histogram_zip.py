'''
ICSI 531 - Data Mining
Amith Kumar Singh
'''
import csv
import seaborn as sns
from dateutil import parser
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main():
    print "Histogram - NYPD Collision data"
    sum1 = 0
    borough = ["BRONX", "QUEENS", "MANHATTAN", "BROOKLYN", "STATEN ISLAND"]
    for region in borough:
        filename = region
        file1 = open("data/" + filename + ".txt", "a")
        c, zip, x, y = 0, {}, [], []
        with open ("data/NYPD_Motor_Vehicle_Collisions.csv") as f:
            reader = csv.reader(f)
            firstline = True
            for row in reader:
                if row[2] == region:
                    c = c + 1
                    if firstline:  # skip first line
                        firstline = False
                        continue
                    if row[3] not in zip:
                        zip[row[3]] = 1
                    zip[row[3]] += 1
            print zip
            for k, v in zip.iteritems():
                x.append(k)
                y.append(v)
            filename = region
            # plt.bar(zip.keys(), zip.values(), width = 1.0, color='g', edgecolor='orange') #for hist
            plt.xticks(x, rotation = 'vertical')
            plt.xlabel ('Zip codes')
            plt.ylabel ('# of accidents')
            plt.title ("Histogram - ZipCode Accident in " + filename)
            plt.show()
            # plt.savefig('data/cluster/'+ filename + '.png')


def BoxPlot():
    missing_values = ["n/a", "na", "-", ".", "NaN"]
    df = pd.read_csv ('./data/NYPD_Motor_Vehicle_Collisions.csv', na_values = missing_values)
    # df = pd.read_csv ('data/dummy.csv', na_values = missing_values)  # just for Bronx - elbow test

    # print df.head(10)
    df['HOUR'] = pd.to_datetime(df['TIME'], format='%H:%M').dt.hour
    print df.head(10)

    df1 = df[['BOROUGH', 'ZIP CODE','NUMBER OF PERSONS INJURED', 'NUMBER OF PERSONS KILLED', 'NUMBER OF PEDESTRIANS INJURED', 'NUMBER OF PEDESTRIANS KILLED',
              'NUMBER OF CYCLIST INJURED', 'NUMBER OF CYCLIST KILLED','NUMBER OF MOTORIST INJURED', 'NUMBER OF MOTORIST KILLED', 'HOUR']]
    df2 = df1.dropna(how = 'any')
    print df2.head(10)
    df2['ZIP CODE'] = pd.to_numeric (df['ZIP CODE'], errors = 'coerce')
    print df2.dtypes
    df2['TOTAL ACCIDENTS'] = df2.iloc[:, -8:-2].sum (axis = 1)
    print df2.head(10)

    fig, axes = plt.subplots (nrows = 1, ncols = 1)
    colors1 = ['red', 'green', 'blue', 'orange', 'cyan']
    sns.boxplot(x = df2["BOROUGH"], y = df2["HOUR"], palette = colors1)
    plt.show()
    # fig.savefig("box.png")
    plt.close()


if __name__ == '__main__':
    # main()
    BoxPlot()