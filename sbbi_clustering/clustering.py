import argparse
import glob
import os
import numpy
from numpy import genfromtxt
from sklearn.cluster import DBSCAN
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

def recipes_DBSCAN(nutrition_data):
    db = DBSCAN(eps=20, min_samples=3)
    db.fit(nutrition_data)
    y_pred = db.fit_predict(nutrition_data)
    plt.figure(figsize=(10, 10))
    plt.scatter(nutrition_data[:, 0], nutrition_data[:, 1], c=y_pred, cmap='Paired')
    plt.title("Clusters determined by DBSCAN")
    plt.show()

def recipes_KMean(nutrition_data):
    print(1)

def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument("-c", "--country", help="country information", default='American')
    # country = parser.parse_args().country
    country = 'American'
    os.chdir(country)
    csv_file = glob.glob(country + '_recipes_nutrition.csv')[0]

    nutrition_data = genfromtxt(csv_file, delimiter=',', skip_header=True)
    nutrition_data = numpy.delete(nutrition_data, 0, 1)
    recipes_DBSCAN(nutrition_data)




if __name__ == '__main__':
    main()
