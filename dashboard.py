import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Menambahkan judul di navbar
st.set_page_config(layout="wide")

# Membuat sidebar
st.title('Dashboard Visualisasi Data Penyewaan Sepeda')
st.sidebar.write("Anggota :")
st.sidebar.write("Nama: Rafly Maulana Zulyzar")
st.sidebar.write("NIM: 10122790")
menu = ["day", "hour"]
selected_page = st.sidebar.selectbox("Halaman", menu)



@st.cache_data
#Load Data CSV
def load_data(url) :
    df = pd.read_csv(url)
    return df

data_jam = load_data("https://raw.githubusercontent.com/RaflyMZ/VisualisasiSewaSepeda/e2228d187e4251f6e3b5673052e74fb219945e8a/hour.csv")
dfDay = load_data("https://raw.githubusercontent.com/RaflyMZ/VisualisasiSewaSepeda/e2228d187e4251f6e3b5673052e74fb219945e8a/day.csv")
#dfDay = pd.read_csv('day.csv')

# Mengelompokkan data berdasarkan bulan dan menghitung total penyewaan
dfDay_groupby_month = dfDay.groupby('mnth')['cnt'].sum()

# Menampilkan visualisasi berdasarkan pilihan di sidebar

# Analisis Sewa Harian
if selected_page == "day":

    st.header('Analisis Data Sewa Harian')

    st.write("Penjelasan: Berdasarkan Chart dibawah, ini merupakan informasi mengenai total penyewaan sepeda tiap bulan. ")
    st.write("Jika kita mengambil informasi dari chart dibawah, kita dapat melihat tren di bulan keberapakah penyewaan sepeda terbanyak.")

    # Mengubah kolom dteday menjadi datetime
    dfDay['dteday'] = pd.to_datetime(dfDay['dteday'])

    # Membuat sidebar
    st.sidebar.header('Filter Data')
    # Memilih data tahun
    tahun_pilihan = st.sidebar.selectbox('Pilih Tahun', dfDay['dteday'].dt.year.unique())

    # Memfilter data berdasarkan tahun yang dipilih
    dfDay = dfDay[dfDay['dteday'].dt.year == tahun_pilihan]

    # Menghitung total penyewaan per bulan
    df_groupby_month = dfDay.groupby('mnth')['cnt'].sum()

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

    # Menampilkan tabel data di dalam expander
    with st.expander("Tabel Total Penyewaan Sepeda per Bulan"):
        st.table(df_groupby_month.to_frame())
    #Penjelasan Chart
    with st.expander("Penjelasan Chart") :
        st.write('Chart diatas menampilkan perbandingan total orang yang menyewa sepeda pada tiap bulannya. Dengan Informasi ini kita dapat mengetahui pada bulan keberapa penyewaan terbanyak, sehingga dengan informasi ini dapat menambah informasi untuk strategi marketing. Akan tetapi jika hanya data ini yang dikumpulkan belum cukup untuk membuat strategi sehingga perlu dilakukannya analisis lagi seperti pada analisis lanjutan')

    



    # Viaualisasi Perbandingan total sewa hari kerja dan weekend/holiday
    st.header('Perbandingan total sewa hari kerja dan weekend/holiday')
    st.write("Penjelasan: Berdasarkan Chart dibawah, ini merupakan informasi mengenai total penyewaan sepeda berdasarkan hari kerja dan holiday/weekend ")
    st.write("Jika kita mengambil informasi dari chart dibawah, kita dapat melihat tren di hari apakah penyewaan sepeda terbanyak.")


    import streamlit as st
    import pandas as pd
    import matplotlib.pyplot as plt

 
    # Mengelompokkan data berdasarkan workingday dan menghitung total penyewaan
    rentals_by_day_type = dfDay.groupby('workingday')['cnt'].sum()


    # Memvisualisasikan data dengan diagram batang
    plt.figure(figsize=(8, 6))
    rentals_by_day_type.plot(kind='bar', color=['skyblue', 'salmon'])
    plt.title('Total Penyewaan Sepeda Berdasarkan Hari')
    plt.xlabel('Hari (0: Hari Kerja, 1: Akhir Pekan/Hari Libur)')
    plt.ylabel('Total Penyewaan')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(plt)

    # Menampilkan tabel data di dalam expander
    with st.expander("Tabel Total Penyewaan Sepeda Berdasarkan Hari"):
        st.write(rentals_by_day_type)
    with st.expander("Penjelasan Chart") :
        st.write('Chart diatas menampilkan perbandingan total orang yang menyewa sepeda pada hari biasa dengan holiday/weekend. Dengan informasi ini, pihak strategi marketing dapat mengetahui tren masyarakat paling banyak menyewa pada hari apa dan jika disambungkan dengan analisis sebelumnya yang dimana penyewaan terbanyak pada bukan ke-6 sampai dengan 8 memiliki banyak hari libur sehingga orang yang menyewa sepeda pun banyak.')

