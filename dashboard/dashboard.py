import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


# Konfigurasi awal 
st.set_page_config(page_title="Dashboard Penyewaan Sepeda", layout="wide")
st.title("Dashboard Analisis Data Penyewaan Sepeda")

# Load dataset 
@st.cache_data
def load_data():
    if os.path.exists("D:/submission/data/day.csv") and os.path.exists("D:/submission/data/hour.csv"):
        day_df = pd.read_csv("D:/submission/data/day.csv")
        hour_df = pd.read_csv("D:/submission/data/hour.csv")
        return day_df, hour_df
    else:
        st.error("Dataset tidak ditemukan. pastikan path-nya benar.")
        return None, None

day_df, hour_df = load_data()

# Sidebar Navigasi 
menu = st.sidebar.radio("Pilihan Halaman Analisis:", [
    "Informasi Dataset",
    "Korelasi cnt dengan Faktor Lingkungan",
    "Korelasi Jam Sibuk dan Pola Harian",
    "Rata-rata Peminjaman per Waktu"
])


# Halaman : Informasi Dataset 
if menu == "Informasi Dataset":
    st.subheader("Informasi Dataset")

    st.write("### Dataset Harian (day.csv)")
    st.dataframe(day_df.head())
    with st.expander("Statistik Deskriptif"):
        st.write(day_df.describe())

    st.write("### Dataset Jam (hour.csv)")
    st.dataframe(hour_df.head())
    with st.expander("Statistik Deskriptif"):
        st.write(hour_df.describe())

    st.write("### Cek Missing Values")
    st.code(day_df.isnull().sum().to_string())
    st.code(hour_df.isnull().sum().to_string())

    st.markdown("> **Insight:** Dataset tidak memiliki missing values, sehingga dapat langsung digunakan untuk analisis. Selain itu, semua kolom juga sudah memiliki tipe data yang sesuai, kecuali kolom tanggal pada dataset day yang perlu dikonversi ke datetime.")


# Halaman : Korelasi cnt dengan Faktor Lingkkungan 
elif menu == "Korelasi cnt dengan Faktor Lingkungan": 
    st.subheader("Korelasi Jumlah Penyewaan (cnt) dengan variabel Lingkungan")

    correlation_matrix = day_df[['cnt', 'temp', 'atemp', 'hum', 'windspeed']].corr()
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('### Heatmap Korelasi')
        fig1, ax1 = plt.subplots(figsize=(5, 4))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax1)
        st.pyplot(fig1)

    with col2:
        st.markdown('### Scatterplot')
        selected_col = st.selectbox("Pilih variabel Lingkungan:", ['temp', 'atemp', 'hum', 'windspeed'])
        fig2, ax2 = plt.subplots(figsize=(5, 4))
        sns.scatterplot(x=selected_col, y='cnt', data=day_df, ax=ax2, alpha=0.6)
        ax2.set_title(f'{selected_col.capitalize()} vs Jumlah Penyewaan')
        st.pyplot(fig2)

    st.markdown("> **Insight**: Suhu berkorelasi positif, kelembaban dan kecepatan angin berkorelasi negatif terhadap jumlah penyewaan sepeda.")


    # Halaman: Korelasi Jam Sibuk dan Pola Harian
elif menu == "Korelasi Jam Sibuk dan Pola Harian":
    st.subheader("Korelasi Pola Jam Sibuk (Peak Hours) dan Weekday vs Weekend")

    peak_hours = hour_df.groupby('hr')['cnt'].sum()
    weekday_usage = hour_df[hour_df['weekday'] < 5].groupby('hr')['cnt'].mean()
    weekend_usage = hour_df[hour_df['weekday'] >= 5].groupby('hr')['cnt'].mean()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(peak_hours.index, peak_hours.values, label='Total', color='gray')
    ax.plot(weekday_usage.index, weekday_usage.values, label='Weekday', color='blue')
    ax.plot(weekend_usage.index, weekend_usage.values, label='Weekend', color='green')
    ax.axvline(8, linestyle='--', color='red', label='Puncak Pagi')
    ax.axvline(18, linestyle='--', color='orange', label='Puncak Sore')
    ax.set_title('Tren Penyewaan Sepeda Per Jam')
    ax.set_xlabel('Jam')
    ax.set_ylabel('Jumlah Penyewaan')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    st.markdown("> **Insight:** Jam sibuk terjadi antara pukul 07:00–09:00 dan 17:00–19:00 pada hari kerja. Redistribusi dan maintenance sebaiknya dilakukan sebelum jam 7 pagi dan setelah jam 7 malam.")


elif menu == "Rata-rata Peminjaman per Waktu":
    st.subheader("⏰ Rata-rata Peminjaman Sepeda per Waktu dalam Sehari")

    def label_time(hr):
        if 5 <= hr < 12:
            return 'Morning'
        elif 12 <= hr < 17:
            return 'Afternoon'
        elif 17 <= hr < 21:
            return 'Evening'
        else:
            return 'Night'

    hour_df['time_of_day'] = hour_df['hr'].apply(label_time)
    grouped_time = hour_df.groupby('time_of_day')['cnt'].mean().reindex(['Morning', 'Afternoon', 'Evening', 'Night'])

    col = st.container()
    with col:
        fig, ax = plt.subplots(figsize=(5, 3.5))
        plot_df = pd.DataFrame({
            'time_of_day': grouped_time.index,
            'avg_cnt': grouped_time.values
        })
        sns.barplot(data=plot_df, x='time_of_day', y='avg_cnt', hue='time_of_day', palette='viridis', legend=False, ax=ax)
        ax.set_title('Rata-rata Peminjaman Sepeda per Waktu')
        ax.set_xlabel('Waktu')
        ax.set_ylabel('Rata-rata Peminjaman')
        ax.grid(True, axis='y')
        st.pyplot(fig)

        st.markdown("### Insight:")
        st.markdown("> **Evening** menunjukkan rata-rata peminjaman tertinggi.")
