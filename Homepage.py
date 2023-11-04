import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(
    page_title = 'Giới thiệu',
    layout = 'wide',

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

with st.sidebar:
    st.sidebar.subheader('Biểu đồ phân bố dữ liệu số')
    list_chart = ['box plot', 'violin plot', 'histogram']
    chart_filter = st.selectbox(label = 'Chọn biểu đồ', options = list_chart)
    if chart_filter == 'histogram':
        num_bins = st.slider('Chọn số lượng bin', 1, 20, 10)
        height = st.slider('Điều chỉnh độ cao', 250, 400, 250)

st.markdown('<h1 class="title">Đồ án cuối kì môn Trực quan hóa dữ liệu</h1>', unsafe_allow_html=True)
st.markdown('<h1 class="title">Phân tích dữ liệu youtube</h1>', unsafe_allow_html=True)

# st.title("Seminar môn Trực quan hóa dữ liệu - Phân tích dữ liệu youtube")

data = pd.read_csv('datasets/data_preprocess.csv', index_col=0)

st.markdown("## Thông tin về bộ dữ liệu")
st.markdown("- **Nguồn:** crawl từ trang [socialblade](https://socialblade.com/youtube/) bằng `beautifulsoup` và `selenium`")
st.markdown(f"- Bộ dữ liệu cung cấp thông tin chi tiết về các kênh youtube trên thế giới.")
st.markdown(f"- Sau khi thực hiện tiền xử lý, bộ dữ liệu cuối cùng có kích thước `{data.shape[0]} dòng` và `{data.shape[1]} cột`.")
meaning = pd.read_csv(r"datasets/columns_meaning.csv", index_col = 0)
st.dataframe(meaning, use_container_width = True)

st.markdown("## Phân bố dữ liệu dạng số")

st.markdown("### Mô tả về dữ liệu")
describe = data.select_dtypes(include=['number']).describe().round(1)
st.dataframe(describe, use_container_width = True)


st.markdown("### Biểu đồ phân bố của dữ liệu dạng số.")

num_col = data._get_numeric_data().columns
if chart_filter in ['box plot', 'violin plot']:
    count = 0
    for i in range(4):
        col = st.columns([1, 1, 1, 1])
        for j in range(4):
            try:
                if chart_filter == 'box plot':
                    fig = px.box(data, y = num_col[count])
                elif chart_filter == 'violin plot':
                    fig = px.violin(data, y = num_col[count])
                elif chart_filter == 'histogram':
                    fig = px.histogram(data[num_col[count]], nbins = num_bins)
                    fig.update_layout(height = height)
                count += 1
                with col[j]:
                    st.plotly_chart(fig, use_container_width = True)
            except:
                break
else:
    count = 0
    for i in range(8):
        col = st.columns([1, 1])
        for j in range(2):
            try:
                if chart_filter == 'histogram':
                    fig = px.histogram(data[num_col[count]], nbins = num_bins)
                    fig.update_layout(height = height, xaxis_title = num_col[count], showlegend = False)
                count += 1
                with col[j]:
                    st.plotly_chart(fig, use_container_width = True)
            except:
                break

st.markdown("## Phân bố dữ liệu dạng phân loại")

st.markdown("### Mô tả dữ liệu dạng phân loại")
describe= data[['channel_type', 'total_grade', 'country_name']].describe()
st.dataframe(describe, use_container_width = True)

cate_col = ['channel_type', 'total_grade']
col1, col2 = st.columns([1, 1])

def draw(data, col, orient, title, xlabel, ylabel):
    counts = data[col].value_counts().reset_index()
    counts.columns = [col, 'Count']
    fig = px.bar(counts, y = col, x = 'Count', orientation = orient)
    
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

with col1:
    st.plotly_chart(draw(data, 'channel_type', 'h', 'Phân bố của thể loại kênh', 'số lượng', 'thể loại'), use_container_width=True)

with col2:
    st.plotly_chart(draw(data, 'total_grade', 'h', 'Phân bố của xếp loại kênh', 'số lượng', 'xếp loại'), use_container_width=True)
    
 
def draw_heatmap(data, title):

   fig = px.imshow(data,text_auto=True)
    
   fig.update_layout(
   title={
        'text': title,
        'x': 0.5,  # Giữa trục x
        'xanchor': 'center',  # Căn giữa theo trục x
        'yanchor': 'top'  # Căn theo trục y
        
    },
   height=800,  # Set the height
   width=800   # Set the width
   )
    
   return fig   
    
st.markdown("## Phân tích độ tương quan giữa các biến")
corrmat = data.corr()
st.plotly_chart(draw_heatmap(corrmat.round(2),'Độ tương quan giữa các biến'),use_container_width=True)

