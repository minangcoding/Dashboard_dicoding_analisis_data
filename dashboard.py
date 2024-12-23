

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date
import os
import numpy as np

# Memastikan kompatibilitas seaborn dengan pandas terbaru
sns.set_theme()

# Membaca data
day_df = pd.read_csv("day.csv")
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Sidebar untuk memilih rentang tanggal
st.sidebar.header("Select Date Range")
min_date = day_df['dteday'].min().date()
max_date = day_df['dteday'].max().date()
default_start_date = min_date
default_end_date = max_date

start_date = st.sidebar.date_input("Start Date", value=default_start_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Date", value=default_end_date, min_value=min_date, max_value=max_date)

# Filter data berdasarkan rentang tanggal
filtered_df = day_df[(day_df['dteday'].dt.date >= start_date) & (day_df['dteday'].dt.date <= end_date)]

# Visualisasi 1: Jumlah penyewa sepeda berdasarkan musim
season_pattern = filtered_df.groupby(by="season")[["registered", "casual"]].sum().reset_index()
fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.bar(season_pattern["season"], season_pattern["registered"], label="Registered", color="blue")
ax1.bar(season_pattern["season"], season_pattern["casual"], bottom=season_pattern["registered"], label="Casual", color="red")
ax1.set_xlabel("Season")
ax1.set_ylabel("Number of Users")
ax1.set_title("Jumlah Penyewa Sepeda Berdasarkan Musim")
ax1.legend()

# Visualisasi 2: Perbandingan penyewa sepeda setiap hari
filtered_df["weekday"] = filtered_df["weekday"].map({0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'})
filtered_df["weekday"] = filtered_df["weekday"].astype("category")
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(
    x="weekday",
    y="cnt",
    data=filtered_df,
    order=["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
    palette="viridis",
    ax=ax2
)
ax2.set_title('Perbandingan Penyewa Sepeda Setiap Hari')
ax2.set_xlabel("Hari")
ax2.set_ylabel('Jumlah Pengguna Sepeda')
ax2.grid(True)

# Tampilkan visualisasi di aplikasi Streamlit
st.title("Dashboard Analisis Penyewa Sepeda")
st.write("Visualisasi data penyewa sepeda berdasarkan data historis.")

st.write("\n")
st.subheader("Jumlah Penyewa Sepeda Berdasarkan Musim")
st.write("Grafik di bawah ini menunjukkan jumlah penyewa sepeda berdasarkan musim untuk tipe pengguna terdaftar dan tidak terdaftar.")
st.pyplot(fig1, use_container_width=True)

st.write("\n")
st.subheader("Perbandingan Penyewa Sepeda Setiap Hari")
st.write("Grafik di bawah ini menunjukkan perbandingan jumlah penyewa sepeda setiap hari dalam seminggu.")
st.pyplot(fig2, use_container_width=True)
