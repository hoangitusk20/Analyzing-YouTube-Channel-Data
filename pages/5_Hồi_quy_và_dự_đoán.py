import json
import pickle
import re
from traceback import print_exc
import numpy as np
import pandas as pd
import streamlit as st

from crawl_data import social_blade_crawler

st.set_page_config(
    page_title="Hồi quy và dự đoán",
    layout="wide",
    initial_sidebar_state="expanded",
)

model = pickle.load(open("models/gradient_boosting.pkl", "rb"))
df = pd.read_csv("datasets/data_regression.csv")
y_col = 'video_views'

st.title("Hồi quy và dự đoán")

st.header("Hồi quy")
st.markdown(
    """
    Sử dụng Gradient Boosting Regressor của thư viện Scikit-learn để thực hiện hồi quy trên tập dữ liệu.
    """
)
st.text(f"Gradient boosting score: {model.score(df.drop(y_col, axis=1), df[y_col])}.")

st.header("Dự đoán")
channel_id = st.text_input("Nhập id/username kênh:")
channel_id = channel_id.strip()

if channel_id:
    try:
        data = social_blade_crawler.get_channel_data(channel_id)
        filtered_data = {}
        for col in [*df.columns, 'user_created']:
            if col in data:
                filtered_data[col] = data[col]
            else:
                filtered_data[col] = np.nan

        new_df = pd.DataFrame([filtered_data])

        new_df['percentage_subscribed_last_30_days'] = new_df['subscribers_last_30_days'] / new_df['subscribers']
        new_df['percentage_video_views_last_30_days'] = new_df['video_views_last_30_days'] / new_df['video_views']
        new_df['average_views_per_video'] = new_df['video_views'] / new_df['uploads']
        new_df['average_views_per_subscriber'] = new_df['video_views'] / new_df['subscribers']
        new_df['user_created_dt'] = pd.to_datetime(new_df['user_created'].map(lambda d: re.sub(r'((st)|(nd)|(rd)|(th)),', '', d or '')), format='%b %d %Y', errors='coerce')
        new_df['channel_age'] = (pd.to_datetime('today') - new_df['user_created_dt']).dt.days
        new_df['average_views_per_day'] = new_df['video_views'] / new_df['channel_age']

        new_df.drop(columns=['user_created', 'user_created_dt'], inplace=True)
        st.table(new_df)

        y_pred = model.predict(new_df.drop(y_col, axis=1))
        diff = abs(y_pred[0] - data[y_col])
        st.text(f"Dự đoán lượt xem video: {y_pred[0]:.0f}\n"
                f"Lượt xem video thực tế: {data[y_col]}\n"
                f"Chênh lệch: {diff:.0f} - {diff / data[y_col] * 100:.2f}%")
    except:
        print_exc()
        st.error("Không tìm thấy kênh hoặc dữ liệu thiếu.")
