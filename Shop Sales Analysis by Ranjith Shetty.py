#!/usr/bin/env python
# coding: utf-8

#                                                                                                       

# Data Importing

# In[6]:


#import the required libraries

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[ ]:





# In[7]:


#Import the raw datasets

jan_data = pd.read_csv(r"C:\Users\ADMIN\Documents\Data Sets project/Sales_January_2019.csv")
feb_data = pd.read_csv(r"C:\Users\ADMIN\Documents\Data Sets project/Sales_February_2019.csv")
march_data = pd.read_csv(r"C:\Users\ADMIN\Documents\Data Sets project/Sales_March_2019.csv")
april_data = pd.read_csv(r"C:\Users\ADMIN\Documents\Data Sets project/Sales_April_2019.csv")
may_data = pd.read_csv(r"C:\Users\ADMIN\Documents\Data Sets project/Sales_May_2019.csv")
june_data = pd.read_csv(r"C:\Users\ADMIN\Documents\Data Sets project/Sales_June_2019.csv")
july_data = pd.read_csv(r"C:\Users\ADMIN\Documents\Data Sets project/Sales_July_2019.csv")
aug_data = pd.read_csv(r"C:\Users\ADMIN\Documents\Data Sets project/Sales_August_2019.csv")
sep_data = pd.read_csv(r"C:\Users\ADMIN\Documents\Data Sets project/Sales_September_2019.csv")
oct_data = pd.read_csv(r"C:\Users\ADMIN\Documents\Data Sets project/Sales_October_2019.csv")
nov_data = pd.read_csv(r"C:\Users\ADMIN\Documents\Data Sets project/Sales_November_2019.csv")
dec_data = pd.read_csv(r"C:\Users\ADMIN\Documents\Data Sets project/Sales_December_2019.csv")


# In[ ]:





# Data Wrangling

# In[8]:


#Using Concatenate() function to merge all these datasets horizontally

df = pd.concat([jan_data, feb_data, march_data, april_data, may_data,june_data,july_data,aug_data,
               sep_data, oct_data, nov_data, dec_data])


# In[ ]:





# In[9]:


#Making sure to convert the new large dataset into DataFrame to start my analysis

df = pd.DataFrame(df)
df


# In[ ]:





# In[10]:


#Since the NA values are 545 so the ratio is 545/186850 "We can eliminate them", as they don't have much weights on 
#the model we build

df.isna().sum()


# In[ ]:





# In[11]:


# Drop NA values, and modify the Order ID column

df = df.dropna(how='all', inplace=False)
df.drop(df.loc[df['Order ID'] =='Order ID'].index.tolist(), axis=0,inplace=True)
df.info()
df


# In[ ]:





# In[12]:


#Convert these columns into their correct dtype

df['Quantity Ordered'] = pd.to_numeric(df['Quantity Ordered']).astype(int)
df['Price Each'] = pd.to_numeric(df['Price Each']).astype(float)
df['Order Date'] = pd.to_datetime(df['Order Date'])


# In[ ]:





# In[13]:


#Confirm everything works smoothly 

df.info()


# In[ ]:





# In[14]:


# Splitting the location primar location then the state and month

df["Consumer_Primary_Location"] = df['Purchase Address'].apply(lambda x: x.split(',')[0])
df["Consumer_State"] =  df['Purchase Address'].apply(lambda x: x.split(',')[1])
df['Month'] = df['Order Date'].dt.month


# In[ ]:





# How much was earned in 2019?

# In[16]:


#Calculating the revenue "the earnings of 2019"

df['Revenue'] = df['Quantity Ordered'] * df['Price Each']


# In[ ]:





# In[17]:


round(df['Revenue'].sum(), 2)


# In[ ]:





# In[18]:


#Checking the latest corrected Dataset

df


# In[ ]:





# In[19]:


#Creating sub-dataset from the original df to bring more analysis 

Consumer_Usage = df.groupby("Product")[ "Revenue"].sum().sort_values(ascending = False).to_frame(name = 'Total Profits').reset_index()


