import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- 2. LOAD & PREPROCESS DATA ---
@st.cache_data
def load_data():
    # Mengambil path direktori tempat file dashboard.py ini berada
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Naik satu folder, lalu masuk ke folder 'data' untuk menemukan 'hour.csv'
    # Ini menjamin path selalu benar di mana pun script ini dieksekusi
    file_path = os.path.join(current_dir, '..', 'data', 'hour.csv')
    
    # Membaca file menggunakan path dinamis
    df = pd.read_csv(file_path)
        
    # Cleaning Data
    df['dteday'] = pd.to_datetime(df['dteday'])
    
    # Feature Engineering (Mapping Label)
    season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    weather_map = {1: 'Clear', 2: 'Mist', 3: 'Light Rain', 4: 'Heavy Rain'}
    df['season_label'] = df['season'].map(season_map)
    df['weather_label'] = df['weathersit'].map(weather_map)
    
    return df

df = load_data()

# --- 3. SIDEBAR INTERAKTIF ---
st.sidebar.title("🚲 Filter Data")
st.sidebar.write("Gunakan filter di bawah ini untuk mengeksplorasi data.")

# Filter rentang tanggal
min_date = df['dteday'].min().date()
max_date = df['dteday'].max().date()

start_date, end_date = st.sidebar.date_input(
    label='Rentang Waktu',
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Mengaplikasikan filter ke dataframe
main_df = df[(df['dteday'].dt.date >= start_date) & (df['dteday'].dt.date <= end_date)]

st.sidebar.markdown("---")
st.sidebar.info("Dashboard ini merangkum analisis data Bike Sharing untuk operasional bisnis.")

# --- 4. KONTEN UTAMA (MAIN LAYOUT) ---
st.title("Bike Sharing Data Analytics Dashboard")
st.markdown("Dashboard ini menyajikan wawasan mengenai pola penyewaan sepeda berdasarkan jam operasional, cuaca, dan musim.")

# Menampilkan metrik utama (Key Performance Indicators)
col1, col2, col3 = st.columns(3)
with col1:
    total_rentals = main_df['cnt'].sum()
    st.metric("Total Penyewaan (Filtered)", value=f"{total_rentals:,}")
with col2:
    avg_rentals = round(main_df['cnt'].mean(), 2)
    st.metric("Rata-rata Penyewaan per Jam", value=f"{avg_rentals}")
with col3:
    max_rentals = main_df['cnt'].max()
    st.metric("Penyewaan Tertinggi dalam 1 Jam", value=f"{max_rentals}")

st.markdown("---")

# --- 5. VISUALISASI BERDASARKAN PERTANYAAN BISNIS ---

# Pertanyaan 1: Pola Jam Sibuk
st.subheader("Jam Berapa Lonjakan Penyewaan Tertinggi Terjadi?")
st.write("Perbandingan pola penyewaan sepeda per jam antara **Hari Kerja** dan **Akhir Pekan/Libur**.")

peak_hours = main_df.groupby(['workingday', 'hr'])['cnt'].mean().reset_index()

fig_1, ax_1 = plt.subplots(figsize=(10, 5))
sns.lineplot(data=peak_hours, x='hr', y='cnt', hue='workingday', marker='o', ax=ax_1, palette="Set1")
ax_1.set_title('Rata-rata Penyewaan Sepeda: Hari Kerja vs Akhir Pekan')
ax_1.set_xlabel('Jam (00–23)')
ax_1.set_ylabel('Rata-rata Penyewaan')
ax_1.set_xticks(range(0, 24))
ax_1.legend(title='Keterangan', labels=['Akhir Pekan/Libur', 'Hari Kerja'])
ax_1.grid(True, linestyle='--', alpha=0.7)
st.pyplot(fig_1)

with st.expander("Lihat Detail Analisis Jam Sibuk"):
    st.write(
        """
        - **Hari Kerja (Working Day):** Lonjakan (*rush hour*) terjadi pada jam keberangkatan kerja (06:00 - 10:00) dengan puncaknya pada jam 08:00, dan jam pulang kerja (16:00 - 20:00) dengan puncaknya pada jam 17:00.
        - **Akhir Pekan/Libur:** Penyewaan lebih merata mulai dari jam 10:00 hingga 16:00, menunjukkan pola penggunaan untuk rekreasi.
        """
    )

st.markdown("---")

# Pertanyaan 2: Pengaruh Cuaca dan Musim
st.subheader("Bagaimana Pengaruh Musim dan Cuaca terhadap Penyewaan?")

weather_season_analysis = main_df.groupby(['season_label', 'weather_label'])['cnt'].mean().reset_index()

fig_2, ax_2 = plt.subplots(figsize=(10, 5))
sns.barplot(data=weather_season_analysis, x='season_label', y='cnt', hue='weather_label', ax=ax_2, palette="viridis")
ax_2.set_title('Rata-rata Penyewaan Sepeda berdasarkan Musim dan Kondisi Cuaca')
ax_2.set_xlabel('Musim')
ax_2.set_ylabel('Rata-rata Jumlah Penyewaan')
ax_2.legend(title='Kondisi Cuaca')
st.pyplot(fig_2)

with st.expander("Lihat Detail Analisis Cuaca & Musim"):
    # Kalkulasi persentase penurunan secara dinamis
    mean_clear = main_df[main_df['weathersit'] == 1]['cnt'].mean()
    mean_rain = main_df[main_df['weathersit'] == 3]['cnt'].mean()
    
    if pd.notna(mean_clear) and pd.notna(mean_rain) and mean_clear > 0:
        penurunan = ((mean_clear - mean_rain) / mean_clear) * 100
        st.write(f"- Penurunan rata-rata penyewaan sepeda dari cuaca **Cerah** ke cuaca **Hujan Ringan** adalah sebesar **{penurunan:.2f}%**.")
    
    st.write(
        """
        - Cuaca cerah selalu menghasilkan rata-rata penyewaan tertinggi di semua musim.
        - Musim Gugur (Fall) mencatatkan tingkat penyewaan tertinggi secara keseluruhan, sementara Musim Semi (Spring) adalah yang terendah.
        """
    )

# --- 6. KESIMPULAN & REKOMENDASI ---
st.markdown("---")
st.subheader("Rekomendasi Bisnis")
st.success(
    """
    1. **Manajemen Armada (*Fleet Management*):** Pastikan ketersediaan sepeda maksimal di stasiun-stasiun strategis pada *rush hour* hari kerja (07:00-09:00 dan 16:00-18:00).
    2. **Pemeliharaan (*Maintenance*):** Jadwalkan *stock opname* dan perbaikan besar armada sepeda pada Musim Semi (Spring) atau saat prediksi cuaca buruk, karena tingkat permintaan sedang berada di titik terendah.
    3. **Promosi Dinamis:** Berikan insentif berupa diskon penyewaan pada saat cuaca mendung atau saat akhir pekan untuk mendongkrak utilitas aset.
    """
)