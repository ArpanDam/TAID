# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 10:49:58 2022

@author: HP
"""

import matplotlib.pyplot as plt


x=[1,2,3,4,5]
y=[3,4,5,6,7]  
plt.xticks([2,4])
plt.plot(x, y)  # Plot the chart
plt.xlabel("Number of iteration")
plt.ylabel("Gain")
plt.savefig('Gain.png')
plt.close()  
plt.xticks([2,4])
y=[23,45,67,45,56]
plt.plot(x, y)  # Plot the chart
plt.xlabel("Number of iteration")
plt.ylabel("Number_of_influenced_node")
plt.savefig('Number_of_influenced_node.png') 