# In[20]:


Consumer_Usage = pd.DataFrame(Consumer_Usage)
Consumer_Usage


# In[ ]:





# In[ ]:




#We plot the barh plot based on the product and the revenue for each product

plt.figure(figsize = (30,30))
l = Consumer_Usage.groupby('Product')["Total Profits"].mean().plot.barh(figsize=(10,7),  color = ('red', 'cyan'), edgecolor='b')
plt.xlabel('Count')
plt.title('The Properation per Product')

l.bar_label(l.containers[0], label_type='edge')
plt.tight_layout()

l.spines['top'].set_visible(False)
l.spines['right'].set_visible(False)
l.spines['left'].set_visible(False)
l.grid(axis="y")

plt.show()
# In[ ]:





# Interpretation:
- The first best seller is (Macbook Pro Laptop), followed by (Iphone). So both products it's not necessary to apply discounts upon.
- In the second category, (ThinkPad) then (Google Phone) are considered most popular after Apple Products.
# In[ ]:





# In[22]:


#Creating the most states that have the most revenue.

Usage_per_State = df.groupby(["Consumer_State","Month"])["Revenue"].sum().sort_values(ascending = False).to_frame(name = 'Total Revenue').reset_index()


# In[23]:


Usage_per_State = pd.DataFrame(Usage_per_State)
Usage_per_State


# In[ ]:





# In[24]:


#Plotting the Revenue for each state then drawing the average revenue line.

plt.figure(figsize = (30,30))
m = Usage_per_State.groupby('Consumer_State')["Total Revenue"].mean().plot.bar(figsize=(10,7),  color = ('pink', 'green'), edgecolor='b')
plt.xlabel('State Name')
plt.ylabel('The Toal Revenue')
plt.title('The Revenue Properation per State')

m.bar_label(m.containers[0], label_type='edge')
plt.tight_layout()

m.spines['top'].set_visible(False)
m.spines['right'].set_visible(False)
m.spines['left'].set_visible(False)
m.grid(axis="y")

plt.axhline(Usage_per_State["Total Revenue"].mean(), color='red', linewidth=3, linestyle='--')

plt.show()


# In[ ]:





# The Interpretation

# The highest stated that recorded the highest revenue is San Fransico, followed by Los Angles, so based on that we might we consider opening more stores to connect more with our loyal clients. We might want to expand a little in these two areas by focusing on geomgraphic research such as retrieving the essential inforamtion of customers then we start building a personalised marketing campaigns.
# Our average revenue is a little above 300k for 2019.

# In[ ]:





# In[25]:


gg = df.groupby(["Consumer_State","Month"])["Revenue"].count().sort_values(ascending = False).to_frame(name = 'Total_Revenue').reset_index()


# In[26]:


dada = pd.DataFrame(gg)
dada


# In[27]:


plt.figure(figsize = (80,80))
#m = dada.groupby("Month")["Total Revenue"].sum().plot.bar(figsize=(18,15),  color = ('pink', 'green'), edgecolor='b')
n = dada.groupby(["Month", 'Consumer_State'])["Total_Revenue"].sum().plot.barh(figsize=(18,15),  color = ('blue', 'brown'), edgecolor='b')


plt.xlabel('Count')
plt.title('The Properation per State')

n.bar_label(m.containers[0], label_type='edge')
plt.tight_layout()

n.spines['top'].set_visible(False)
n.spines['right'].set_visible(False)
n.spines['left'].set_visible(False)
n.grid(axis="y")

#plt.axhline(dada["Total Revenue"].mean(), color='red', linewidth=3, linestyle='--')

plt.show()


# In[28]:


# set seaborn "whitegrid" theme
sns.set_style("darkgrid")


mme = ["Jan", "Feb", "March", "April", "May", "June", "July", "August", "Sep", "Oct", "Nov", "Dec"] 

plt.figure(figsize=(80,70))

