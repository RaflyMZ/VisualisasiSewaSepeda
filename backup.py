import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Menambahkan judul di navbar
st.set_page_config(layout="wide")

# Membuat sidebar
st.title('Dashboard Visualisasi Data Penyewaan Sepeda')
menu = ["day", "hour"]
selected_page = st.sidebar.selectbox("Pilih Halaman", menu)

# Import data
df = pd.read_csv('day.csv')

# Mengelompokkan data berdasarkan bulan dan menghitung total penyewaan
df_groupby_month = df.groupby('mnth')['cnt'].sum()

# Menampilkan visualisasi berdasarkan pilihan di sidebar

# Analisis Sewa Harian
if selected_page == "day":

    st.header('Analisis Data Sewa Harian')

    # Mengubah kolom dteday menjadi datetime
    df['dteday'] = pd.to_datetime(df['dteday'])

    # Membuat sidebar
    st.sidebar.header('Filter Data')
    # Memilih data tahun
    tahun_pilihan = st.sidebar.selectbox('Pilih Tahun', df['dteday'].dt.year.unique())

    # Memfilter data berdasarkan tahun yang dipilih
    df = df[df['dteday'].dt.year == tahun_pilihan]

    # Menghitung total penyewaan per bulan
    df_groupby_month = df.groupby('mnth')['cnt'].sum()

    # Membuat bar chart
    fig1, ax1 = plt.subplots(figsize=(7, 6))
    plt.bar(df_groupby_month.index, df_groupby_month)
    plt.xlabel('Bulan')
    plt.ylabel('Total Penyewaan Sepeda')
    plt.title('Total Penyewaan Sepeda per Bulan ({})'.format(tahun_pilihan))

    # Membuat pie chart
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    plt.pie(df_groupby_month, labels=df_groupby_month.index, autopct='%1.1f%%')
    plt.title('Total Penyewaan Sepeda per Bulan')

    # Menampilkan chart di Streamlit
    st.pyplot(fig1)
    st.pyplot(fig2)

    # Menampilkan tabel data
    st.table(df_groupby_month.to_frame())

# Analisis Sewa Jam
elif selected_page == "hour":

    st.header('Analisis Data Sewa Jam')

    # Import data
    data_jam = pd.read_csv('hour.csv')

    # Memilih data 8 baris pertama
    hr_data = data_jam['hr'].head(30)
    registered_data = data_jam['registered'].head(30)

    # Membuat plot
    fig, ax = plt.subplots(figsize=(8, 4))

    # Plot kolom 'hr'
    ax.plot(hr_data, label='hr', marker='o')

    # Plot kolom 'registered'
    ax.plot(registered_data, label='registered', marker='o')

    # Menambahkan judul dan label
    ax.set_title('Perbandingan Data Kolom hr dan registered')
    ax.set_xlabel('Index')
    ax.set_ylabel('Nilai')

    # Menambahkan legenda
    ax.legend()

    # Tabel jam
    df_jam_aggr = data_jam.groupby('hr')['registered'].sum().head(30)
    st.table(df_jam_aggr.to_frame())

    # Menampilkan plot di Streamlit
    st.pyplot(fig)

    # Heatmap Temperatur selama 6 Bulan
    st.header('Heatmap Temperatur selama 6 Bulan')

    # Mengambil data 6 bulan pertama
    df_6bulan = df_groupby_month.to_frame().loc[df_groupby_month.index <= 6, :] 

    # Menampilkan data tabel
    st.table(df_6bulan)

    # Mengatur kolom 'temp' sesuai kebutuhan
    df_6bulan['temp'] = df_6bulan.index

    fig3, ax3 = plt.subplots(figsize=(8, 6))

    # Membuat heatmap
    heatmap_data = df_6bulan.pivot_table(values='cnt', index='mnth', columns='temp', aggfunc='sum')
    sns.heatmap(heatmap_data, ax=ax3, annot=True, fmt="g", cmap="YlOrRd")

    # Menambahkan judul dan label
    plt.title('Heatmap Temperatur selama 8 Bulan')
    plt.xlabel('Temperatur (°C)')
    plt.ylabel('Bulan')

    # Menampilkan plot di Streamlit
    st.pyplot(fig3)


