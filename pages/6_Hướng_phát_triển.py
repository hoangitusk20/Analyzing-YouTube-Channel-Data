import streamlit as st


st.set_page_config(
    page_title="Hướng phát triển",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Hướng phát triển")

st.subheader("❗Vấn đề gặp phải")

st.markdown(
    """
    **Cào dữ liệu**: 
    Vì cào hơn 20000 dòng nên gặp tình trạng bị chặn IP và không cho cào tiếp.

    **Mô hình dự đoán**:
    Sử dụng Linear Regression và các mô hình hồi quy tương tự thì độ chính xác không cao. Có thể do dữ liệu cào về chưa đủ nhiều, hoặc mô hình không phù hợp.
    """
)

st.subheader("💡Hướng giải quyết của nhóm")

st.markdown(
    """
    **Cào dữ liệu**:
    Cào 1000 dòng, nghỉ 10 phút sau đó lại cào tiếp. Cách này đã giúp nhóm cào được dữ liệu từ trang Social Blade về nhưng tốn thêm thời gian chờ.
    
    **Mô hình dự đoán**:
    Thêm một số thuộc tính mới được tính toán dựa trên các thuộc tính có sẵn. Điều này giúp tăng độ chính xác của mô hình qua kết quả thực nghiệm. 
    """
)

st.subheader("📝Hướng phát triển trong tương lai")

st.markdown(
    """
    - Thuê dịch vụ proxy để thay đổi địa chỉ ip. Dịch vụ sẽ cung cấp proxy gồm ip, port, username, password. Khi cào dữ liệu, thêm proxy được cung cấp vào, sau đó thực hiện cào dữ liệu. Proxy sẽ được thay đổi liên tục tự động bởi dịch vụ, nên sẽ tránh được việc bị chặn IP.
    - Cào hết 3 cái top 100 (sort theo Social Blade, Subscribers, Video views) của mỗi quốc gia để có nhiều dữ liệu hơn để phân tích.
    - Cào thêm dữ liệu từ google API để có nhiều thông tin hơn.
    - Cào và trực quan dữ liệu theo thời gian thực.
    - Thử các mô hình khác để dự đoán với độ chính xác cao hơn.
    - Sử dụng các thuật toán phân cụm để phân cụm các kênh youtube.
    """
)
