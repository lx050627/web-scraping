#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np

def draw_pie(quants):
    # make a square figure 
    plt.figure(1, figsize=(6, 6))
    labels = ['A', 'B', 'C', 'D', 'E', 'F']
    expl = [0.05, 0, 0, 0, 0, 0]
    colors = ["green", "yellow", "coral", "blue", "orange" "red"]
    plt.pie(quants, explode=expl, colors=colors, labels=labels, autopct='%1.1f%%', pctdistance=0.8)
    plt.title('Grades Summary', bbox={'facecolor': '0.8', 'pad': 5})
    plt.show()
    plt.close()

def draw_bar(quants):
    fig, ax = plt.subplots()
    plt.figure(1, figsize=(6, 6))
    opacity = 0.66

    ind = np.arange(6)  # the x locations for the groups
    width=0.35   # the width of the bars

    ax.set_title("Grades Summary")
    ax.set_ylabel("Number")
    ax.set_xlabel("Grade")
    ax.set_xticks(ind)
    ax.set_xticklabels(('A', 'B', 'C', 'D', 'E','F'))
    ax.set_yticks([y for y in range(max(quants)+1)])
    ax.bar(ind,quants,width,alpha=opacity,color='b')
    plt.show()
    plt.close()








