"""
Amith Kumar Singh
"""
import pandas as pd
from pandas._libs import json
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from matplotlib import pyplot as plt


def data():
    zip_dict={}
    print('Lets Start')
    # Making a list of missing value types
    missing_values = ["n/a", "na", "-",".", "NaN"]
    # df = pd.read_csv ('./data/NYPD_Motor_Vehicle_Collisions.csv', na_values=['.'])
    df = pd.read_csv('data/dummy.csv',na_values = missing_values)  # just for Bronx - elbow test

    # print df.head(10)

    df1 = df[['ZIP CODE', 'LATITUDE', 'LONGITUDE', 'NUMBER OF PERSONS INJURED', 'NUMBER OF PERSONS KILLED', 'NUMBER OF PEDESTRIANS INJURED', 'NUMBER OF PEDESTRIANS KILLED',
              'NUMBER OF CYCLIST INJURED', 'NUMBER OF CYCLIST KILLED','NUMBER OF MOTORIST INJURED', 'NUMBER OF MOTORIST KILLED']]
    df2 = df1.dropna(how = 'any')
    print df2.head(10)
    df2['ZIP CODE'] = pd.to_numeric(df['ZIP CODE'], errors='coerce')
    print df2.dtypes
    df3 = df2.drop(['ZIP CODE','LATITUDE', 'LONGITUDE'],axis=1)
    print df3.head(5)

    tweets = []
    for index, row in df2.iterrows():
        d = str(row[0])
        tweets.append(json.loads(d))
    print tweets
    # return(df3, tweets)

def find_clusters(d):
    df2, tweets = d
    s = StandardScaler()
    s.fit(df2)
    normalized = s.transform(df2)

    sum_of_squared_distances = []
    K = range(1, 15)
    for k in K:
        km1 = KMeans(n_clusters = k)  # try 100 different initial centroids
        km1.fit(normalized)
        sum_of_squared_distances.append(km1.inertia_)

    plt.plot(K, sum_of_squared_distances, 'gx-')
    plt.xlabel("K -  Value")
    plt.ylabel("Sum of Squared Error")
    plt.title("Determing k-value based on SSE")
    plt.show()
    plt.savefig("data/cluster/elbow_test.png")

def cluster(d):
    df2, tweets = d
    # K-means clustering
    km = KMeans(n_clusters = 8, n_init = 100) # try 100 different initial centroids
    km.fit(df2)

    cluster = []
    cluster_stat = dict()
    # Print zip codes that belong to cluster 2
    for idx, cls in enumerate(km.labels_):
        # print idx,cls
        if cluster_stat.has_key(cls):
            cluster_stat[cls] += 1
        else:
            cluster_stat[cls] = 1
        open('data/cluster/cluster-{0}.txt'.format(cls), 'a').write(json.dumps(tweets[idx]) + '\r\n')


if __name__=='__main__':
    d = data()
    # find_clusters(d)
    # cluster(d)
