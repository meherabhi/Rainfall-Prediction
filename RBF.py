#!/usr/bin/env python
# coding: utf-8

# In[36]:


import netCDF4
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report
from scipy.spatial import distance
from scipy.signal import correlate2d


# In[37]:

#extracting data from .nc files
temp_nc_file = 'tasmax_day_CNRM-CM5_historical_r1i1p1_19800101-19841231.nc'
nc = netCDF4.Dataset(temp_nc_file, mode='r')
lat = nc.variables['lat'][:]
lon = nc.variables['lon'][:]
time_var = nc.variables['time']
dtime = netCDF4.num2date(time_var[:],time_var.units)
maxtemp = nc.variables['tasmax'][:]
templist=[]
templist1=[]


# In[38]:


n=365*3
clusters=52
#K-means before feeding it to the ANN
for i in range(n):
    templist.append(maxtemp[i][85][64])
date=np.linspace(0,n,n).reshape(n,1)
templist=np.asarray(templist)
templist=templist.reshape(n,1)
data=np.concatenate((date,templist),axis=1)
kmeans = KMeans(n_clusters=clusters, random_state=0).fit(data)
labels=kmeans.labels_.reshape(n,1)
centres=kmeans.cluster_centers_
  


# In[39]:

#Training an ANN over the feature vectors
clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(100), random_state=1)
clf.centres=kmeans.cluster_centers_
clf.fit(data, labels.ravel())
testsize=100
testlist=[]
tslabels=[]
for i in range(n,n+testsize):
    testlist.append(maxtemp[i][85][64])
datets=np.linspace(0,testsize,testsize).reshape(testsize,1)
testlist=np.asarray(testlist)
testlist=testlist.reshape(testsize,1)
tsdata=np.concatenate((datets,testlist),axis=1)
for i in range(testsize):
    dist=[]
    for j in range(clusters):
        dist.append(distance.euclidean(tsdata[i,:],centres[j,:]))
    mind=np.argmin(dist)
    tslabels.append(mind)  
topltx=centres[:,0]
toplty=centres[:,1]
fig=plt.figure()
#plotting the trend using cluster centres
arguments=np.argsort(topltx)
for i in range(np.size(centres,0)-1):
    plt.plot((topltx[arguments[i]],topltx[arguments[i+1]]),(toplty[arguments[i]],toplty[arguments[i+1]])) 
plt.show()


# In[40]:


#prediction part
labelspred=clf.predict(tsdata)
print('Accuracy score using an RBF ANN is',clf.score(tsdata,tslabels))
print('Classification report for the ANN predictor ',classification_report(tslabels, labelspred))
fig=plt.figure()
plt.scatter(data[:,0],data[:,1],s=7, c=kmeans.labels_)   
#plt.scatter(kmeans.cluster_centers_[:,0],kmeans.cluster_centers_[:,1],color='black')
plt.xlabel('days of the year')
plt.ylabel('max temperature of the day recorded')
plt.title('clustered data')
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:




