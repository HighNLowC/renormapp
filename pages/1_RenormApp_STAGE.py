import pandas as pd
import numpy  as np
import streamlit as st

# Page Config
st.set_page_config(layout="wide",page_title="FAC Renorm App v1 - STAGE")

# Header
st.header('STAGE Renorm App')

# Data info variables (dim_fac and dim_fac_item_count matches based on index)
dim_fac             = ['S','S1','S2','S3','S4',
                       'T','T1','T2','T3','T4','T5',
                       'A','A1','A2','A3','A4',
                       'G','G1','G2','G3','G4',
                       'E','E1','E2','E3','E4','E5','E6']
dim_fac_item_count  = [17,4,3,5,5,
                       22,5,5,5,3,4,
                       20,4,7,4,5,
                       18,4,4,6,4,
                       30,7,7,5,4,3,4]


# STAGE dim_fac score dataframe
minScore_dim_fac    = np.array(dim_fac_item_count)
maxScore_dim_fac    = list(minScore_dim_fac * 5)
dim_fac_score       = pd.DataFrame(data={'dim_fac'   : dim_fac,
                                         'min_score' : minScore_dim_fac,
                                         'max_score' : maxScore_dim_fac})

# File uploader
colL, colR = st.columns(2)

with colL:
    uploaded_file = st.file_uploader("Pilih file '(1) DATA STAGE' (pastikan struktur data/penamaan kolom file sudah sesuai):")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file, sep =';')
        st.dataframe(data, height = 200)

        # Columns name
        data_colname        = list(data.columns)
        class_list          = [i for i in data_colname if i not in dim_fac]

        # Select column for category  
        select_cat = st.selectbox('Select categories column:', class_list)
    else:
        data            = None
        data_colname    = None
        class_list      = None
        select_cat      = None

with colR:
    uploaded_file_padanan = st.file_uploader("Pilih file '(2) PADANAN STAGE':")
    if uploaded_file_padanan is not None:
        stagecomp_padanan = pd.read_csv(uploaded_file_padanan, sep =';')
        st.dataframe(stagecomp_padanan, height = 200)
    else:
        stagecomp_padanan = None

