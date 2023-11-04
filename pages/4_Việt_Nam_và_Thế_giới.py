import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from scipy import stats

st.set_page_config(
    page_title='So sánh',
    layout='wide'
)

# Read data from csv
df = pd.read_csv('datasets/data_preprocess.csv', index_col=0)

# Side bar
country_list = np.sort(df[df["country_name"] != "Vietnam"]
                       ['country_name'].unique())[1:].tolist()
country_list.insert(0, "Thế Giới")
with st.sidebar:
    st.sidebar.subheader('Quốc gia')
    country_filter = st.selectbox(label='Chọn quốc gia', options=country_list,
                                  index=0)

# Title
st.markdown(f'<h1 style="text-align: center;">So sánh các thông số của Việt Nam với {country_filter}</h1>',
            unsafe_allow_html=True)

compare_df = df if country_filter == 'Thế Giới' else df[df["country_name"]
                                                        == country_filter]
compare_df['x'] = country_filter
vietnam_df = df[df["country_name"] == "Vietnam"]
vietnam_df['x'] = 'Việt Nam'
df_merged = vietnam_df.append(compare_df, ignore_index=True)

vietnam_stat = df[df["country_name"] == "Vietnam"].agg(
    {'uploads': 'mean',
     'subscribers': 'mean',
     'video_views': 'mean',
     'subscribers_last_30_days': 'mean',
     'video_views_last_30_days': 'mean',
     'estimated_monthly_earnings_min': 'mean',
     'estimated_monthly_earnings_max': 'mean',
     'estimated_yearly_earnings_min': 'mean',
     'estimated_yearly_earnings_max': 'mean',
     'social_blade_rank': 'mean',
     'subscriber_rank': 'mean',
     'video_views_rank': 'mean',
     'channel_type_rank': 'mean', })
compare_stat = compare_df.agg(
    {'uploads': 'mean',
     'subscribers': 'mean',
     'video_views': 'mean',
     'subscribers_last_30_days': 'mean',
     'video_views_last_30_days': 'mean',
     'estimated_monthly_earnings_min': 'mean',
     'estimated_monthly_earnings_max': 'mean',
     'estimated_yearly_earnings_min': 'mean',
     'estimated_yearly_earnings_max': 'mean',
     'social_blade_rank': 'mean',
     'subscriber_rank': 'mean',
     'video_views_rank': 'mean',
     'channel_type_rank': 'mean', })

most_channel_type_vn = df[(df["country_name"] == "Vietnam") &
                          (df['channel_type'] != 'Unknown')]['channel_type'].mode()
most_channel_type_compare = compare_df[df['channel_type']
                                       != 'Unknown']['channel_type'].mode()

most_grade_vn = df[(df["country_name"] == "Vietnam") &
                   (df['total_grade'] != 'Unknown')]['total_grade'].mode()
most_grade_compare = compare_df[df['total_grade']
                                != 'Unknown']['total_grade'].mode()


col1, col2 = st.columns(2)
with col1:
    # Subscribers
    fig = px.box(df_merged,
                 y='subscribers',
                 x='x')
    fig.update_layout(title="Lượt đăng ký", width=400)
    st.plotly_chart(fig)

    # Uploaded videos
    fig = px.box(df_merged,
                 y='uploads',
                 x='x')
    fig.update_layout(title="Số video đã đăng", width=400)
    st.plotly_chart(fig)

    # Subscribers last 30 days
    fig = px.box(df_merged,
                 y='subscribers_last_30_days',
                 x='x')
    fig.update_layout(
        title="Lượt đăng ký 30 ngày gần đây", width=400)
    st.plotly_chart(fig)

with col2:
    # Video views
    fig = px.box(df_merged,
                 y='video_views',
                 x='x')
    fig.update_layout(title="Lượt xem", width=400)
    st.plotly_chart(fig)

    # Monthly earnings
    fig = px.box(df_merged,
                 y=['estimated_monthly_earnings_min',
                     'estimated_monthly_earnings_max'],
                 x='x')

    fig.update_layout(title="Ước tính thu nhập hàng tháng",
                      width=400)
    st.plotly_chart(fig)

    # Video views last 30 days
    fig = px.box(df_merged,
                 y='video_views_last_30_days',
                 x='x')
    fig.update_layout(title="Lượt xem 30 ngày gần đây", width=400)
    st.plotly_chart(fig)


def mean_stand(df, col):
    temp = np.array(df[col].values.tolist())
    return temp.mean(), temp.std(), len(temp)


def z(df1, df2, col):
    mean1, std1, n1 = mean_stand(df1, col)
    mean2, std2, n2 = mean_stand(df2, col)
    # Tính sai số chuẩn (standard error)
    se = np.sqrt((std1**2 / n1) + (std2**2 / n2))
    # Tính giá trị z-score
    z_score = (mean1 - mean2) / se
    # Tính giá trị p-value (cho kiểm định z)
    p_value_z = 1 - stats.norm.cdf(z_score)
    # Ngưỡng ý nghĩa
    alpha = 0.05
    # Kết luận
    if p_value_z < alpha:
        return True
    else:
        return False


def compare_earning(monthly=False, yearly=False):
    if monthly:
        if z(vietnam_df, compare_df, 'estimated_monthly_earnings_min') and z(vietnam_df, compare_df, 'estimated_monthly_earnings_max'):
            return f'Việt Nam > {country_filter}'
        elif z(compare_df, vietnam_df, 'estimated_monthly_earnings_min') and z(compare_df, vietnam_df, 'estimated_monthly_earnings_max'):
            return f'Việt Nam < {country_filter}'

    if yearly:
        if z(vietnam_df, compare_df, 'estimated_yearly_earnings_min') and z(vietnam_df, compare_df, 'estimated_yearly_earnings_max'):
            return f'Việt Nam > {country_filter}'
        elif z(compare_df, vietnam_df, 'estimated_yearly_earnings_min') and z(compare_df, vietnam_df, 'estimated_yearly_earnings_max'):
            return f'Việt Nam < {country_filter}'

    return "--"


