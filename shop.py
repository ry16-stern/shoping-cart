from pandas import read_csv
import os

csv_filepath = "data/products.csv"
x = read_csv(csv_filepath)
print(x)