
import requests
import pandas as pd
import time
import random

# 1. Definisi endpoint API
url = "https://jsonplaceholder.typicode.com/posts"

# Menambahkan User-Agent kustom untuk mematuhi etika ekstraksi data
headers = {"User-Agent": "TugasDataMiningBot/1.0 (+https://untirta.ac.id/bot)"}

# Menerapkan jeda antar permintaan (politeness)
time.sleep(random.uniform(1, 3))

# 2. Eksekusi permintaan GET
response = requests.get(url, headers=headers)

# 3. Validasi status 200 OK
if response.status_code == 200:
    print("Permintaan berhasil! Status:", response.status_code)
    
    # Parsing JSON ke tipe native Python
    data = response.json()
    
    # Membentuk struktur Data Frame awal
    df = pd.DataFrame(data)
    
    # 4. Mengubah ke format panjang (Melting)
    # Meleburkan kolom 'title' dan 'body' menjadi baris
    df_long = pd.melt(
        df, 
        id_vars=['userId', 'id'], 
        var_name='element', 
        value_name='value'
    )
    print("\nContoh Format Panjang (Melted):")
    print(df_long.head(2))
    
    # 5. Mengembalikan ke bentuk Tidy (Casting)
    # Menyebarkan kembali variabel 'element' menjadi kolom 'title' dan 'body'
    df_tidy = df_long.pivot(
        index=['userId', 'id'], 
        columns='element', 
        values='value'
    ).reset_index()
    
    # Membersihkan nama indeks sisa pivoting
    df_tidy.columns.name = None
    
    # 6. Menyimpan hasil Tidy Data ke CSV
    # index=False mencegah kolom indeks tambahan, encoding="utf-8" menjaga karakter non-ASCII
    df_tidy.to_csv("posts.csv", index=False, encoding="utf-8")
    print("\nData rapi (Tidy Data) berhasil diekspor ke posts.csv")
    
else:
    print(f"Gagal. Endpoint mengembalikan kode status: {response.status_code}")