# Stat table
st.subheader('Bảng so sánh thông số')
st.markdown(f"""|| Việt Nam | {country_filter} | Kết luận |
|-|:---:|:---:|:---:|
|Loại kênh phổ biến nhất|{most_channel_type_vn[0]}|{most_channel_type_compare[0]}|--|
|Đánh giá phổ biến nhất|{most_grade_vn[0]}|{most_grade_compare[0]}|--|
|Lượt đăng ký trung bình|{'{:,.0f}'.format(vietnam_stat['subscribers'])}|{'{:,.0f}'.format(compare_stat['subscribers'])}|{f'Việt Nam > {country_filter}' if z(vietnam_df, compare_df, 'subscribers') else f'Việt Nam < {country_filter}' if z(compare_df, vietnam_df, 'subscribers') else '--' }|
|Lượt xem trung bình|{'{:,.0f}'.format(vietnam_stat['video_views'])}|{'{:,.0f}'.format(compare_stat['video_views'])}|{f'Việt Nam > {country_filter}' if z(vietnam_df, compare_df, 'video_views') else f'Việt Nam < {country_filter}' if z(compare_df, vietnam_df, 'video_views') else '--' }|
|Số video trung bình|{'{:,.0f}'.format(vietnam_stat['uploads'])}|{'{:,.0f}'.format(compare_stat['uploads'])}|{f'Việt Nam > {country_filter}' if z(vietnam_df, compare_df, 'uploads') else f'Việt Nam < {country_filter}' if z(compare_df, vietnam_df, 'uploads') else '--' }|
|Lượt xem trung bình 30 ngày gần đây|{'{:,.0f}'.format(vietnam_stat['video_views_last_30_days'])}|{'{:,.0f}'.format(compare_stat['video_views_last_30_days'])}|{f'Việt Nam > {country_filter}' if z(vietnam_df, compare_df, 'video_views_last_30_days') else f'Việt Nam < {country_filter}' if z(compare_df, vietnam_df, 'video_views_last_30_days') else '--' }|
|Lượt đăng ký trung bình 30 ngày gần đây|{'{:,.0f}'.format(vietnam_stat['subscribers_last_30_days'])}|{'{:,.0f}'.format(compare_stat['subscribers_last_30_days'])}|{f'Việt Nam > {country_filter}' if z(vietnam_df, compare_df, 'subscribers_last_30_days') else f'Việt Nam < {country_filter}' if z(compare_df, vietnam_df, 'subscribers_last_30_days') else '--' }|
|Ước tính thu nhập hàng tháng trung bình|\${'{:,.0f}'.format(vietnam_stat['estimated_monthly_earnings_min'])} - \${'{:,.0f}'.format(vietnam_stat['estimated_monthly_earnings_max'])}|\${'{:,.0f}'.format(compare_stat['estimated_monthly_earnings_min'])} - \${'{:,.0f}'.format(compare_stat['estimated_monthly_earnings_max'])}|{compare_earning(monthly=True)}|
|Ước tính thu nhập hàng năm trung bình|\${'{:,.0f}'.format(vietnam_stat['estimated_yearly_earnings_min'])} - \${'{:,.0f}'.format(vietnam_stat['estimated_yearly_earnings_max'])}|\${'{:,.0f}'.format(compare_stat['estimated_yearly_earnings_min'])} - \${'{:,.0f}'.format(compare_stat['estimated_yearly_earnings_max'])}|{compare_earning(yearly=True)}|
|Xếp hạng theo social blade trung bình|{'{:,.0f}'.format(vietnam_stat['social_blade_rank'])}|{'{:,.0f}'.format(compare_stat['social_blade_rank'])}|{f'Việt Nam < {country_filter}' if z(vietnam_df, compare_df, 'social_blade_rank') else f'Việt Nam > {country_filter}' if z(compare_df, vietnam_df, 'social_blade_rank') else '--' }|
|Xếp hạng theo lượt đăng ký trung bình|{'{:,.0f}'.format(vietnam_stat['subscriber_rank'])}|{'{:,.0f}'.format(compare_stat['subscriber_rank'])}|{f'Việt Nam < {country_filter}' if z(vietnam_df, compare_df, 'subscriber_rank') else f'Việt Nam > {country_filter}' if z(compare_df, vietnam_df, 'subscriber_rank') else '--' }|
|Xếp hạng theo lượt xem trung bình|{'{:,.0f}'.format(vietnam_stat['video_views_rank'])}|{'{:,.0f}'.format(compare_stat['video_views_rank'])}|{f'Việt Nam < {country_filter}' if z(vietnam_df, compare_df, 'video_views_rank') else f'Việt Nam > {country_filter}' if z(compare_df, vietnam_df, 'video_views_rank') else '--' }|
|Xếp hạng theo loại kênh trung bình|{'{:,.0f}'.format(vietnam_stat['channel_type_rank'])}|{'{:,.0f}'.format(compare_stat['channel_type_rank'])}|{f'Việt Nam < {country_filter}' if z(vietnam_df, compare_df, 'channel_type_rank') else f'Việt Nam > {country_filter}' if z(compare_df, vietnam_df, 'channel_type_rank') else '--' }|
""")
st.write("""
<style>
[data-testid="stMarkdownContainer"] tbody tr:nth-child(2n) {
    background-color: rgba(255, 255,255, 0.1);
}

</style>
""", unsafe_allow_html=True)
