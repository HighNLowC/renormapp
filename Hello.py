# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st

# Title
st.title('STAGE & CTONI Renorm App v1 :100:')
st.divider()

st.subheader('Gambaran Aplikasi & Instruksi')
st.write('''
         Aplikasi "STAGE & CTONI Renorm App" milik FAC dibuat untuk memudahkan dan mempercepat proses pembuatan norma
         untuk alat ukur STAGE dan CTONI. Aplikasi ini dirangkai menggunakan bahasa pemrograman Python, menggunakan 
         framework/package "streamlit".
         ''')
st.write('''
         Untuk mengakses aplikasi, silakan membuka sidebar yang terdapat pada bagian kiri penampang web ini.
         Web ini terdiri dari dua aplikasi:
         ''')       
st.write('''
            - I. Pada aplikasi STAGE, user dapat melakukan:
            - 1) renorm untuk tabel konversi "Sum of Raw Score each Dimension/Facet" menjadi "SCALED SCORE (T)"
            - 2) renorm untuk tabel konversi 'Average Competency Score' menjadi 'STEN SCORE'.
         
            - User dapat mengunggah data STAGE peserta bersama dengan padanan kompetensi (pastikan menggunakan \
              struktur tabulasi yang tepat, atau dapat mengunduh template file .csv)
         ''')
st.write('''
            - II. Pada aplikasi CTONI, user dapat membuat tabel norma klasifikasi skor IQ berdasarkan kategori yang dipilih user. 
         
            - User dapat mengunggah data IQ peserta (pastikan menggunakan struktur tabulasi yang tepat, \
              atau dapat mengunduh template file .csv)
         ''')
st.write('''
         Instruksi lebih detail bersama dengan template file .csv data dan contoh file data yang dapat digunakan 
         diaplikasi ini, silakan menekan tombol di bawah ini untuk mengakses folder google drive:
         ''')

st.link_button(label="Folder Google Drive",url="https://drive.google.com/drive/folders/1c8t1x-NnH-k7UmJHQulLVgXzfX5e93y0?usp=sharing")
st.divider()

st.write(''' 
         Jika mendapati kesulitan selama menggunakan aplikasi ini, mohon kontak tim Research and Product Innovation FAC.
        
         Developer:
         Ian (RPI) - aplikasi v1\
        ''')
