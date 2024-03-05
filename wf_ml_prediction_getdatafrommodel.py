import os
import numpy as np


def get_data_from_model(model_name):
    os.chdir("data_processed")
    two_dimension_arr = np.loadtxt(model_name, dtype=[('f0', list),('f1',float)], delimiter="$", skiprows=0, usecols=(0, 1))
    x_emotional = []
    y_emotional = []
    for entry in two_dimension_arr:
        x = entry[0].replace('[', '').replace(']', '').split(',')
        x = [float(string) for string in x]
        x_emotional.append(x)
        y_emotional.append(float(entry[1]))

    os.chdir("..")
    return x_emotional, y_emotional
