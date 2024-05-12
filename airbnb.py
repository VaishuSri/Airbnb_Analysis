import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image
import seaborn as sns
import matplotlib.pyplot as plt
df1=pd.read_csv("C:/Users/RAMAN/Desktop/DS/PROJECT/air/Airbnb.csv")
print(df1)

#Streamlit part
st.set_page_config(
                    layout= "wide",
                    initial_sidebar_state= "expanded",
               )

# Creating option menu in the side bar
with st.sidebar:
    selected = option_menu("Menu", ["Home","Explore","Overview"], 
                           icons=["house","bar-chart","graph-up"],
                           menu_icon= "menu-button-wide",
                           #default_index=0,
                          )

st.markdown('<h1 style="color:#441273;">AIRBNB ANALYSIS</h1>', unsafe_allow_html=True)

if selected=='Home':
    col1,col2=st.columns(2)
    with col1:
        st.image(Image.open("C:/Users/RAMAN/Desktop/DS/PROJECT/Airbnb/ce100e07-fc5b-485e-8cd3-45f74d02f45f.png"), width=500)
    with col2:
        st.subheader("Airbnb.com was the third most visited travel and tourism website worldwide behind some of its biggest competitors Booking.com and Tripadvisor. Meanwhile, when looking at the most downloaded travel apps worldwide in 2022, Airbnb came in fourth place with 52 million downloads. Comparatively, Google Maps took the top spot with over double the number of downloads. Despite not having the most visited website nor the most downloaded app, Airbnb’s growth does not show signs of slowing down. The company went public in December 2020, making it one of the top initial public offerings (IPOs) that year. Just three years later, in 2023, Airbnb’s global market capitalization was valued at over 73 billion U.S. dollars.")

if selected=='Explore':
    tab1,tab2,tab3=st.tabs(["Geospatial Visualization","Price Analysis and Visualization","Availability Analysis by Season"])
    print(df1)
    print(df1.country.unique())
    

    with tab1:
        data = df1
        country = st.sidebar.multiselect('Select a Country', sorted(data['country'].unique()), sorted(data['country'].unique()))
        prop = st.sidebar.multiselect('Select Property Type', sorted(data['property_type'].unique()), sorted(data['property_type'].unique()))
        room = st.sidebar.multiselect('Select Room Type', sorted(data['room_type'].unique()), sorted(data['room_type'].unique()))
        price = st.sidebar.slider('Select Price Range', min_value=data['price'].min(), max_value=data['price'].max(), value=(data['price'].min(), data['price'].max()))
        # CONVERTING THE USER INPUT INTO QUERY
        query = f'country in {country} & room_type in {room} & property_type in {prop} & price >= {price[0]} & price <= {price[1]}'

        # TOTAL LISTINGS BY COUNTRY CHOROPLETH MAP
        country_df = df1.query(query).groupby(['country'],as_index=False)['name'].count().rename(columns={'name' : 'Listings_name'})
        fig = px.choropleth(country_df,
                            title='Total Listings in each Country',
                            locations='country',
                            locationmode='country names',
                            color='Listings_name',
                            color_continuous_scale=px.colors.sequential.Plasma
                            )
        st.plotly_chart(fig,use_container_width=True)

        # AVG AVAILABILITY IN COUNTRIES SCATTERGEO
        country_df = df1.query(query).groupby('country',as_index=False)['availability'].mean()
        country_df.availability = country_df.availability.astype(int)
        fig = px.scatter_geo(data_frame=country_df,
                                       locations='country',
                                       hover_data=['availability'],
                                       locationmode='country names',
                                       size='availability',
                                       title= 'Avg Availability in each Country',
                                       color_continuous_scale='agsunset'
                            )
        st.plotly_chart(fig,use_container_width=True)

    with tab2:
       
        selected_location = st.sidebar.selectbox('Select Location', df1['street'].unique())
        selected_property_type = st.sidebar.selectbox('Select Property Type', df1['property_type'].unique())

        # Filter data based on user selections
        filtered_data = df1[(df1['street'] == selected_location) & (df1['property_type'] == selected_property_type)]

        # Price analysis
        st.subheader('Price Analysis')

        # Average price by location and property type
        average_price = filtered_data.groupby(['street', 'property_type'])['price'].mean().reset_index()
        st.write(average_price)

        # Dynamic plot - Price distribution
        st.subheader('Price Distribution')
        sns.histplot(filtered_data['price'], kde=True)
        price_dist_fig, price_dist_ax = plt.subplots()
        sns.histplot(filtered_data['price'], kde=True, ax=price_dist_ax)
        st.pyplot(price_dist_fig)

        # Dynamic plot - Price trend over time
        st.subheader('Price Trend Over Time')
        date_column = 'availability'  # Replace 'date_of_listing' with your actual date column
        sns.lineplot(data=filtered_data, x=date_column, y='price')
        price_trend_fig, price_trend_ax = plt.subplots()
        sns.lineplot(data=filtered_data, x=date_column, y='price', ax=price_trend_ax)
        st.pyplot(price_trend_fig)
        
        # Correlation analysis
        st.subheader('Correlation Analysis')

        # Exclude non-numeric columns
        numeric_columns = filtered_data.select_dtypes(include=['number']).columns

        # Calculate correlation matrix
        correlation_matrix = filtered_data[numeric_columns].corr()

        # Visualize correlation matrix
        sns.heatmap(correlation_matrix, annot=True)
        correlation_fig, correlation_ax = plt.subplots()
        sns.heatmap(correlation_matrix, annot=True, ax=correlation_ax)
        st.pyplot(correlation_fig)

    with tab3:
        # Preprocessing: Convert date column to datetime format
        st.markdown("## Availability Analysis")

        # AVAILABILITY BY ROOM TYPE PIE CHART
        fig = px.pie(data_frame=df1.query(query),
                    values='availability',  # Specify the data for the pie chart
                    names='room_type',      # Specify the labels for the pie chart
                    title='Availability by Room Type'
                    )
        st.plotly_chart(fig, use_container_width=True)