# Initialize Button
if st.button('Calculate'):

    if data is None or stagecomp_padanan is None:
        st.warning("Pastikan upload file '(1) DATA STAGE' & '(2) PADANAN STAGE'!")
        st.stop()   

    else:
        #Subheader
        st.subheader('Hasil Perhitungan Renorm/STEN STAGE')

        #Category Count
        candidate_per_client = pd.DataFrame(data = data[select_cat].value_counts())
        candidate_per_client.reset_index(inplace=True)
        st.write('Candidate Count per Category Class')
        st.dataframe(candidate_per_client, height = 200, width=600)

        #Container
        col1, col2 = st.columns(2)

        # Result Left(1) Col - Norm
        with col1:
            #class categories unique list
            st.write('New Norm Scores (T-Score)')
            class_category_list = data.loc[:,select_cat].unique()

            normTable_allgroups = []
            for class_ in class_category_list:
                data_temp = data[data[select_cat] == class_].drop(columns=class_list)

                normTable_groups = []
                for i in dim_fac:
                    dim_fac_select  = data_temp.loc[:,i]
                    mean            = np.mean(dim_fac_select)
                    std             = np.std(dim_fac_select)

                    min_score = dim_fac_score[dim_fac_score['dim_fac'] == i].loc[:,'min_score']
                    min_score = int(min_score.iloc[0])
                    max_score = dim_fac_score[dim_fac_score['dim_fac'] == i].loc[:,'max_score']
                    max_score = int(max_score.iloc[0])

                    raw_list       = []
                    for o in range(min_score,max_score+1):
                        raw_list.append(o)
                    
                    scaled_list    = []
                    for p in raw_list:
                        scaled_score = (((p-mean)/std)*10)+50
                        scaled_list.append(np.floor(scaled_score))
                    
                    norm_temp = pd.DataFrame(data={'raw_score':raw_list,'scaled_score0':scaled_list})
                    norm_temp['dim_fac'] = i
                    normTable_groups.append(norm_temp)

                normTable_class = pd.concat(normTable_groups, ignore_index=True)
                normTable_class['classification'] = class_
                normTable_allgroups.append(normTable_class)

            normTable_final = pd.concat(normTable_allgroups, ignore_index=True)

            scaled_score1   = []
            for i in normTable_final['scaled_score0']:
                if i<0:
                    scaled_score1.append(0)
                else:
                    scaled_score1.append(i)

            normTable_final['scaled_score'] = scaled_score1

            normTable_final = normTable_final.loc[:,['dim_fac','raw_score','scaled_score','classification']]
            st.dataframe(normTable_final, height = 400, width=600)

        # Result Right(2) Col - STEN
        with col2:
            st.write('New STEN Score')
            # STEN SCORE TABLE 1
            ## Convert Sum of Raw Scores based on new norm table
            converted_Data_all      = []

            for class_ in class_category_list:
                convertedData_temp  = pd.DataFrame()

                for i in dim_fac:
                    subset_norm     = normTable_final[normTable_final['dim_fac'].isin([i]) & normTable_final['classification'].isin([class_])]
                    
                    subset_dimfac   = data[data[class_list[1]] == class_].loc[:,[i]] #####FOR APP INGET INGET####

                    convert_dimfac  = subset_dimfac.merge(how='left',left_on=i,right=subset_norm,right_on='raw_score')

                    convertedData_temp[i] = convert_dimfac['scaled_score']
                
                convertedData_temp['classification'] = class_
                converted_Data_all.append(convertedData_temp)
            
            # STEN SCORE TABLE 2
            ## Define Functions and scoring matrix ##

            #sten to score
            def sten_to_score(sten,mean,std):
                score    = (((sten - 5.5)/2)*std)+mean
                return score

            # t to cluster
            def t_to_cluster(score):
                if score < 34:
                    return 'a'
                elif score > 33 and score < 45:
                    return 'b'
                elif score > 44 and score < 56:
                    return 'c'
                elif score > 55 and score < 66:
                    return 'd'
                else:
                    return 'e'

            #Cluster to Score Matrix
            level   = ['--','-','=','+','++']
            cluster = ['a','b','c','d','e']

            dim_fac_spread  = []
            level_spread    = []
            cluster_spread  = []

            for a in dim_fac:
                for b in level:
                    for c in cluster:
                        dim_fac_spread.append(a)
                        level_spread.append(b)
                        cluster_spread.append(c)

            df                      = pd.DataFrame(data = {'cluster_core':[80,70,50,30,20,90,80,60,40,30,50,60,80,60,50,30,40,60,80,90,20,30,50,70,80]})
            cluster_score           = df.iloc[:,-1]
            cluster_score_spread    = []

            while len(cluster_score_spread) < 700:
                for o in cluster_score:
                    cluster_score_spread.append(o)

            score_matrix = pd.DataFrame(data={"dimension_facet":dim_fac_spread,"level":level_spread,"cluster":cluster_spread,"score":cluster_score_spread})

            # STEN SCORE TABLE 3
            ## STEN creation ##
            # Unique List of Competencies Names
            stagecomp_list      = stagecomp_padanan.loc[:,'Kompetensi'].unique()

            #Zip for loop
            zippedSTEN = zip(converted_Data_all,class_category_list)

            #Empty list for df repo (to be concatenated)
            stenTable_all = []

            #for loop STEN creation
            for df,class_ in zippedSTEN:

                stenTable_allcomps =[]

                for comp in stagecomp_list:
                    data_temp       = df.loc[:,dim_fac]
                    padanan_temp    = stagecomp_padanan[stagecomp_padanan['Kompetensi'] == comp]

                    dim_fac_pick    = list(padanan_temp.loc[:,'dim_fac'])
                    level_pick      = list(padanan_temp.loc[:,'level'])

                    ## For Loop ##
                    ## Padanan for Matching ##
                    padanan         = [] #list with dataframe for matching
                    forpadanan      = zip(dim_fac_pick,level_pick)

                    for i,o in forpadanan:
                        temp = score_matrix[score_matrix['dimension_facet'].isin([i]) & score_matrix['level'].isin([o])] #note isin()
                        padanan.append(temp)

                    ## Tscore data to Cluster data ##
                    cluster_data = data_temp.map(t_to_cluster)

                    ## Cluster data clean ##
                    cluster_data2 = cluster_data.loc[:,dim_fac_pick]

                    ## Cluster to score ##
                    col_num         = range(0,len(dim_fac_pick))
                    zipped          = zip(col_num,dim_fac_pick)

                    score_data      = pd.DataFrame()
                    col_name_dim    = []

                    for i,o in zipped:
                        tempcol     = cluster_data2.iloc[:,[i]]
                        tempdata    = padanan[i]
                            
                        tempscore   = pd.merge(left=tempcol,right=tempdata,left_on=o,right_on='cluster',how='left')
                        tempscore   = tempscore.iloc[:,[-1]]

                        score_data[o] = tempscore

                        col_name_dim.append(o[0])

                    ## Dimension Averages ##
                    # Rename Columns
                    rename_col_name     = dict(zip(dim_fac_pick,col_name_dim))
                    score_data2         = score_data.rename(columns=rename_col_name) #renamed columns dataframe
                    col_name_set        = set(col_name_dim)
                    # Averages (score_data3)
                    score_data3         = pd.DataFrame()
                    for i in col_name_set:
                        score_data3[i]  = score_data2.loc[:,[i]].apply(np.average,axis=1).apply(np.round)

                    ## Final Data ##
                    # Rename to avg_score
                    average_score_data  = score_data3.apply(np.average,axis=1).apply(np.floor)
                    avg_data            = pd.DataFrame(data={'avg_score':average_score_data})

                    ## To STEN ##
                    mean_avgscore       = avg_data.apply(np.average,axis=0)
                    mean_avgscore       = float(mean_avgscore.iloc[0])
                    std_avgscore        = avg_data.apply(np.std,axis=0)
                    std_avgscore        = float(std_avgscore.iloc[0])

                    sten_empty    = list(range(1,11))
                    score         = []
                    for i in sten_empty:
                        temp    = sten_to_score(sten=i,mean=mean_avgscore,std=std_avgscore)
                        score.append(int(np.floor(temp)))

                    #sten values
                    sten_anc    = pd.DataFrame(data={'score':score,'sten':sten_empty})

                    #final sten table
                    score_anc   = list(range(0,101))
                    score_anc   = pd.DataFrame(data={'score':score_anc})

                    final_sten  = pd.merge(how='left',left=score_anc,right=sten_anc,left_on='score',right_on='score')
                    final_sten  = final_sten.bfill().fillna(value=10)
                    final_sten['competencies'] = comp
                    stenTable_allcomps.append(final_sten)
                
                stenTable_perclass = pd.concat(stenTable_allcomps, ignore_index=True)
                stenTable_perclass['classification'] = class_
                stenTable_all.append(stenTable_perclass)

            stenTable_final = pd.concat(stenTable_all, ignore_index=True)
            st.dataframe(stenTable_final, height = 400, width=600)
