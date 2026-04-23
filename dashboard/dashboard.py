import pandas as pd
import streamlit as st

st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

@st.cache_data
def load_data():
    day_df = pd.read_csv("final_cleaned_day.csv")
    hour_df = pd.read_csv("final_cleaned_hour.csv")
    
    day_df["dteday"] = pd.to_datetime(day_df["dteday"], format='%d-%m-%Y')
    hour_df["dteday"] = pd.to_datetime(hour_df["dteday"], format='%d-%m-%Y')
    return day_df, hour_df

day_df, hour_df = load_data()

with st.sidebar:
    st.header("🚲 Filter Data")
    st.write("Pilih rentang tanggal untuk melihat perubahan pola penyewaan sepeda.")

    min_date = day_df["dteday"].min()
    max_date = day_df["dteday"].max()

    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

filtered_day = day_df[(day_df["dteday"] >= pd.to_datetime(start_date)) & (day_df["dteday"] <= pd.to_datetime(end_date))]
filtered_hour = hour_df[(hour_df["dteday"] >= pd.to_datetime(start_date)) & (hour_df["dteday"] <= pd.to_datetime(end_date))]

st.title("🚲 Bike Sharing Dashboard")
st.markdown("Dashboard ini menampilkan gambaran penggunaan sepeda berdasarkan waktu, jenis pengguna, dan kondisi lingkungan.")

col1, col2, col3 = st.columns(3)
with col1:
    total_rentals = filtered_day['cnt'].sum()
    st.metric("Total Peminjaman", value=f"{total_rentals:,}")
with col2:
    total_registered = filtered_day['registered'].sum()
    st.metric("Registered", value=f"{total_registered:,}")
with col3:
    total_casual = filtered_day['casual'].sum()
    st.metric("Casual", value=f"{total_casual:,}")

st.divider()

tab1, tab2, tab3 = st.tabs(["📊 Harian", "⏰ Jam Sibuk", "🌤️ Cuaca & Musim"])

with tab1:
    st.subheader("Tren Penyewaan Harian")
    daily_trend = filtered_day.set_index("dteday")["cnt"]
    st.line_chart(daily_trend)

    st.markdown("### Perbandingan Penggunaan")
    col_tab1_left, col_tab1_right = st.columns(2)
    
    with col_tab1_left:
        st.markdown("**Hari Kerja vs Libur**")
        avg_day = filtered_day.groupby("day_type")["cnt"].mean()
        st.bar_chart(avg_day)
        
    with col_tab1_right:
        st.markdown("**Tipe Pengguna**")
        user_types = pd.DataFrame({
            "Jumlah": [filtered_day['casual'].sum(), filtered_day['registered'].sum()]
        }, index=["Casual", "Registered"])
        st.bar_chart(user_types)

    with st.expander("Lihat insight"):
        st.write(
            "Penggunaan sepeda cenderung lebih tinggi di hari kerja. "
            "Selain itu, pengguna registered jauh lebih dominan dibandingkan casual, "
            "yang menunjukkan sepeda banyak digunakan untuk aktivitas rutin seperti bekerja atau sekolah."
        )


with tab2:
    st.subheader("Pola Penggunaan per Jam")
    hourly_trend = filtered_hour.groupby(["hr", "day_type"])["cnt"].mean().unstack()
    
    st.line_chart(hourly_trend)

    with st.expander("Lihat insight"):
        st.write(
            "Di hari kerja terlihat dua lonjakan utama, yaitu pagi sekitar jam 08.00 "
            "dan sore sekitar jam 17.00. Pola ini tidak terlalu terlihat di akhir pekan, "
            "karena penggunaan lebih menyebar dan cenderung tinggi di siang hari."
        )
        st.write(
            "Waktu di luar jam sibuk bisa dimanfaatkan untuk perawatan sepeda "
            "agar tidak mengganggu pengguna."
        )


with tab3:
    st.subheader("Pengaruh Cuaca dan Musim")
    
    col_tab3_left, col_tab3_right = st.columns(2)
    
    with col_tab3_left:
        st.markdown("**Berdasarkan Musim**")
        avg_season = filtered_day.groupby("season")["cnt"].mean()
        st.bar_chart(avg_season)
        
    with col_tab3_right:
        st.markdown("**Berdasarkan Cuaca**")
        avg_weather = filtered_day.groupby("weathersit")["cnt"].mean()
        st.bar_chart(avg_weather)

    with st.expander("Lihat insight"):
        st.write(
            "Jumlah penyewaan meningkat saat musim dengan cuaca yang lebih nyaman, "
            "seperti summer dan fall. Sebaliknya, saat cuaca buruk, jumlah penyewaan menurun cukup signifikan."
        )
        st.write(
            "Kondisi ini menunjukkan bahwa cuaca menjadi salah satu faktor penting "
            "yang memengaruhi minat pengguna."
        )

st.caption("Bike Sharing Dashboard - 2026")