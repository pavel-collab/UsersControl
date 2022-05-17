#!/usr/bin/python3

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import os
from sys import argv


def main():
    file = open("./Hists/Hist" + argv[1] + ".dat", "r")
    lines = file.readlines()

    win_list = []
    percent_list = []

    try:
        for i in range(3):
            new_line = (lines[2*i][:16] + '...' + lines[2*i][-16:]) if len(lines[2*i]) > 35 else lines[2*i]

            win_list.append(new_line)
            percent_list.append(float(lines[2*i + 1]))
    except:
        pass


    data = {"Windows":    win_list,
            "Percentage": percent_list}
    file.close()

    # Now convert this dictionary type data into a pandas dataframe
    # specifying what are the column names
    df = pd.DataFrame(data, columns=['Windows', 'Percentage'])

    # Defining the plotsize
    plt.figure(figsize=(12, 9))

    sns.set(rc={'axes.labelsize':10,
                'xtick.labelsize':16,
                'font.size':20,
                'ytick.labelsize':20})
    plots = sns.barplot(x="Windows", y="Percentage", data=df, edgecolor=(0,0,0), linewidth=2)

    # Iterrating over the bars one-by-one
    for bar in plots.patches:
        plots.annotate( str(format(bar.get_height(), '.2f')) + "%", (bar.get_x() + bar.get_width() / 2, 
                        bar.get_height()), ha='center', va='center',
                        size=15, xytext=(0, 8),
                        textcoords='offset points')

    ax = plt.gca()
    ax.set_ylim([0, 100])

    # Setting the x-axis label and its size
    plt.xlabel("Windows", fontsize=25)
    plt.xticks(fontsize=10)
     
    # Setting the y-axis label and its size
    plt.ylabel("Percentage", fontsize=25)

    plt.title("Most used windows by " + argv[1],fontsize=30)

    # Finally plotting the graph
    plt.savefig("./Graphs/Windows" + argv[1] + ".png")

if __name__ == '__main__':
    main()
