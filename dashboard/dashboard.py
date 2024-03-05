import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import seaborn as sns
import streamlit as st
import numpy as np
from babel.numbers import format_currency
import matplotlib.dates as mdates
sns.set(style='dark')

##################################################

# PERSIAPAN DATA
df=pd.read_csv("https://raw.githubusercontent.com/lutfi-reza/BANGKIT/main/air_quality.csv")
air = df

# Drop columns yang tidak dibutuhkan
air.drop(['RAIN', 'wd', 'station', 'PRES','DEWP','WSPM'], axis=1,inplace=True)
# Fill missing values in specific columns with median
columns_to_fill = ['SO2', 'NO2', 'CO', 'O3']
df[columns_to_fill] = df[columns_to_fill].fillna(df[columns_to_fill].median())

# Membuat kolom baru 'waktu' dari kolom 'day', 'month', and 'year'
air['waktu'] = air['day'].astype(str) + '-' + air['month'].astype(str) + '-' + air['year'].astype(str)

# Formatting 'waktu' ke datetime format
air['waktu'] = pd.to_datetime(air['waktu'], format='%d-%m-%Y')

# Menghilangkan 'day', 'month', and 'year' 
air.drop(['day', 'month', 'year'], axis=1,inplace=True)

page = st.sidebar.selectbox('Menu Utama', ('Data dan Persiapan','Plot Deret Waktu', 'Analisis Regresi'))

################################################    
if page == 'Data dan Persiapan':
    #Data Awal
    st.subheader("Data Awal")
    st.write("Data yang digunakan dalam analisis ini adalah data kualitas udara di Stasiun Huairou, dengan 17 variabel, yaitu:")
    st.markdown("""
    1. Year
    2. Month
    3. Day
    4. Hour
    5. PM2.5
    6. PM10
    7. SO2
    8. NO2
    9. CO
    10. O3
    11. TEMP
    12. PRES
    13. DEWP
    14. RAIN
    15. wd
    16. WSPM
    """)
    st.dataframe(df)
    
    #Menghilangkan data yang tidak akan digunakan dalam analisis
    
    st.subheader("Data Setelah Cleaning")
    st.write("Pada data ini dilakukan cleaning berupa menghilangkan beberapa variabel dan juga menambahkan variabel baru bertnama `waktu` yang merupakan kombinasi dari `year`, `month`, dan `day`.")
    st.dataframe(air)
    
##################################################
elif page == 'Plot Deret Waktu':
    
    st.subheader("Plot Time Series PM2.5")
    # Visualisasi 1: Time Series Plot PM2.5
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='waktu', y='PM2.5', data=air)
    ax.set_title('Time Series Plot PM2.5')
    ax.set_xlabel('Date')
    ax.set_ylabel('PM2.5')
    st.pyplot(fig)

    st.subheader("Plot Time Series PM10")
    # Visualisasi 2: Time Series Plot PM10
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='waktu', y='PM10', data=air)
    ax.set_title('Time Series Plot PM10')
    ax.set_xlabel('Date')
    ax.set_ylabel('PM10')
    st.pyplot(fig)
    
    st.write(" Pada Plot Time Series PM2.5 terlihat bahwa terdapat pola musiman, di mana setiap awal tahun terjadi kelonjakan jumlah partikel PM2.5 dan PM10 di udara. Kedua variabel ini merupakan partikel yang biasanya berasal partikel udara halus yang umumnya berasal dari antropogenik seperti kendaraan bermotor, pembakaran biomassa dan pembakaran bahan bakar. Hal ini sangat mungkin terjadi karena akhir tahun dan awal tahun adalah momentum bagi masyarakat untuk melaksanakan berpergian yang lebih intens. Secara subjektif diketahui bahwa data belum stasioner, baik secara ragam dan nilai tengah dengan nilai tengah yang beragam dan lebar pita yang terbentuk sangat beragam akibat fluktuatif data.")


##################################################
elif page == 'Analisis Regresi':
    y1=air['PM2.5'].values.reshape(-1,1)
    x=air['TEMP'].values.reshape(-1,1)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.regplot(x=x, y=y1, data=air, line_kws={'color': '#A25772'}, scatter_kws={'color': '#9EB8D9'})
    ax.set_title('Regresi PM2.5 dan TEMP')
    ax.set_xlabel('TEMP')
    ax.set_ylabel('PM2.5')
    st.pyplot(fig)

    y2=air['PM10'].values.reshape(-1,1)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.regplot(x=x, y=y2, data=air, line_kws={'color': '#A25772'}, scatter_kws={'color': '#9EB8D9'})
    ax.set_title('Regresi PM10 dan TEMP')
    ax.set_xlabel('TEMP')
    ax.set_ylabel('PM10')
    st.pyplot(fig)
    
    st.write("Berdasarkan plot regresi terlihat bahwa hampir tidak ada hubungan antara temperature dengan PM2.5 dan PM10. Berdasarkan penelitian temperatur udara berkorelasi negatif terhadap PM2,5 dan PM10. Penyebabnya adalah penurunan suhu di malam hari menurunkan difusi partikel sehingga meningkatkan konsentrasi PM2,5 dan PM10 (Hernandez dkk, 2017).")
##################################################
