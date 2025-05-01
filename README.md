# Dashboard Analisis Penyewaan Sepeda

Dashboard ini dibuat menggunakan **Streamlit** untuk menganalisis data penyewaan sepeda berdasarkan dataset `day.csv` dan `hour.csv`.

## Struktur Folder
```
submission/
├── dashboard/
    ├── dashboard.py
    └── main_data.csv
└── data/
    ├── day.csv
    └── hour.csv
├── Proyek_Analisis_Data (1).ipynb
├── README.md
├── requirements.txt
├── url.txt

```

## Cara Menjalankan

1. Clone repository ini atau unduh semua file.
2. Pastikan Python 3.7+ telah terinstall.
3. Install semua dependensi:
   ```bash
   pip install -r requirements.txt
   ```
4. Jalankan aplikasi:
   ```bash
   streamlit run dashboard.py
   ```

## Sumber Data

Dataset diambil dari [Bike Sharing Dataset](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset) yang terdiri dari:
- `day.csv` — data penyewaan harian
- `hour.csv` — data penyewaan per jam

## Fitur Dashboard

- Melihat data dan informasi statistik dasar
- Visualisasi korelasi antara cuaca dan jumlah penyewaan sepeda
- Analisis pola jam sibuk antara weekday dan weekend
- Rata-rata penyewaan sepeda berdasarkan waktu (pagi, siang, sore, malam)