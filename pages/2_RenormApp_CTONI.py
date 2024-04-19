import pandas as pd
import numpy  as np
import streamlit as st
from pandas.api.types import is_numeric_dtype

# Page Config
st.set_page_config(layout="wide",page_title="FAC Renorm App v1 - CTONI")

# Header
st.header('CTONI IQ Classification App')

# File uploader
colL, colR = st.columns(2)

with colL:
    uploaded_file = st.file_uploader("Pilih file data IQ:")
    if uploaded_file is not None:
        data_CTONI_input = pd.read_csv(uploaded_file, sep =';')
        st.dataframe(data_CTONI_input, height = 200)

        # Columns name
        data_colname    = list(data_CTONI_input.columns)

        # Select column for category  
        select_cat  = st.selectbox('(1) Pilih kolom kategori:', data_colname)

        # Select column for category
        select_iq   = st.selectbox('(2) Pilih kolom data IQ:', data_colname)
    else:
        data_CTONI_input = None
        data_colname    = None
        select_cat      = None
        select_iq       = None

# Initialize Button
if st.button('Calculate'):
    # Column selection check
    if data_CTONI_input is None:
        st.warning("Pastikan upload file data IQ")
        st.stop()        
    elif select_cat == select_iq:
        st.warning("Pastikan pilih kolom '(1) Kategori' dan '(2) IQ Data' yang berbeda")
        st.stop()
    # IQ data column dtype check
    elif is_numeric_dtype(data_CTONI_input.loc[:,select_iq]) != True :
        st.warning("Pastikan kolom 'IQ data (2)' memiliki datatype numerikal")
        st.stop()
    # Execute Calculation
    else:
        class_category_list = data_CTONI_input.loc[:,select_cat].unique()

        IQtable_all = []

        for class_ in class_category_list:
            data_temp = data_CTONI_input[data_CTONI_input[select_cat] == class_].loc[:,select_iq]

            max_col_perc = [87.5,75,62.5,50,37.5,25,12.5]

            min_col = []
            max_all = max(data_temp)
            max_col = [max_all]

            for max_per in max_col_perc:
                temp_max = np.floor(np.percentile(data_temp,max_per))
                max_col.append(temp_max)
            
            for i in range(1,len(max_col)):
                min_col.append(max_col[i]+1)
            min_col.append(min(data_temp))
            
            w_class = ['(8) Tinggi di atas rata-rata','(7) Di atas rata-rata','(6) Sedikit di rata-rata',
                    '(5) Rata-rata atas','(4) Rata-rata','(3) Rata-rata bawah',
                    '(2) Sedikit di bawah rata-rata','(1) Di bawah rata-rata']

            IQtable_temp = pd.DataFrame(data={'WeschlerClass':w_class,'min_score':min_col,'max_score':max_col})
            IQtable_temp['classification'] = class_
            IQtable_all.append(IQtable_temp)

        IQtable_final = pd.concat(IQtable_all, ignore_index=True)
        st.dataframe(IQtable_final, height=400, width=600)
