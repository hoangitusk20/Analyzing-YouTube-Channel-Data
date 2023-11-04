import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime
from isodate import parse_duration

chanel_df = pd.read_csv('datasets/data_preprocess.csv')
vietnam_df = chanel_df[chanel_df["country_name"] == "Vietnam"]

recent_video = pd.read_csv('datasets/video_details.csv')

st.set_page_config(page_title = "Tổng quan Việt Nam", layout = 'wide', 
                   initial_sidebar_state = 'expanded')

with st.sidebar:
    top_n = st.slider('Chọn số lượng kênh hiển thị', 10, 20, 10)
    top_n_topic = st.slider('Chọn số lượng topic hiển thị', 10, 20, 15)

### Title

st.markdown(f'<h1 style="text-align: center;">TỔNG QUAN CÁC KÊNH YOUTUBE Ở VIỆT NAM</h1>', unsafe_allow_html=True)  

st.markdown("## Phân tích tổng quan các kênh youtube Việt Nam")


# TOP CHANNEL
most_sub_channels = vietnam_df.sort_values(by='subscribers', ascending=False).head(top_n).sort_values(by='subscribers', ascending=True)

most_view_channels = vietnam_df.sort_values(by='video_views', ascending=False).head(top_n).sort_values(by='video_views', ascending=True)


col1, col2 =  st.columns(2)
with col1:
    fig = px.bar(most_sub_channels, x='subscribers', y='channel_name', orientation='h',
    title=f'Top {top_n} Channels with Highest Subscribers')
    fig.update_layout(xaxis_title='Subscribers', yaxis_title='Channel Name')
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
with col2:
    fig = px.bar(most_view_channels, x='video_views', y='channel_name', orientation='h',
    title=f'Top {top_n} Channels with Highest video views')
    fig.update_layout(xaxis_title='Total video views', yaxis_title='Channel Name')
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

## PHÂN TÍCH THEO CHANNEL TYPE

col1, col2 = st.columns((7,3))

def subscribe_view_channelType(method):
    fig = go.Figure()
    df_agg = vietnam_df.groupby('channel_type').agg({'subscribers': method, 'video_views': method}).reset_index()
    
    fig.add_trace(go.Bar(x=df_agg['channel_type'], y=df_agg['subscribers'], name='subscribers', yaxis='y'))
    # Vẽ biểu đồ số view (đường)
    fig.add_trace(go.Scatter(x=df_agg['channel_type'], y=df_agg['video_views'], mode='lines', name='View', yaxis='y2'))
    # Đặt layout cho biểu đồ
    fig.update_layout(
        title='Biểu đồ số view và số subscribe theo loại channel',
        xaxis=dict(title='Channel Type'),
        yaxis=dict(title='Số Subscribe', side='left'),
        yaxis2=dict(title='Số View', side='right', overlaying='y'),
        legend=dict(x=0.7, y=1)
        )
    return fig

with col1:

    # Vẽ biểu đồ số subscribe (cột)
    tab1, tab2 = st.tabs(["Sum", "Mean"])
    tab1.plotly_chart(subscribe_view_channelType('sum'), theme="streamlit", use_container_width=True)
    tab2.plotly_chart(subscribe_view_channelType('mean'), theme="streamlit", use_container_width=True)   
with col2:
    count_channel_type = vietnam_df.groupby("channel_type")["channel_id"].count()
    count_channel_type_df = pd.DataFrame({"channel_type": count_channel_type.index, "count": count_channel_type.values})

    fig = go.Figure(data=[go.Pie(labels=count_channel_type_df['channel_type'], values=count_channel_type_df['count'], hole=0.4)])

    # Đặt layout cho biểu đồ
    fig.update_layout(
        title='Biểu đồ cơ cấu channel type'
    )
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

#PHÂN TÍCH THEO VIDEO
st.markdown("## Phân tích theo video của kênh")

# Metric
col1, col2, col3, col4 = st.columns(4)

