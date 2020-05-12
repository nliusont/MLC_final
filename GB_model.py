#!/usr/bin/env python
# coding: utf-8

# In[59]:


import time
import pickle
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error as MSE
from sklearn.metrics import r2_score
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV
import shap


# In[60]:


#import data
X = pd.read_csv('files/X.csv', index_col=0)
y = pd.read_csv('files/y.csv', header=0, index_col=0)

#import data
X_train = pd.read_csv('files/X_train.csv', index_col=0)
y_train = pd.read_csv('files/y_train.csv', header=0, index_col=0)

#import data
X_test = pd.read_csv('files/X_test.csv', index_col=0)
y_test = pd.read_csv('files/y_test.csv', header=0, index_col=0)

#import df11
df11 = pd.read_csv('files/df11.csv', index_col=0, header=0)


# In[61]:


# mark whether each building that was in the training or test set
def checkIfValuesExists(dfObj, listOfValues):
    ''' Check if given elements exists in dictionary or not.
        It returns a dictionary of elements as key and thier existence value as bool'''
    resultDict = {}
    # Iterate over the list of elements one by one
    for elem in listOfValues:
        # Check if the element exists in dataframe values
        if elem in dfObj.values:
            resultDict[elem] = 'Train'
        else:
            resultDict[elem] = 'Test'
    # Returns a dictionary of values & thier existence flag        
    return resultDict

dict = checkIfValuesExists(y_train.index ,y.index.values)
gb_train_test = pd.DataFrame.from_dict(dict, orient='index')


# In[62]:


# instantiate gb
gb = GradientBoostingRegressor(n_estimators=500, max_depth=6, min_samples_split=3, max_features=5, subsample=1, learning_rate=0.025)

# train model
gb.fit(X_train, y_train.values.ravel())
y_train_pred = gb.predict(X_train)

y_pred = gb.predict(X_test)

# predict all data

y_pred_all = gb.predict(X)

r2_gb_train = r2_score(y_train, y_train_pred)
r2_gb = r2_score(y_test, y_pred)
r2_gb_all = r2_score(y,y_pred_all)
print("Training set r_sq: {:.2f}".format(r2_gb_train))
print("Test set r_sq: {:.2f}".format(r2_gb))
print("Whole set r_sq: {:.2f}".format(r2_gb_all))


# In[63]:


#create a results df
gb_results = df11[['source_eui_norm']]
gb_results['gb_source_eui_norm'] = y_pred_all

#mark each building if it was in the train or test set
gb_results = gb_results.merge(gb_train_test, how='left', left_index=True, right_index=True)
gb_results.rename(columns = {0:'gb_train_test'}, inplace = True) 


# In[67]:


#graph
sns.set(style="dark")
sns.set("talk")
pyplot.figure(figsize=(10,10))
ax = sns.scatterplot(x=y_test['source_eui_norm'], y=y_pred, alpha=0.8)
pyplot.plot([0, 400], [0, 400], color = 'black', linewidth = 1, alpha=0.3)
pyplot.xlim(0,400)
pyplot.ylim(0,300)
ax.set_title('Gradient Boosting Test Set')
ax.set_xlabel('actual EUI')
ax.set_ylabel('predicted EUI')
pyplot.show()
pyplot.savefig("figures/GB.png")


# In[53]:


shap.initjs()

# explain the model's predictions using SHAP
explainer = shap.TreeExplainer(gb)
shap_values = explainer.shap_values(X)



#shap summary plot
shap.summary_plot(shap_values, X, plot_size=(15,12), show=False)
pyplot.xlim(-30,30)
pyplot.title('Gradient Boosting SHAP Plot')
pyplot.savefig('Figures/GB_shap.png')


# In[ ]:




