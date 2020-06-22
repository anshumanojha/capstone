#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
get_ipython().system('{sys.executable} -m pip install pandas')
get_ipython().system('{sys.executable} -m pip install beautifulsoup4')
get_ipython().system('{sys.executable} -m pip install requests')


# In[2]:


from bs4 import BeautifulSoup
import requests
import pandas as pd


# In[3]:


wiki_url = 'https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'
html_text = requests.get(wiki_url).text


# In[4]:


# Extract the table data using BeautifulSoup
soup = BeautifulSoup(html_text)
table = soup.find('table', attrs={'class':'wikitable sortable'})
trs = table.find_all('tr')
print("Number of rows in the table(including columns header): ",
      len(trs))

# Extract the text from all the table cells and add all rows
# to a list of rows.
rows = list()
for tr in trs:
    td = tr.find_all('td')
    row = [ele.text.strip() for ele in td]
    if row:
        # Ignore empty rows with no 'td',
        # applicable for the column headers row.
        rows.append(row)

print("Number of rows with data in the table: ", len(rows))


# In[5]:


df = pd.DataFrame(rows,
                  columns=['PostalCode', 'Borough', 'Neighborhood'])
print("Dataframe shape: ", df.shape)
df.head(10)


# In[6]:


df = df[df.Borough != 'Not assigned']
df.reset_index(inplace=True, drop=True)
print("Dataframe shape: ", df.shape)
df.head(10)


# In[7]:



df['Neighborhood'] = df.apply(
    lambda row: 
    row['Borough'] if row['Neighborhood'] == 'Not assigned' 
    else row['Neighborhood'],
    axis=1)
print("Dataframe shape: ", df.shape)
df.head(10)


# In[9]:



df = df.groupby(['PostalCode', 'Borough'])['Neighborhood'].    apply(', '.join).to_frame()
df.reset_index(inplace=True)


# In[10]:


df.head(12)


# In[11]:


df.shape


# In[ ]:




