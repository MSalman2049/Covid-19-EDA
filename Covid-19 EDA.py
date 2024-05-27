#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use("ggplot")


# In[2]:


covdata = pd.read_csv(r"C:\Users\muham\OneDrive\Desktop\Course Resurces-Python for Data Analysis and Visualization\owid-covid-data.csv")


# In[4]:


pd.set_option('display.max_rows',300)


# In[12]:


covdata['location'].unique()


# In[9]:


#list of non country locations that should be removed from the data - we already have the continent column for this
# for data for the world, we can use the sum of all locations instead.

nonclocations = ['Asia','Low income','South America','North America','Upper middle income','World','Oceania','High income','European Union', 'Lower middle income','Europe', 'Africa']



# In[13]:


#Removing the non-country locations data that will skew future plots.
for x in covdata.index:
    if covdata.loc[x, 'location'] in nonclocations:
        covdata.drop(x, inplace = True)


# In[18]:


# New list of locations
covdata['location'].unique()


# In[19]:


covdata


# In[21]:


# Now that the extra data is removed, we should have a more accurate representation of the new cases in the world
# We will prepare the data by changing the date to datetime and grouping the sum of cases by each date
covdata2 = covdata.copy()
covdata2.date = pd.to_datetime(covdata2['date'])
covdata2 = covdata2.groupby('date').sum()


# In[22]:


# Create new columns to look at the weekly trend of new case and new deaths in the world
covdata2['7 days MA new cases'] = 0
covdata2['7 days MA new cases'] = covdata2['new_cases'].rolling(7).mean() 
covdata2['7 days MA new deaths'] = 0
covdata2['7 days MA new deaths'] = covdata2['new_deaths'].rolling(7).mean() 


# In[29]:

# A visaul representation of the new case in the world over the course of the pandemic.
covdata2[['new_cases', '7 days MA new cases']].plot(figsize = (11, 5), alpha = 0.5)
plt.title('Timeline new cases in world')
plt.xlabel('Date')
plt.ylabel('New cases')

plt.show()


# In[28]:

# A visaul representation of the new deaths in the world over the course of the pandemic.
covdata2[['new_deaths', '7 days MA new deaths']].plot(figsize = (11, 5), alpha = 0.5)
plt.title('Timeline new deaths in world')
plt.xlabel('Date')
plt.ylabel('New Deaths')

plt.show()


# In[ ]:





# In[45]:


# Now to focus on Canada
covCanada = covdata[covdata['location']== 'Canada']
covCanada.reset_index(inplace = True)


# In[46]:


# Similar to the above charts for weekly average of new covid cases/deaths in the world, we will focus on the same for Canada
covCanada.date = pd.to_datetime(covCanada['date'])
covCanada = covCanada.groupby('date').sum()
covCanada['7 days MA new cases'] = 0
covCanada['7 days MA new cases'] = covCanada['new_cases'].rolling(7).mean()
covCanada['7 days MA new deaths'] = 0
covCanada['7 days MA new deaths'] = covCanada['new_deaths'].rolling(7).mean()

# A visaul representation of the new cases in the Canada over the course of the pandemic.
covCanada[['new_cases', '7 days MA new cases']].plot(figsize = (10, 5), alpha = 0.5)
plt.title('Timeline new cases in Canada')
plt.xlabel('Date')
plt.ylabel('New cases')

# A visaul representation of the new deaths in the Canada over the course of the pandemic.
covCanada[['new_deaths', '7 days MA new deaths']].plot(figsize = (10, 5), alpha = 0.5)
plt.title('Timeline new deaths in Canada')
plt.xlabel('Date')
plt.ylabel('New deaths')

plt.show()


# In[3]:

#Creating a new dataframe to map out potential correlations between key statistics in the Covid-19 cases database.
covdata3 = covdata[['location','total_cases','total_deaths','life_expectancy','female_smokers','male_smokers','total_vaccinations_per_hundred','total_deaths_per_million','handwashing_facilities','hospital_beds_per_thousand','human_development_index']].groupby(by = 'location').max('total_cases')
covdata3.reset_index(inplace = True)
covdata3


# In[4]:

# Importing plotyly express for interactive visualizations.
import plotly.express as px


# In[5]:


# One of the most important factors to reducing covid cases was the distribution of vaccinations
# A key correlation can be seen between the human development index of the country and the total number of vaccinations per 100.
# The below scatter plot shows that countries with higher human development index had a higher number of vaccinations per 100
fig = px.scatter(covdata3, y="human_development_index", x="total_vaccinations_per_hundred", color="location", hover_data=['total_cases','total_deaths'],trendline="rolling")

fig.show()


# In[8]:


condata = pd.read_csv(r"C:\Users\muham\OneDrive\Desktop\Course Resurces-Python for Data Analysis and Visualization\owid-covid-data.csv")


# In[155]:


sns.scatterplot(x='continent',y='total_cases',data=condata,color=['blue']).set(title = 'Total cases per continent')
plt.xticks(rotation = 'vertical')

sns.despine()
plt.plot()


# In[9]:


contotals = condata[['continent', 'total_cases','total_deaths']].groupby(by = 'continent').max()
contotals.reset_index(inplace = True)


# In[10]:


fig2 = px.bar(contotals, x='continent', y='total_deaths', color="continent", title="Total Deaths per Continent as of March 2022")

fig2.show()


# In[12]:


fig3 = px.bar(contotals, x='continent', y='total_cases', color="continent", title="Total Cases per Continent/Region as of March 2022")

fig3.show()


# In[ ]:




