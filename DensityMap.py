"""
Amith Kumar Singh
"""
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


def data():
    zip_dict={}
    print('Lets Start')
    # Making a list of missing value types
    missing_values = ["n/a", "na", "-",".", "NaN"]
    # df = pd.read_csv ('./data/NYPD_Motor_Vehicle_Collisions.csv', na_values=['.'])
    df = pd.read_csv('data/NYPD_Motor_Vehicle_Collisions.csv',na_values = missing_values)

    # print df.head(10)

    df1 = df[['ZIP CODE', 'NUMBER OF PERSONS INJURED', 'NUMBER OF PERSONS KILLED', 'NUMBER OF PEDESTRIANS INJURED', 'NUMBER OF PEDESTRIANS KILLED',
              'NUMBER OF CYCLIST INJURED', 'NUMBER OF CYCLIST KILLED','NUMBER OF MOTORIST INJURED', 'NUMBER OF MOTORIST KILLED']]
    df2 = df1.dropna(how = 'any')
    print df2.head(10)
    df2['ZIP CODE'] = pd.to_numeric(df['ZIP CODE'], errors='coerce')

    fig, axes = plt.subplots (nrows = 1, ncols = 1)
    sns.kdeplot (df2['NUMBER OF PERSONS INJURED'], shade = True, color = "b")
    # sns.kdeplot (df2['NUMBER OF PERSONS KILLED'], shade = True, color = "r")
    sns.kdeplot (df2['NUMBER OF PEDESTRIANS INJURED'], shade = True, color = "g")
    sns.kdeplot (df2['NUMBER OF CYCLIST INJURED'], shade = True, color = "g")
    # sns.kdeplot (df2['NUMBER OF CYCLIST KILLED'], shade = True, color = "b")
    sns.kdeplot (df2['NUMBER OF MOTORIST INJURED'], shade = True, color = "y")
    # sns.kdeplot (df2['NUMBER OF MOTORIST KILLED'], shade = True, color = "y")
    plt.show()
    fig.savefig("density_injured.png")
    plt.close()


if __name__=='__main__':
    data()
