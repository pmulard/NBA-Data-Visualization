import seaborn as sns
import numpy as np
import sklearn.metrics
import matplotlib.pyplot as plt
import pandas as pd

import downloadStats as ds

#---------- PROGRAM OVERVIEW ----------
	#This program combines two statistical data sets together, one consisting of advanced
	#stats and the other per 36 minutes stats. A diagonal correlation heat map matrix is then
	#constructed to show relationships between the various statistics.


#Retrieves advanced 2019 stats
adv2019 = ds.getStats(2019, "advanced")

#Retrieves per 36 minutes 2019 stats
min362019 = ds.getStats(2019, "per_minute")

#Merges two data sets together
merge = ds.mergeData(adv2019, min362019)


#Creates a diagonal correlation heatmap matrix
#Compute the correlation matrix
corr = merge.corr()

sns.set(style="white")

#Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype = np.bool)
mask[np.triu_indices_from(mask)] = True

#Set up the matplotlib figure
f, ax = plt.subplots(figsize = (22, 22))

#Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap = True)

#Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask = mask, cmap = cmap, vmax = 1, vmin = -1, center = 0,
            square = True, linewidths = .5, cbar_kws = {"shrink": .5})

#Sets the title of the plot
plt.title("2019 NBA Advanced & Per 36 Minutes Stats for All Players")

#Shows the plot on screen
plt.show()