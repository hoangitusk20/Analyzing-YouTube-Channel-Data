import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime
import webcolors

st.set_page_config(page_title="Thông tin channel", layout='wide',
                   initial_sidebar_state='expanded')


# Read data from csv
data = pd.read_csv('datasets/data_preprocess.csv', index_col=0)

# Change type
data['user_created'] = pd.to_datetime(data['user_created']).dt.date

all_colors = webcolors.CSS3_NAMES_TO_HEX
list_color = list(all_colors.keys())

# Side bar
with st.sidebar:
    st.sidebar.subheader('Quốc gia')
    country_filter = st.selectbox(label='Chọn quốc gia', options=np.sort(
        data['country_name'].unique())[1:].tolist())

    st.sidebar.subheader('Kênh')
    channel_filter = st.selectbox(label='Chọn kênh', options=np.sort(
        data[data['country_name'] == country_filter]['channel_name'].unique())[1:].tolist())

    temp = data[(data['channel_name'] == channel_filter) &
                (data['country_name'] == country_filter)]

    color_hex = st.color_picker('Chọn màu khung', '#4169e1')
    text1_color = st.color_picker('Chọn màu chữ 1', '#ffffff')
    text2_color = st.color_picker('Chọn màu chữ 1', '#000000')


# Title

st.markdown(
    f'<h1 style="text-align: center;">TỔNG QUAN KÊNH <br>{channel_filter}</h1>', unsafe_allow_html=True)


def markdown(title, description, bottom=False):
    if bottom:
        bottom_css = f'border-bottom: 6px solid {color_hex}; box-shadow: 0 6px 0 {color_hex};'
    else:
        bottom_css = ''
    st.markdown(f'<div style="{bottom_css}border: 3px solid {color_hex}; padding: 10px;">'
                f'<h5 style="text-align: center; font-weight: normal; margin: 1px; line-height: 1; color: {text2_color};">{title}</h5>'
                f'<h3 style="text-align: center; margin: 1px; line-height: 0.5; color: {text2_color};">{description}</h3>'
                '</div>', unsafe_allow_html=True)


# Row 1
col = st.columns([0.5, 1, 1, 1])

columns = ['total_grade', 'channel_type', 'country_name', 'user_created']

with col[0]:
    st.markdown(f'<div style="border-bottom: 7px solid {color_hex}; box-shadow: 0 7px 0 {color_hex}; border: 3px solid {color_hex}; padding: 10px; background-color: {color_hex}; text-align: center;">'
                f'<h5 style="font-weight: normal; margin: 0; line-height: 0.5; color: {text1_color};">Xếp loại</h5>'
                f'<h1 style="margin: 0; line-height: 0.3; color: {text1_color};">{temp[columns[0]].values[0].replace(" ", "")}</h3>'
                '</div>', unsafe_allow_html=True)


with col[1]:
    markdown('Thể loại', temp[columns[1]].values[0].replace(" ", ""), True)

with col[2]:
    markdown('Quốc gia', temp[columns[2]].values[0].replace(" ", ""), True)

with col[3]:
    markdown('Ngày tạo', temp[columns[3]].values[0], True)

st.write('')

# Row 2
col = st.columns([1, 1, 1, 1, 1])

columns = ['social_blade_rank', 'country_rank',
           'subscriber_rank', 'video_views_rank', 'channel_type_rank']

for i in range(len(columns)):
    with col[i]:
        try:
            num = '{:,.0f}ᵗʰ'.format(int(temp[columns[i]].values))
        except:
            num = '--'
        markdown(columns[i].replace('_', ' ').capitalize(), num)

st.write('')

# Row 3
col = st.columns([1, 1, 1])
columns = ['subscribers', 'uploads', 'video_views']


with col[0]:
    markdown('Tổng số subscribers', '{:,.0f}'.format(
        int(temp[columns[0]].values)))

with col[1]:
    markdown('Tổng số videos', '{:,.0f}'.format(int(temp[columns[1]].values)))

with col[2]:
    markdown('Tổng số views', '{:,.0f}'.format(int(temp[columns[2]].values)))


col = st.columns([1, 1, 1])
columns = ['subscribers_last_30_days',
           'estimated_monthly_earnings', 'video_views_last_30_days']


with col[0]:
    markdown('Lượng subcribers mới trong 30 ngày',
             '{:,.0f}'.format(int(temp[columns[0]].values)))

with col[1]:
    markdown('Ước tính thu nhập tháng này', str(
        temp[columns[1]].values[0].replace(' ', '')))

with col[2]:
    markdown('Lượng views trong 30 ngày',
             '{:,.0f}'.format(int(temp[columns[2]].values)))
