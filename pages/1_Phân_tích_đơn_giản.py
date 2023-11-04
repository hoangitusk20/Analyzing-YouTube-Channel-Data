import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
import matplotlib.pyplot as plt
import seaborn as sns
from dateutil.parser import parse


st.set_page_config(
    page_title = 'Phân tích dữ liệu đơn giản',
    layout = 'wide',
     initial_sidebar_state = 'expanded'
)

st.markdown(
    """
    <style>
    .title {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)
#Đọc dữ liệu 
try:
	data = pd.read_csv('datasets/data_preprocess.csv')
except:
	data = pd.read_csv('../datasets/data_preprocess.csv')
	
data['user_created'] = data['user_created'].apply(lambda x: parse(x) if x != '--' else None)	
#
def draw_pie_chart(data, values, names, title):
	fig = px.pie(data_frame=data, values=values, names=names)
	
	fig.update_layout(
		title={
		    'text': title,
		    'x': 0.5,  # Giữa trục x
		    'xanchor': 'center',  # Căn giữa theo trục x
		    'yanchor': 'top'  # Căn theo trục y
		},
		showlegend=True
	)
	return fig
	

def draw_bar_chart(data, xvalue, yvalue, orient, title, xlabel, ylabel):

    fig = px.bar(data, y = yvalue, x = xvalue, orientation = orient)
    
    fig.update_layout(
    xaxis_title = xlabel,
    yaxis_title = ylabel,
    title={
        'text': title,
        'x': 0.5,  # Giữa trục x
        'xanchor': 'center',  # Căn giữa theo trục x
        'yanchor': 'top'  # Căn theo trục y
    }
    )
    
    return fig   
    
    
def draw_scatter_plot(data, xvalue, yvalue, title, xlabel, ylabel):

    fig = px.scatter(data, x=xvalue, y=yvalue)
    
    fig.update_layout(
    xaxis_title = xlabel,
    yaxis_title = ylabel,
    title={
        'text': title,
        'x': 0.5,  # Giữa trục x
        'xanchor': 'center',  # Căn giữa theo trục x
        'yanchor': 'top'  # Căn theo trục y
    },
    height=600  # Set the height of the plot to 600 pixels
    )
    
    return fig   
	
def draw_line_chart(xvalue, yvalue, title, xlabel, ylabel):

    fig = px.line(y = yvalue, x = xvalue)
    
    fig.update_layout(
    xaxis_title = xlabel,
    yaxis_title = ylabel,
    title={
        'text': title,
        'x': 0.5,  # Giữa trục x
        'xanchor': 'center',  # Căn giữa theo trục x
        'yanchor': 'top'  # Căn theo trục y
    }
    )
    
    return fig   	


#Tiêu đề
st.markdown('<h1 class="title">Phân tích dữ liệu đơn giản</h1>', unsafe_allow_html=True)

#Dữ liệu của VN
vietnam = data[data['country_name']=='Vietnam']


#################################################

# Câu hỏi 1: Thể loại nào được quan tâm nhất từ YouTube
st.markdown("## Thể loại nào được quan tâm nhất từ YouTube")

##Theo lượt xem
st.markdown("### Theo lượt xem")
### Theo luot xem cua VietNam
df1 = vietnam.groupby('channel_type')['video_views_last_30_days'].sum().sort_values()
df1['other']= df1[:5].sum()
df1 = df1[5:].reset_index()
### Theo luot xem cua the gioi
df2 = data.groupby('channel_type')['video_views_last_30_days'].sum().sort_values()
df2['other']= df2[:5].sum()
df2 = df2[5:].reset_index()

col1, col2 = st.columns([1, 1])
with col1:
    st.plotly_chart(draw_pie_chart(df1,'video_views_last_30_days','channel_type','Tỉ lệ xem theo thể loại gần đây của Việt Nam'), use_container_width=True)

with col2:
    st.plotly_chart(draw_pie_chart(df2,'video_views_last_30_days','channel_type','Tỉ lệ xem theo thể loại gần đây của Thế Giới'), use_container_width=True)

## Theo số lượt uploads
st.markdown("### Theo số lượng video được upload")
### Lượt upload theo thể loại của VN
df1 = vietnam.groupby('channel_type')['uploads'].sum().sort_values()
df1['other']= df1[:5].sum()
df1 = df1[5:].reset_index()
### Lượt upload theo thể loại của TG
df2 = data.groupby('channel_type')['uploads'].sum().sort_values()
df2['other']= df2[:7].sum()
df2 = df2[7:].reset_index()

col1, col2 = st.columns([1, 1])
with col1:
    st.plotly_chart(draw_pie_chart(df1,'uploads','channel_type','Uploads theo thể loại của Việt Nam'), use_container_width=True)

with col2:
    st.plotly_chart(draw_pie_chart(df2,'uploads','channel_type','Uploads theo thể loại của Thế Giới'), use_container_width=True)
    
############################################


# Câu hỏi 2: Phân tích theo quốc gia
st.markdown("## Phân tích theo quốc gia")

## Xếp theo số lượt xem
st.markdown("### Xếp theo số lượt xem")
top20 = data.groupby('country_name')['video_views'].sum().sort_values()[-20:]
top20 = top20.reset_index()
top20_last_30_days = data.groupby('country_name')['video_views_last_30_days'].sum().sort_values()[-20:]
top20_last_30_days = top20_last_30_days.reset_index()
col1, col2 = st.columns([1, 1])
with col1:
    st.plotly_chart(draw_bar_chart(top20, 'video_views','country_name' ,'h', 'Số lượt xem theo từng quốc gia', 'Lượt xem', 'Quốc gia'), use_container_width=True)

with col2:
    st.plotly_chart(draw_bar_chart(top20_last_30_days, 'video_views_last_30_days','country_name' ,'h', 'Số lượt xem theo từng quốc gia trong 30 ngày gần đây', 'Lượt xem', 'Quốc gia'), use_container_width=True)
    
## Xếp theo số lượt đăng ký kênh
st.markdown("### Xếp theo số lượt đăng ký kênh")
top20 = data.groupby('country_name')['subscribers'].sum().sort_values()[-20:]
top20 = top20.reset_index()
top20_last_30_days = data.groupby('country_name')['subscribers_last_30_days'].sum().sort_values()[-20:]
top20_last_30_days = top20_last_30_days.reset_index()
col1, col2 = st.columns([1, 1])
with col1:
    st.plotly_chart(draw_bar_chart(top20, 'subscribers','country_name' ,'h', 'Số subscribers theo từng quốc gia', 'Lượt subscribe', 'Quốc gia'), use_container_width=True)

with col2:
    st.plotly_chart(draw_bar_chart(top20_last_30_days, 'subscribers_last_30_days','country_name' ,'h', 'Số subscribers theo từng quốc gia trong 30 ngày gần đây', 'Lượt subscribe', 'Quốc gia'), use_container_width=True)
    
## Xếp theo thu nhập kiếm được từ YouTube
st.markdown("### Xếp theo thu nhập kiếm được từ YouTube")
top20 = data.groupby('country_name')['estimated_yearly_earnings_max'].sum().sort_values()[-20:]
top20 = top20.reset_index()
st.plotly_chart(draw_bar_chart(top20, 'estimated_yearly_earnings_max','country_name' ,'h', 'Thu nhập từ YouTube theo từng quốc gia trong 1 năm', 'dollars', 'Quốc gia'), use_container_width=True)

############################################


# Câu hỏi 3: Tương quan giữa số người đăng ký và số lượt xem
st.markdown("## Tương quan giữa số người đăng ký và số lượt xem")
col1, col2 = st.columns([1, 1])
with col1:
    st.plotly_chart(draw_scatter_plot(data, 'subscribers','video_views' , 'Tương quan giữa số người đăng ký và lượt xem của kênh', 'Lượt subscribe', 'Lượt xem'), use_container_width=True)

with col2:
    st.plotly_chart(draw_scatter_plot(data, 'subscribers_last_30_days','video_views_last_30_days' , 'Tương quan giữa số người đăng ký và lượt xem của kênh trong 30 ngày gần đây', 'Lượt subscribe', 'Lượt xem'), use_container_width=True)
    
#################################################

# Câu hỏi 4: Số lượng kênh YouTube được tạo theo thời gian
st.markdown("## Số lượng kênh YouTube được tạo theo thời gian")
count_channel = data.groupby('user_created').count()['channel_id'].resample('M').sum()
count_channel=count_channel.reset_index()
st.plotly_chart(draw_line_chart(count_channel.user_created,count_channel.channel_id,'Số lượt kênh được tạo theo thời gian', 'Date', 'Số kênh'), use_container_width=True)



