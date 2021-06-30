from sys import meta_path
from pandas.core.indexes.api import get_objs_combined_axis
import streamlit as st
# MAP QUERIES
import pyodbc
import pandas as pd
import numpy as np
import folium
from string import Template
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import folium_static
from PIL import Image
from folium.plugins import TimestampedGeoJson
import pandas as pd
import geopandas as gpd
import geopy
import statistics
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import matplotlib.pyplot as plt
import tqdm
from tqdm import tqdm_notebook
from sql_queries import *


get_data(http_transfer)


@st.cache(allow_output_mutation=True)  #As long as the passed argument(in this time query) wont change, data loading action will not be performed.
def get_data(query):
	cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
											"Server=V10S9-NSSMRTANL;"
											"Database=Trial_Data;"
											"uid=sa;pwd=qclEm!Kllc")
	query = http_transfer
	a = pd.read_sql(query,cnxn)
	return a


# route_df = get_data(ROUTE)
# # def get_route
# count = 0
# sum_lat=0
# sum_lon=0
# mean_lat = []
# mean_lot = []
# for row in route_df.itertuples():
# if count == 20:
# 	mean_lat.append(sum_lat/20)
# 	mean_lot.append(sum_lon/20)
# 	count = 0
# 	sum_lat = 0
# 	sum_lon = 0
# 	sum_lat += row.latitude
# 	sum_lon += row.longitude
# 	count += 1


# else:
# 	sum_lat += row.latitude
# 	sum_lon += row.longitude
# 	count+=1

# series_1 = pd.Series(mean_lat)
# series_2 = pd.Series(mean_lot)
# df = pd.concat([series_1,series_2],axis=1)
# df.rename(columns={0:'lat',1:'lon'},inplace=True)





# sw = df[['lat', 'lon']].min().values.tolist()
# ne = df[['lat', 'lon']].max().values.tolist()
# m = folium.Map([(sw[0]+ne[0])/2, (sw[1]+ne[1])/2], zoom_start=12,zoom_control=np.False_)
# for  row in df.itertuples():
# folium.Circle(radius=3,location=[row.lat,row.lon]).add_to(m)
# m.save("satak.html",stand_alone=False)

###########










st.set_page_config(layout='wide')
header = st.beta_container()
dataset = st.beta_container()
route = st.beta_container()
features = st.beta_container()
c1 = st.sidebar
c2,c4,c3 = st.beta_columns((1,2,3))
modelTraining = st.beta_container()
interactive = st.beta_container()
mapping = st.beta_container()
with header:
	image = Image.open('road.jpg')
	st.image(image,use_column_width=True)
	st.title("Welcome to DT Interactive Web Page")
	type_fail =st.selectbox("Which Type of Events to show in table",options=['Data','Voice'])

	if type_fail =='Data':
		a = get_data(data_fails)
		st.write(a)
		st.header("Data Fail Events RF Distribution")
		add_select = st.selectbox("Which RF Metric Do You Want to See ?",options=['RSRP','RSRQ','SINR'])
		####
		###
		RF_DF= pd.DataFrame(a[add_select].value_counts())
		st.bar_chart(RF_DF)
	else:
		st.header("There is No Data available")
	st.title("A closer look into data")
	#fig = go.Figure(data=go.Table(header=dict(values=),cells=dict()))


	#fig = go.Figure()

with c1:
	st.sidebar.title("Region Selection")
	st.sidebar.selectbox("What city do you want to analyze",("London","Liverpool","Birmingham","Tarlabasi"))
	st.sidebar.title("Technology Selection")
	st.sidebar.radio("Which technology do you want to analyze", options=["4G", "3G", "2G","ALL"])

	st.sidebar.title("Data Test Types")
	st.sidebar.radio("Which technology do you want to analyze", options=["HTTP Browsing", "HTTP Transfer DL", "HTTP Transfer UL","Youtube","All"])
	st.sidebar.title("Voice Test Types")
	st.sidebar.radio("Which technology do you want to analyze", options=["CSFB", "CS","VOLTE","All"])
with c2:

	fail_types = get_data(data_fail_types)
	fail_DF = pd.DataFrame(fail_types['FailType'].value_counts())
	fail_DF.reset_index(inplace=True)
	fig = px.pie(fail_DF,values='FailType',names='index')
	c2.write(fig,use_column_width=True)

with c3:
	Events = fail_types
	Events.dropna(inplace=True)
	sw = Events[['latitude', 'longitude']].min().values.tolist()
	ne = Events[['latitude', 'longitude']].max().values.tolist()
	add_select = st.selectbox("Which Type of Map for Background ?",options=['OpenStreetMap','Stamen Terrain','Stamen Toner'])
	add_select2 = st.selectbox("Which Type of Events Do You Want to See ?",options=['Data','Voice'])

	m = folium.Map([(sw[0]+ne[0])/2, (sw[1]+ne[1])/2], zoom_start=12,zoom_control=False,tiles=add_select)
	st.title('Map of Events')
	def show_maps(df):
		feature_RF = folium.FeatureGroup(name='RF')
		feature_nonRF = folium.FeatureGroup(name='non-RF')
		for lat, lot,type in zip(df['latitude'], df['longitude'],df['FailType']):

			if type == 'Non-RF Related Fail':
				folium.CircleMarker(
				[lat, lot],
				radius=3,
				color='red',
				fill=True,
				fill_color='red',
				fill_opacity=1
			).add_to(feature_nonRF)
			else:
				folium.CircleMarker(
				[lat, lot],
				radius=3,
				color='blue',
				fill=True,
				fill_color='blue',
				fill_opacity=1
				).add_to(feature_RF)
		feature_RF.add_to(m)
		feature_nonRF.add_to(m)
		folium.LayerControl(collapsed=False).add_to(m)
		m.fit_bounds([sw, ne])
		folium_static(m)
	show_maps(Events)