if selected=="Overview":
    col1,col2=st.columns(2)
    with col1:

        plt.figure(figsize=(10,8))
        ax = sns.countplot(data=df1,
                           y=df1.property_type.values,
                           order=df1.property_type.value_counts().index[:10])
        ax.set_title("Top 10 Property")
        st.pyplot(plt)

        #Find best host in the Listing name
        plt.figure(figsize=(10,8))
        ax =sns.countplot(data=df1,y=df1.host_name,order=df1.host_name.value_counts().index[:10])
        ax.set_title("Top 10 Hosts with Highest number of Listings")
        st.pyplot(plt)

    with col2:
        data = df1
        country = st.sidebar.multiselect('Select a Country', sorted(data['country'].unique()), sorted(data['country'].unique()))
        prop = st.sidebar.multiselect('Select Property Type', sorted(data['property_type'].unique()), sorted(data['property_type'].unique()))
        room = st.sidebar.multiselect('Select Room Type', sorted(data['room_type'].unique()), sorted(data['room_type'].unique()))
        price = st.sidebar.slider('Select Price Range', min_value=data['price'].min(), max_value=data['price'].max(), value=(data['price'].min(), data['price'].max()))
        # CONVERTING THE USER INPUT INTO QUERY
        query = f'room_type in {room} & property_type in {prop} & price >= {price[0]} & price <= {price[1]}'
        #query = f'country in {country} & room_type in {room} & property_type in {prop} & price >= {price[0]} & price <= {price[1]}'
         # AVG PRICE BY ROOM TYPE BARCHART
        pr_df = df1.query(query).groupby('room_type',as_index=False)['price'].mean().sort_values(by='price')
        fig = px.bar(data_frame=pr_df,
                     x='room_type',
                     y='price',
                     color='price',
                     title='Avg Price in each Room type'
                    )
        st.plotly_chart(fig,use_container_width=True)
        
        # HEADING 2
        st.markdown("## Availability Analysis")
        
        # AVAILABILITY BY ROOM TYPE BOX PLOT
        fig = px.box(data_frame=df1.query(query),
                     x='room_type',
                     y='availability',
                     color='room_type',
                     title='Availability by Room_type'
                    )
        st.plotly_chart(fig,use_container_width=True)








