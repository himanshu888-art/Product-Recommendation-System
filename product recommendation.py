#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns


# In[3]:


books = pd.read_csv('Books.csv')
users = pd.read_csv('Users.csv')
ratings = pd.read_csv('Ratings.csv')


# # # Exploratory Data Analysis 

# In[4]:


books.head(5)


# In[5]:


users.head(5)


# In[6]:


ratings.head(5)


# In[7]:


print(books.shape)
print(ratings.shape)
print(users.shape)


# In[8]:


books.isnull().sum()


# In[9]:


ratings.isnull().sum()


# In[10]:


users.isnull().sum()


# In[11]:


books.duplicated().sum()


# In[13]:


ratings.duplicated().sum()


# In[14]:


users.duplicated().sum()


# In[15]:


print(books.dtypes)


# In[16]:


print(users.dtypes)


# In[18]:


print(ratings.dtypes)


# # create visualiztion for specific columns  

# In[19]:


plot = sns.pairplot(users,  height = 2.5)
plot.fig.suptitle("Pairwise relationships between features of the users", y=1.05)
plt.show()


# ## popularity based- Recomandation system 

# In[21]:


rating_with_name = ratings.merge(books, on='ISBN')


# In[22]:


num_rating_df = rating_with_name.groupby('Book-Title').count()['Book-Rating'].reset_index()
num_rating_df.rename(columns={'Book-Rating':'num_ratings'}, inplace = True)
num_rating_df


# In[23]:


avg_rating_df = rating_with_name.groupby('Book-Title').mean(numeric_only = True)['Book-Rating'].reset_index()
avg_rating_df.rename(columns={'Book-Rating':'avg_rating'}, inplace = True, )
avg_rating_df


# In[24]:


popular_df = num_rating_df.merge(avg_rating_df, on='Book-Title')
popular_df


# In[25]:


popular_df = popular_df[popular_df['num_ratings']>=250].sort_values('avg_rating',ascending=False).head(50) 


# In[26]:


popular_df = popular_df.merge(books, on='Book-Title').drop_duplicates('Book-Title')[['Book-Title','Book-Author','Image-URL-M','num_ratings','avg_rating']]


# In[51]:


popular_df['Image-URL-M'][0]


# ## collaborative flitering based recommedation 

# In[28]:


x = rating_with_name.groupby('User-ID').count()['Book-Rating'] > 200
phada_likha_user = x[x].index


# In[29]:


filtered_rating=rating_with_name[rating_with_name['User-ID'].isin(phada_likha_user)]


# In[30]:


y = filtered_rating.groupby('Book-Title').count()['Book-Rating']>=50
famous_books = y[y].index


# In[31]:


final_ratings = filtered_rating[filtered_rating['Book-Title'].isin(famous_books)]


# In[32]:


pt = final_ratings.pivot_table(index='Book-Title',columns='User-ID',values='Book-Rating')


# In[33]:


pt.fillna(0,inplace=True)


# In[34]:


pt


# In[35]:


from sklearn.metrics.pairwise import cosine_similarity


# In[36]:


similarity_scores = cosine_similarity(pt)


# In[37]:


similarity_scores.shape


# In[38]:


def recommend(book_name):
    # index fetch
    index = np.where(pt.index==book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:5]
    
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(item)
    
    return data


# In[39]:


recommend('1984')


# In[40]:


pt.index[545]


# In[48]:


import pickle
pickle.dump(popular_df,open('popular.pkl','wb'))


# In[52]:


books.drop_duplicates('Book-Title')


# In[53]:


pickle.dump(pt,open('pt.pkl','wb'))
pickle.dump(books,open('books.pkl','wb'))
pickle.dump(similarity_scores,open('similarity_scores.pkl','wb'))


# In[ ]:





# In[ ]:





# In[ ]:




