amazonnAPP.py
import pandas as pd
import streamlit as st
import plotly.express as px
st.set_page_config(page_title='amazon results',layout='wide')
df=pd.read_csv('cleaned amazon dataframe')
st.title('amazon orders analysis dashboard')
st.sidebar.header('filters')


page=st.sidebar.radio('choose section',
                      ['overview',
                       'dashboard',
                       'orders by categories',
                       'order status',
                       'shipping service',
                       'b2b analysis',
                       'promotions',
                       'geography',
                       'time analysis',
                       'fulfilment vs status',
                       'size analysis',
                       'month period analysis'
                      ])


select_status=st.sidebar.multiselect('select statu',df['status'].unique())
select_day=st.sidebar.multiselect('select day',df['day'].unique())
select_month=st.sidebar.multiselect('select month',df['month'].unique())
select_category=st.sidebar.multiselect('select category',df['category'].unique())
select_size=st.sidebar.multiselect('select size',df['size'].unique())
select_b2b_or_b2c=st.sidebar.radio('select b2b or not',df['b2b'].unique())
select_type_of_fulfilment=st.sidebar.radio('select fulfilment',df['fulfilment'].unique())
select_state=st.sidebar.multiselect('select state',df['ship state'].unique())
select_city=st.sidebar.multiselect('select city',df['ship city'].unique())
select_period=st.sidebar.selectbox('select period',df['month periods'].unique())
select_promotion=st.sidebar.multiselect('select promotion',df['promotion ids update'].unique())
min_qty,max_qty=st.slider('select quantity',int(df['qty'].min()),int(df['qty'].max()),
                          (int(df['qty'].min()),int(df['qty'].max())))
min_amount,max_amount=st.slider('select amount',float(df['amount'].min()),float(df['amount'].max()),
                                (float(df['amount'].min()),float(df['amount'].max())))
select_ship_service_level=st.sidebar.radio('select ship service level',df['ship service level'].unique())


filtered_df=df.copy()
if select_status:
    filtered_df=filtered_df[filtered_df['status'].isin(select_status)]
if select_day:
    filtered_df=filtered_df[filtered_df['day'].isin(select_day)]
if select_month:
    filtered_df=filtered_df[filtered_df['month'].isin(select_month)]
if select_size:
    filtered_df=filtered_df[filtered_df['size'].isin(select_size)]
if select_b2b_or_b2c:
    filtered_df=filtered_df[filtered_df['b2b']==select_b2b_or_b2c]
if select_state:
    filtered_df=filtered_df[filtered_df['ship state'].isin(select_state)]
if select_city:
    filtered_df=filtered_df[filtered_df['ship city'].isin(select_city)]
if select_period:
    filtered_df=filtered_df[filtered_df['month periods']==select_period]
if select_promotion:
    filtered_df=filtered_df[filtered_df['promotion ids update'].isin(select_promotion)]
if select_type_of_fulfilment:
    filtered_df=filtered_df[filtered_df['fulfilment']==select_type_of_fulfilment]
if select_ship_service_level:
    filtered_df=filtered_df[filtered_df['ship service level']==select_ship_service_level]
if select_category:
    filtered_df=filtered_df[filtered_df['category'].isin(select_category)]
    

min_value,max_value=min_qty,max_qty
filtered_df=filtered_df[(filtered_df['qty']>=min_value)&(filtered_df['qty']<=max_value)]
min_value2,max_value2=min_amount,max_amount
filtered_df=filtered_df[(filtered_df['amount']>=min_value2)&(filtered_df['amount']<=max_value2)]


st.dataframe(filtered_df)

#dashboard

#over view:
if page == 'overview':
    st.header('dataset overview')
    col1,col2,col3=st.columns(3)
    col1.metric('total orders = ',len(filtered_df))
    col2.metric('total cities = ',filtered_df['ship city'].nunique())
    col3.metric('total of categories = ',filtered_df['category'].nunique())
#1 orders by category:
elif page=='orders by categories':
    st.header('orders by category')
    fig1=px.histogram(filtered_df,x='category')
    st.plotly_chart(fig1,use_container_width=True)
#2 orders status
elif page=='order status':
    st.header('order status distribution')
    fig2=px.histogram(filtered_df,x='status')
    st.plotly_chart(fig2,use_container_width=True)

#3 ship service level
elif page=='shipping service':
    st.header('shipping service level vs status')
    fig3=px.histogram(filtered_df,x='ship service level',color='status')
    st.plotly_chart(fig3,use_container_width=True)

#4 b2b analysis
elif page=='b2b analysis':
    st.header('b2b orders by category and status')
    fig4=px.histogram(filtered_df,x='category',color='b2b')
    st.plotly_chart(fig4,use_container_width=True)
    fig5=px.histogram(filtered_df,x='status',color='b2b')
    st.plotly_chart(fig5,use_container_width=True)
    
#5 promotions

elif page=='promotions':
    st.header('promotion ids vs status')
    fig6=px.histogram(filtered_df,x='promotion ids',color='status')
    st.plotly_chart(fig6,use_container_width=True)
    
#6 geography analysis
elif page=='geography':
    st.header('orders by cities and states')
    state_orders=filtered_df.groupby('ship state').size().reset_index(name='state orders')
    cities_orders=filtered_df.groupby('ship city').size().reset_index(name='city orders')
    fig7=px.bar(state_orders.sort_values(by='state orders',ascending=False).head(10),x='ship state',y='state orders')
    st.plotly_chart(fig7,use_container_width=True)
    fig8=px.bar(cities_orders.sort_values(by='city orders',ascending=False).head(10),x='ship city',y='city orders')
    st.plotly_chart(fig8,use_container_width=True)

#7 time analysis
elif page=='time analysis':
    st.header('orders over time')
    fig9=px.histogram(filtered_df,x='month')
    st.plotly_chart(fig9,use_container_width=True)
    fig10=px.histogram(filtered_df,x='day')
    st.plotly_chart(fig10,use_container_width=True)
    
#8 fulfilment vs status
elif page== 'fulfilment vs status':
    st.header('fulfilment vs delivered')
    filtered_df['delivered status']=filtered_df['status'].apply(lambda x:'Delivered to Buyer' if x=='Delivered to Buyer' else 'other')
    fig11=px.histogram(filtered_df,x='fulfilment',color='delivered status')
    st.plotly_chart(fig11,use_container_width=True)
    
#9 size analysis
elif page=='size analysis':
    st.header('size vs category')
    fig12=px.histogram(filtered_df,x='size',color='category')
    st.plotly_chart(fig12,use_container_width=True)
    
elif page== 'month period analysis':
    st.header('orders between periods')
    fig13=px.histogram(filtered_df,x='month periods')
    st.plotly_chart(fig13,use_container_width=True)
    