kiki = dada["Total_Revenue"]*1000
# use the scatterplot function
ax = sns.scatterplot(data=dada, x="Month", y="Total_Revenue", size="Total_Revenue", hue='Consumer_State', 
                palette="bright", edgecolors="black", alpha=0.5, sizes=(2000,80000), legend = False)

# Add titles (main and on axis)
plt.xlabel("Month", fontsize = 60)
plt.ylabel("Revenue Amount", fontsize = 60)
plt.title("The Revenue of each State per Month", fontsize = 60)

#sns.set_xticklabels(mme)
plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12], mme, fontsize = 45)
plt.yticks(fontsize = 45)


# Locate the legend outside of the plot

for line in range(0,dada.shape[0]):
     ax.text(dada.Month.iloc[line], dada.Total_Revenue.iloc[line], dada.Consumer_State.iloc[line], horizontalalignment='left', size='xx-large', color='black', weight='semibold')

#plt.legend(bbox_to_anchor=(1,1), loc='upper left', fontsize=40)

# show the graph
plt.show()


# In[ ]:





# The Interpretation:

# - I built up this chart as it has three different variables "Revenue" & "Month" & "Consumer State", we can see that the best state is San Fransco and the starting point of the revenue is higher than any other state, in general the revenue for each month for any other state starts from around 700 dollars, but when it comes to San Fransco it's close to 2300 dollars.
# - The best month we achieve high revenue is on December, October, and April.

# In[29]:


Product_Consumprtion = df.groupby(["Product", "Month"])[ "Revenue"].sum().sort_values(ascending = False).to_frame(name = 'Total_Profits').reset_index()
Product_Consumprtion


# In[ ]:





# In[30]:


# set seaborn "whitegrid" theme
sns.set_style("darkgrid")


mme = ["Jan", "Feb", "March", "April", "May", "June", "July", "August", "Sep", "Oct", "Nov", "Dec"] 

plt.figure(figsize=(80,70))

# use the scatterplot function
ax = sns.scatterplot(data=Product_Consumprtion, x="Month", y="Total_Profits", size="Total_Profits", hue='Product', 
                palette="bright", edgecolors="black", alpha=0.5, sizes=(2500,90000), legend = False)

# Add titles (main and on axis)
plt.xlabel("Month", fontsize = 60)
plt.ylabel("Revenue Amount", fontsize = 60)
plt.title("The Revenue of each Product per Month", fontsize = 60)

#sns.set_xticklabels(mme)
plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12], mme, fontsize = 45)
plt.yticks(fontsize = 45)


# Locate the legend outside of the plot

for line in range(0,Product_Consumprtion.shape[0]):
     ax.text(Product_Consumprtion.Month.iloc[line], Product_Consumprtion.Total_Profits.iloc[line], Product_Consumprtion.Product.iloc[line], horizontalalignment='left', size='xx-large', color='black', weight='semibold')

#plt.legend(bbox_to_anchor=(1,1), loc='upper left', fontsize=40)

# show the graph
plt.show()


# In[ ]:





# ### Conclusion

# In[ ]:


- I have covered the main questions asked, and here's the detailed answers:

    - Q: How much was earned in 2019?  At the end of 2019, the shop totall sales are 33879779.77 dollars.

    - Q: What was the best month for sales? How much was earned that month? December is 
        recorded as the best profitable month for 2019, witha total revenue equal to 677010 dollars.

    - Q: What City had the highest number of sales? The highest number os sales is in San Fransesco state.

    - Q: What time should we display adverstisement to maximize 
    likelihood of customer's buying product? The best time is December, then October, then April.

    - Q: What product sold the most? Why do you think it sold the most?  The top are Apple products 
        which are Macbook Pro Laptop, then Iphone.


# In[ ]:





# ### Limitation

# - The raw dataset isn't complete, if there were more data-related to the consumers such as (Their Age, The Product Rating and Reviews, Historical purchase History, Consumer ID), we would have applied Supervised learning models. and draw more accurate analysis.

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




