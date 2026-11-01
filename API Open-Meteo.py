import requests
import pandas as pd
import time
import random

# 1. Endpoint API Open-Meteo sesuai petunjuk tugas
url = "https://api.open-meteo.com/v1/forecast?latitude=-6.2&longitude=106.8&daily=temperature_2m_max,temperature_2m_min&timezone=Asia/Jakarta"

# Konfigurasi User-Agent dan jeda (politeness)
headers = {"User-Agent": "TugasDataMiningBot/1.0 (+https://untirta.ac.id/bot)"}
time.sleep(random.uniform(1, 3))

# 2. Eksekusi permintaan HTTP GET
response = requests.get(url, headers=headers)

# 3. Validasi status 200 OK
if response.status_code == 200:
    print("Permintaan berhasil (200 OK)!\n")
    
    # Parsing JSON
    data = response.json()
    
    # 4. Membentuk Data Frame awal dari objek "daily"
    daily_data = data['daily']
    df = pd.DataFrame({
        'tanggal': daily_data['time'],
        'tmax': daily_data['temperature_2m_max'],
        'tmin': daily_data['temperature_2m_min']
    })
    
    print("--- Data Frame Awal ---")
    print(df.head(3), "\n")
    
    # 5. Format Panjang (Melting)
    # Menyatukan kolom tmax dan tmin menjadi satu kolom 'element'
    df_long = pd.melt(
        df,
        id_vars=['tanggal'],
        var_name='element',
        value_name='value'
    )
    
    print("--- Format Panjang (Melting) ---")
    print(df_long.head(4), "\n")
    
    # 6. Format Tidy (Casting/Pivoting)
    # Mengembalikan kolom 'element' menjadi variabel tmax dan tmin
    df_tidy = df_long.pivot(
        index='tanggal',
        columns='element',
        values='value'
    ).reset_index()
    
    df_tidy.columns.name = None # Menghapus sisa nama indeks 'element'
    
    print("--- Bentuk Tidy Data Akhir ---")
    print(df_tidy.head(3), "\n")
    
    # 7. Simpan ke cuaca.csv
    df_tidy.to_csv("cuaca.csv", index=False, encoding="utf-8")
    print("Berhasil diekspor ke cuaca.csv")

else:
    print(f"Permintaan gagal! Status code: {response.status_code}")