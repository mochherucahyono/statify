# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# 1. KONFIGURASI HALAMAN (TEMA DARK/MINIMALIS)
st.set_page_config(page_title="Statify", layout="wide")

# Gaya CSS Kustom agar tampilannya elegan (Monokrom)
st.markdown("""
    <style>
    .main { background-color: #0b0f19; color: #f8fafc; }
    h1 { font-weight: 800; letter-spacing: -1px; }
    </style>
""", unsafe_allow_html=True)

# 2. HEADER WEBSITE
st.title("STATIFY - Analisis Data")
st.caption("Analisis datamu di sini. Unggah file, pilih variabel, pantau visualisasi.")
st.write("---")

# 3. FITUR UPLOAD FILE (CSV atau Excel)
uploaded_file = st.file_uploader("Upload file data kamu di sini (Format .csv atau .xlsx)", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Membaca file berdasarkan formatnya secara otomatis
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.success("Data berhasil dimuat!")
        
        # MEMBAGI LAYAR MENJADI 2 KOLOM
        kolom_kiri, kolom_kanan = st.columns([1, 2])
        
        with kolom_kiri:
            st.subheader("Ringkasan Data")
            st.write(f"**Total Baris:** {df.shape[0]}")
            st.write(f"**Total Kolom:** {df.shape[1]}")
            
            # Menampilkan statistik deskriptif untuk angka (Rata-rata, Min, Max, dll)
            st.write("**Statistik Dasar:**")
            st.dataframe(df.describe().T)

        with kolom_kanan:
            st.subheader("Preview Tabel Data")
            # Menampilkan 5 data teratas secara interaktif
            st.dataframe(df.head(10))

        st.write("---")
        st.subheader("Visualisasi Grafik Interaktif")
        
        # Ambil daftar nama kolom untuk dijadikan pilihan di dropdown
        daftar_kolom = df.columns.tolist()
        
        kolom_kontrol_1, kolom_kontrol_2, kolom_kontrol_3 = st.columns(3)
        with kolom_kontrol_1:
            sumbu_x = st.selectbox("Pilih Kolom Sumbu X:", daftar_kolom)
        with kolom_kontrol_2:
            sumbu_y = st.selectbox("Pilih Kolom Sumbu Y (Angka):", daftar_kolom)
        with kolom_kontrol_3:
            jenis_grafik = st.selectbox("Pilih Jenis Grafik:", ["Garis (Line)", "Batang (Bar)", "Titik (Scatter)"])

        # LOGIKA PEMBUATAN GRAFIK BERDASARKAN PILIHAN USER
        if jenis_grafik == "Garis (Line)":
            fig = px.line(df, x=sumbu_x, y=sumbu_y, title=f"Grafik Tren: {sumbu_y} berdasarkan {sumbu_x}", template="plotly_dark")
        elif jenis_grafik == "Batang (Bar)":
            fig = px.bar(df, x=sumbu_x, y=sumbu_y, title=f"Grafik Perbandingan: {sumbu_y} berdasarkan {sumbu_x}", template="plotly_dark")
        else:
            fig = px.scatter(df, x=sumbu_x, y=sumbu_y, title=f"Grafik Distribusi: {sumbu_y} berdasarkan {sumbu_x}", template="plotly_dark")
            
        # Tampilkan grafik ke website
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses data: {e}")
        
else:
    # Tampilan awal saat user belum upload file
    st.info("Silakan upload file CSV atau Excel kamu di atas untuk memulai analisis otomatis.")

st.write("---")
st.caption("@ 2026 STATIFY. Dibuat oleh Heru Cahyono")