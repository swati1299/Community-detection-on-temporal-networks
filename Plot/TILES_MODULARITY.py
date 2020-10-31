import os
import matplotlib.pyplot as plt
import csv
base=os.getcwd()
path=str(base)+"/TILES_SCORES/tiles_modularity.csv"
file=open(path,"r")
creader=csv.reader(file)
fields=next(creader)
x_axis=[]
y_axis=[]
for row in creader:
    x=int(row[0])
    y=float(row[1])
    x_axis.append(x)
    y_axis.append(y)
plt.plot(x_axis, y_axis, color='blue', linewidth=2)
plt.xlabel('Time')
# Set the y axis label of the current axis.
plt.ylabel('Modularity')
# Set a title of the current axes.
plt.title("Modularity for TILES")
# show a legend on the plot
# Display a figure.
plt.show()
