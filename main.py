# -*-coding:utf-8-*-

import argparse
from io import StringIO

import joblib
import numpy as np
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
np.set_printoptions(threshold=np.inf)


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="Input file.")
    parser.add_argument("-o", help="Output file.")
    args = parser.parse_args()
    return args.i, args.o


def preprocess(filepath):
    string_1 = string_2 = ""
    file = open(filepath, "r")
    line = file.readline()
    while line:
        if line.startswith(">"):
            string_1 += line
        else:
            string_1 += line.strip()
        line = file.readline()
        if line.startswith(">"):
            string_1 += "\n"
        else:
            continue
    file.close()
    list_1 = string_1.split("\n")
    for i in range(0, len(list_1), 2):
        for j in range(20, len(list_1[i + 1].strip()) - 20):
            if list_1[i + 1].strip()[j].upper() == "A":
                string_2 += list_1[i].strip() + "_" + str(j + 1) + "\n" + list_1[i + 1].strip()[j - 20:j + 21] + "\n"
    list_2 = string_2.split("\n")
    return list_2[0:-1]


def feature_extract(fasta):
    features = ""
    for i in range(1000):
        features += "ohe2_f" + str(i + 1) + ","
    features += "class\n"
    dinucleotides = ["aa", "ac", "ag", "at", "an",
                     "ca", "cc", "cg", "ct", "cn",
                     "ga", "gc", "gg", "gt", "gn",
                     "ta", "tc", "tg", "tt", "tn",
                     "na", "nc", "ng", "nt", "nn"]
    for i in range(0, len(fasta), 2):
        for j in range(len(fasta[i + 1].strip()) - 1):
            for k in range(len(dinucleotides)):
                if fasta[i + 1][j:j + 2].lower() == dinucleotides[k]:
                    features += "1, "
                else:
                    features += "0, "
        features += "?" + "\n"
    return pd.read_csv(StringIO(features), sep=",")


def classify(dataframe):
    clf = joblib.load("model.pkl")
    x, y = dataframe.values[:, :-1], dataframe.values[:, -1]
    y_hat = clf.predict(x)
    return y_hat


def find_last(string, char):
    last_position = -1
    while True:
        position = string.find(char, last_position + 1)
        if position == -1:
            return last_position
        last_position = position


if __name__ == "__main__":
    input_file, output_file = argument_parser()
    dl = preprocess(input_file)
    df = feature_extract(dl)
    pred_y = classify(df)
    result = "No.,Sequence_name,Position,Sequence,Prediction\n"
    for i in range(len(pred_y)):
        sequence = dl[2 * i + 1]
        fl = find_last(dl[2 * i], "_")
        sequence_name = dl[2 * i][0:fl]
        position = dl[2 * i][fl+1:]
        prediction = "non-6mA"
        if pred_y[i] == 1:
            prediction = "6mA"
        result += str(i+1) + "," + sequence_name + "," + position + "," + sequence + "," + prediction + "," + "\n"
    with open(output_file, "w") as file:
        file.write(result)