##Median uploads
median_uploads = vietnam_df['uploads'].median()

##Most common channel type
def to_list(str_list):
    return eval(str_list)

topic_series = recent_video['topic'].dropna().apply(to_list).explode("topic")
topic_counts = topic_series.value_counts()
most_common_topic = topic_counts.idxmax()

## Thời lượng trung vị
duration = recent_video['duration']

def to_total_seconds(duration):
    return parse_duration(duration).total_seconds() 

duration = duration. apply(to_total_seconds)

recent_video['duration_second'] = duration


median_duraion = round(duration.median(), 2)

#Chu kỳ up video (ngày)

df = pd.DataFrame(recent_video)

df['publish_at'] = pd.to_datetime(df['publish_at'])


df = df.sort_values('publish_at')

df['upload_cycle'] = df.groupby('channel_id')['publish_at'].diff().dt.total_seconds() / 86400

average_upload_cycle = df.groupby('channel_id')['upload_cycle'].mean()
median_upload_cycle = round(average_upload_cycle.median(),2)


with col1:
    st.metric(label="Số video trung vị", value=median_uploads)
with col2:
    st.metric(label="Topic phổ biến", value=most_common_topic)
with col3:
    st.metric(label="Thời lượng trung vị (giây)", value=median_duraion)
with col4:
    st.metric(label="Chu kỳ upload trung vị (ngày)", value=median_upload_cycle)


def remove_with_iqr(data, col):
    q1=data[col].quantile(0.25)
    q3=data[col].quantile(0.75)
    iqr = q3 - q1
    upper=q1-1.5*iqr
    lower=q3+1.5*iqr
    clean_data=data[~((data[col]<(upper))  |  (data[col]>(lower)))]
    return clean_data

recent_video_remove_outlier = remove_with_iqr(recent_video, 'duration_second')
fig = px.histogram(recent_video_remove_outlier, x="duration_second", title = "Histogram phân bố thời lượng video")
st.plotly_chart(fig, theme="streamlit", use_container_width=True)

#PHÂN TÍCH THEO TOPIC
col1, col2 = st.columns(2)
common_topic = recent_video['topic'].dropna().apply(to_list).explode("topic").value_counts()
common_topic = common_topic.head(top_n_topic).sort_values(ascending= True)
fig = px.bar(common_topic, x=common_topic.values, y=common_topic.index, orientation='h',
title=f'Top {top_n_topic} topic phổ biến')
fig.update_layout(xaxis_title='Count', yaxis_title='Topic')
col1.plotly_chart(fig, theme="streamlit", use_container_width=True)

recent_video_explode = recent_video.copy()
recent_video_explode['topic'] = recent_video_explode['topic'].dropna().apply(to_list)
recent_video_explode = recent_video_explode.explode("topic")
recent_video_explode = recent_video_explode[recent_video_explode['topic'].isin(common_topic.index)]


def view_duration_topic(method):
    fig = go.Figure()
    df_agg = recent_video_explode.groupby('topic').agg({'duration_second': method, 'views': method}).reset_index()
    
    fig.add_trace(go.Bar(x=df_agg['topic'], y=df_agg['duration_second'], name='duration_second', yaxis='y'))

    fig.add_trace(go.Scatter(x=df_agg['topic'], y=df_agg['views'], mode='lines', name='views', yaxis='y2'))
    # Đặt layout cho biểu đồ
    fig.update_layout(
        title='Biểu đồ số view và thời lượng trung vị theo topic',
        xaxis=dict(title='Topic'),
        yaxis=dict(title='Thời lượng', side='left'),
        yaxis2=dict(title='Số View', side='right', overlaying='y'),
        legend=dict(x=0.2, y= 1)
        )
    return fig



with col2:
    tab1, tab2 = st.tabs(["sum", "median"])
    tab2.plotly_chart(view_duration_topic('median'), theme="streamlit", use_container_width=True)
    tab1.plotly_chart(view_duration_topic('sum'), theme="streamlit", use_container_width=True)




