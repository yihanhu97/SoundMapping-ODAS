#!/usr/bin/env python
# coding: utf-8

# # Oja's Algorithm

# ## The following cell imports the .db file when run

# In[1]:


#import pandas as pd
import numpy as np
# from sklearn import decomposition
# from matplotlib import pyplot as plt
# import matplotlib.cm as cm
# from matplotlib.pyplot import figure
# import seaborn as sns
# from sklearn.cluster import KMeans
# import glob
import pickle
#from datetime import datetime
#get_ipython().run_line_magic('pylab', 'inline')


# In[2]:


data_with_time = pickle.load(open("july_first_np.p", "rb"))


# From [the fast onvergence of incremental PCA](https://arxiv.org/pdf/1501.03796.pdf)
# 
# ![](figures/OnlinePCAEquations.png)

# ### Explanation of Oja's update
# 
# * $V_n$ - the estimate of the top eigenvector at iteration $n$
# * $\gamma_n$ - learning rate.
# * $X_n$ The $n$th example
# * $X_n X_n^T V_{n-1} = X_n (X_n \cdot V_{n-1})$

# In[3]:


data = data_with_time[:,:12]


# ### calc and subtract mean

# In[4]:


print(data[0])
print(np.asarray(data[0]))


# In[5]:


# Calculating the mean of the data points
print(data.shape)
data_mean = np.nanmean(data,axis = 0,keepdims = True)
print(data_mean)

# subtracting the means from the data matrix

print(data_mean.shape)

data = data - data_mean


# In[6]:


# check that mean is now zero
np.nanmean(data,axis = 0,keepdims = True)


# ## New idea: set nan to zero after subtructing the mean
# After subtracting the mean, we know that the new mean is zero. If we now set all of the nans to zero 
# we create a fully defined data with the mean unchanged. Outer product has to be positive semi-definite.

# In[7]:


np.sum(np.isnan(data))


# In[8]:


cdata=np.nan_to_num(data)
np.sum(np.isnan(cdata))


# In[9]:


#cdata.shape


# In[10]:


# import pandas as pd
#import numpy as np
# from sklearn import decomposition
# from matplotlib import pyplot as plt
# import matplotlib.cm as cm
# from matplotlib.pyplot import figure
# import seaborn as sns
# from sklearn.cluster import KMeans
# import glob

from numpy import linalg as LA

d=9  # dimension
data=data[:,0:d]
cdata=cdata[:,0:d]
n=cdata.shape[0]
block_size=10000
# calculate covariance matrix

outters = np.zeros((d, d))
Sout = np.zeros((d, d, n))
for j in range(n):
    outters += np.outer(cdata[j,:],cdata[j,:])
    Sout[:,:,j]=np.outer(data[j,:],data[j,:]);
#   Sout[:,:,j]=data[j,:] @ data[j,:].T;
#   if j%block_size==0:
#       print('\r %d: '%j,end='')

#for d1 in range(d):
#   for d2 in range(d):
#     Sout[d1,d2,:]
   
cov = outters/n
SCM=np.nanmean(Sout,axis=2)
SCMstd=np.nanstd(Sout,axis=2)
SCMfinite=np.sum(np.isfinite(Sout),axis=2)/n
#eigen values
eigen_values, eigen_vectors = LA.eig(cov)
eigen_valuesSCM, eigen_vectorsSCM = LA.eig(SCM)
