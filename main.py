# !apt install gdal-bin python-gdal python3-gdal
# !apt install python3-rtree
# !pip install git+git://github.com/geopandas/geopandas.git
# !pip install descartes
# !pip install folium
# !pip install plotly_express
# !pip install geopandas


import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
import sys
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


df=pd.read_csv('Datafiniti_Hotel_Reviews.csv')
columns_to_remove = ['id','dateAdded','dateUpdated','keys','postalCode','province','reviews.date','reviews.dateSeen']
df = df.drop(columns=columns_to_remove)
filtered_data = df[df['reviews.rating'] >= 3]
df= filtered_data.drop_duplicates(subset=['name', 'reviews.rating'])
df.head()
df.shape
df

# rows,cols= df.shape
# unique_ratings, counts = np.unique(df['reviews.rating'], return_counts=True)
# plt.bar(unique_ratings, counts)
# plt.xlabel('Rating')
# plt.ylabel('Count')
# plt.title('Number of Ratings by Rating Value')
# plt.show()



Las_Vegas=df[df.city == 'Las Vegas']
Boston=df[df.city=='Boston']
Miami_Beach=df[df.city=='Miami Beach']
Chicago=df[df.city=='Chicago']
San_Francisco=df[df.city=='San Francisco']
San_Diego=df[df.city=='San Diego']
New_Orleans=df[df.city=='New Orleans']
Atlanta=df[df.city=='Atlanta']
Hyattsville=df[df.city=='Hyattsville']
Baltimore=df[df.city=='Baltimore']
Springfield=df[df.city=='Springfield']
Virginia_Beach=df[df.city=='Virginia Beach']

List=["Las_Vegas","Boston","Miami_Beach","Chicago","San Diego","San_Francisco","New_Orleans","Baltimore",
      "Atlanta","Springfield","Virginia Beach","Hyattsville"]

# for i,j in enumerate(List):
#   print(f"{i}: {j}")

cityplace=sys.argv[1]
longitude=float(sys.argv[2])
latitude=float(sys.argv[3])

# cityplace=input("enter city")
# longitude=float(input("enter long"))
# latitude=float(input("enter latitu"))



if(cityplace=='Las_Vegas'):
  coords=Las_Vegas[['longitude','latitude']]
  c=Las_Vegas

elif(cityplace=="Boston"):
  coords=Boston[['longitude','latitude']]
  c=Boston

elif(cityplace=="Miami_Beach"):
  coords=Miami_Beach[['longitude','latitude']]
  c=Miami_Beach

elif(cityplace=='Baltimore'):
  coords=Baltimore[['longitude','latitude']]
  c=Baltimore

elif(cityplace=='Springfield'):
  coords=Springfield[['longitude','latitude']]
  c=Springfield

elif(cityplace=="San Diego"):
  coords=San_Diego[['longitude','latitude']]
  c=San_Diego

elif(cityplace=="Chicago"):
  coords=Chicago[['longitude','latitude']]
  c=Chicago

elif(cityplace=="San_Francisco"):
  coords=San_Francisco[['longitude','latitude']]
  c=San_Francisco

elif(cityplace=="Virginia Beach"):
  coords=Virginia_Beach[['longitude','latitude']]
  c=Virginia_Beach

elif(cityplace=="New_Orleans"):
  coords=New_Orleans[['longitude','latitude']]
  c=New_Orleans

elif(cityplace=="Hyattsville"):
  coords=Hyattsville[['longitude','latitude']]
  c=Hyattsville

else:
  coords=Atlanta[['longitude','latitude']]
  c=Atlanta




distortions=[]
K=range(1,20)
for k in K:
  kmeansModel=KMeans(n_clusters=k)
  kmeansModel=kmeansModel.fit(coords)
  distortions.append(kmeansModel.inertia_)


from sklearn.metrics import silhouette_score
silhoutte=[]
kmax=20

for k in range(2,kmax):
  kmeans=KMeans(n_clusters = k).fit(coords)
  labels=kmeans.labels_
  silhoutte.append(silhouette_score(coords,labels,metric='euclidean'))

kmeans=KMeans(n_clusters=5,init='k-means++')
kmeans.fit(coords)
y=kmeans.labels_
# print("k=5","silhoutte_Score",silhouette_score(coords, y,metric='euclidean'))



c['cluster']=kmeans.predict(c[['longitude','latitude']])
c.head()
top_restaurants=c.sort_values(by=['reviews.rating'],ascending=False)
top_restaurants.head()


def recommendation(df,longitude,latitude):
  cluster=kmeans.predict(np.array([longitude,latitude]).reshape(1,-1))[0]
  cluster_hotels = df[df['cluster'] == cluster]
  unique_hotels = cluster_hotels.drop_duplicates(subset=['name'])
  return unique_hotels.iloc[0:5][['name', 'latitude', 'longitude']]


rest=recommendation(top_restaurants,longitude, latitude)
rest.reset_index(drop=True, inplace=True)
from tabulate import tabulate

# Convert the DataFrame to a table format
table = tabulate(rest, headers='keys', tablefmt='pipe')

# Print the table with borders
print(table)

# grouped_data = df.groupby('name')['reviews.rating'].unique()
# for name, ratings in grouped_data.items():
#     print(f"Name: {name}")
#     print(f"Unique Review Ratings: {ratings}")
#     print()

import plotly
import plotly.offline as py
import plotly.graph_objs as go
import plotly_express as px

px.set_mapbox_access_token("pk.eyJ1IjoiYWJoaXJhbWFiaGkiLCJhIjoiY2xqbGw1bGFlMDgzcTNqbW4wazJ2dTk5MCJ9.Yj13nzdFb7tShA8nUS0NIw")
fig=px.scatter_mapbox(c,lat="latitude",lon="longitude",color="reviews.rating",hover_data=['name','longitude','latitude'],size_max="30",zoom=3,width=1200,height=800)

fig.show()