# Analisis Sewa Jam
elif selected_page == "hour":

    st.header('Analisis Data Sewa Jam')
    st.write("Penjelasan: Berdasarkan Chart dibawah, ini merupakan informasi mengenai perbandingan total jam sewa penyewa dengan total penyewa ")
    st.write("Jika kita mengambil informasi dari chart dibawah, kita dapat melihat tren berapa jam kah biasanya rata-rata penyewa ambil")


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
    with st.expander("Tabel Total Penyewaan Sepeda Berdasarkan Jam"):
        st.table(df_jam_aggr.to_frame())
    
    # Menampilkan plot di Streamlit
    st.pyplot(fig)
    with st.expander("Penjelasan Chart") :
        st.write('Chart diatas menampilkan perbandingan total jam yang diambil penyewa dengan total penyewa yang mengambil total jam tersebut. Dengan informasi ini pihak strategi marketing dapat mengetahui total jam yang paling laku atau total jam yang biasa konsumen ambil. Contohnya bisa saja pihak strategi dapat memberikan semacam diskon jika penyewa yang mengambil 1 jam sewa akan mendapatkan sebuah promo atau diskon sehingga dapat menaikan ketertarikan pelaku pada total jam tersebut')




    # Heatmap Temperatur selama 8 Bulan
    st.header('Heatmap Temperatur selama 8 Bulan')
    st.write("Penjelasan: Berdasarkan Chart dibawah, ini merupakan informasi mengenai perbandingan temperatur pada hari sewa dengan total penyewa ")
    st.write("Jika kita mengambil informasi dari chart dibawah, kita dapat melihat tren pada suhu berapakah biasanya konsumen menyewa sepeda")


    # Mengambil data 8 bulan pertama
    df_8bulan = dfDay_groupby_month.to_frame().loc[dfDay_groupby_month.index <= 8, :] 

    # Menampilkan data tabel di dalam expander
    with st.expander("Tabel Data Temperatur selama 8 Bulan"):
        st.table(df_8bulan)

    # Mengatur kolom 'temp' sesuai kebutuhan
    df_8bulan['temp'] = df_8bulan.index

    fig3, ax3 = plt.subplots(figsize=(8, 6))

    

    # Membuat heatmap
    heatmap_data = df_8bulan.pivot_table(values='cnt', index='mnth', columns='temp', aggfunc='sum')
    sns.heatmap(heatmap_data, ax=ax3, annot=True, fmt="g", cmap="YlOrRd")

    # Menambahkan judul dan label
    plt.title('Heatmap Temperatur selama 8 Bulan')
    plt.xlabel('Temperatur (°C)')
    plt.ylabel('Bulan')

    # Menampilkan plot di Streamlit
    st.pyplot(fig3)
    with st.expander("Penjelasan Chart") :
        st.write('Chart diatas menampilkan perbandingan Total penyewa dengan suhu total selama 8 bulan. Dengan informasi ini kita dapat mengetahui pada suhu berapakah biasanya konsumen menyewa sepeda, seperti contoh total suhu pada bulan ke-8 cenderung yang paling panas sehingga pada bulan ke-8 suhu saat itu agak hangat atau panas sehingga selain hari libur, konsumen pun biasanya menyewa jika suhu pada hari itu normal atau panas.')



