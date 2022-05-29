import numpy as np
import streamlit as st
#import plotly_express as px
import pandas as pd
import xlrd
xlrd.xlsx.ensure_elementtree_imported(False, None)
xlrd.xlsx.Element_has_iter = True
from os import devnull, sep
import warnings
import re
import gspread
# configuration
st.set_option('deprecation.showfileUploaderEncoding', False)



# title of the app
st.title("PROCESOS DE DATOS GPON")

# Add a sidebar
st.sidebar.subheader("Primero cargar Trouble Tickets")

# Setup file upload
uploaded_file = st.sidebar.file_uploader(
                        label="Upload your CSV or Excel file. (200MB max)",
                         type=['csv', 'xlsx', 'XLS'])

global df
if uploaded_file is not None:
    print(uploaded_file)
    print("hello")

    try:
        df = pd.read_excel(uploaded_file, engine="openpyxl", skiprows=3)
        df.to_csv('AVERIAS/DT_AVERIAS_Trouble.csv',index=False,encoding='utf-8')

        datos = {
            'CONTRATA_TOA__c': ['ANALISIS DE RUIDO PEX','ANOVO','CABECERA','COBRA','COMFICA','CUARENTENA COE','DOMINION','ENERGIA','EZENTIS','FIBRA','GAC-VOIP','INGENIERIA HFC','LARI','LITEYCA','TRABAJOS PROGRAMADOS','TRANSMISIONES','TRATAMIENTO INTERMITENCIA','TRIAJE HFC','TRATAMIENTO CALL PIN TV-M1'],
            'codctr' : ['485','333','60','15','363','429','335','211','19','209','353','435','245','470','365','210','483','474','434']}
        df = pd.DataFrame(datos)
        #print(df)
        datos2 = {
            'Categorization Tier 3': ['Control Remoto'],
            'codmotv' : ['I129']
        }
        df2 = pd.DataFrame(datos2)
        #print(df2)
        Trouble = pd.read_csv('AVERIAS/DT_AVERIAS_Trouble.csv', sep=',', low_memory=False)
        Trouble=Trouble[['Incident Number','CREATION_DATE_CRM__c','Tipo de incidencia padre','CONTRATA_TOA__c','Categorization Tier 3','CUSTOMER_NAME_CRM__c','OBSERVATIONS_CRM__c','STREETTYPE_CRM__c','STREETNAME_CRM__c','STREETNUMBER_CRM__c','SUBUNITTYPE_CRM__c','DEPARTMENT_CRM','DISTRICT_CRM__c','Network Technology__c','LEX_NIL__c','BORNE_NIL__c','TROBA_ TYPE_NIL__c','TAP_STREET_NIL__c','PLANE_OLT_PORT','NODE_HFC_OLT_HOSTNAME','currentVozTelephone_OMS__c','currentVozProduct_OMS__c','currentVozServiceTechnology_OMS__c','currentBafAccessid_OMS__c','CFS_SERVICE_TECHNOLOGY_NIL__c']]
        #<<------------------------->>
        #comvertir año 1070-01-01 con  FECHA REAL
        Trouble['CREATION_DATE_CRM__c'] = pd.to_datetime(Trouble['CREATION_DATE_CRM__c'], errors='coerce', unit='d', origin='1899-12-30')
        Trouble['CREATION_DATE_CRM__c'] = pd.to_datetime(Trouble.CREATION_DATE_CRM__c, errors = 'coerce').dt.strftime("%Y/%m/%d  %H:%M:%S")
        #concatenated_df=pd.concat([Trouble,cms],ignore_index=True)
        union1 = pd.merge(left=Trouble,right=df, how='left', left_on='CONTRATA_TOA__c', right_on='CONTRATA_TOA__c')
        union2 = pd.merge(left=union1,right=df2, how='left', left_on='Categorization Tier 3', right_on='Categorization Tier 3')
        Trouble2=union2[['Incident Number','CREATION_DATE_CRM__c','Tipo de incidencia padre','codctr','CONTRATA_TOA__c','codmotv','Categorization Tier 3','CUSTOMER_NAME_CRM__c','OBSERVATIONS_CRM__c','STREETTYPE_CRM__c','STREETNAME_CRM__c','STREETNUMBER_CRM__c','SUBUNITTYPE_CRM__c','DEPARTMENT_CRM','DISTRICT_CRM__c','Network Technology__c','LEX_NIL__c','BORNE_NIL__c','TROBA_ TYPE_NIL__c','TAP_STREET_NIL__c','PLANE_OLT_PORT','NODE_HFC_OLT_HOSTNAME','currentVozTelephone_OMS__c','currentVozProduct_OMS__c','currentVozServiceTechnology_OMS__c','currentBafAccessid_OMS__c','CFS_SERVICE_TECHNOLOGY_NIL__c']]
        Trouble2["CFS_SERVICE_TECHNOLOGY_NIL__c"] = Trouble2["CFS_SERVICE_TECHNOLOGY_NIL__c"].replace({'VOIP':'VOZ','GPON':'DATOS','CATV':'TV','DOCSIS':''}, regex=True)
        Trouble2 = Trouble2.rename(columns={'CFS_SERVICE_TECHNOLOGY_NIL__c':'BORRAR',})
        additional_cols = ['codreq','fec_regist','codedo','codctr','desnomctr','codmotv','desmotv','nomcli','desobsordtrab','destipvia','desnomvia','numvia','destipurb','codofcadm','desdtt','tiptecnologia','codtap','codbor','codtrtrn','desurb','nroplano','codnod','numtelefvoip','codpromo','tiplinea','codcli','BORRAR']
        
        Trouble2 = Trouble.reindex(Trouble.columns.tolist() + additional_cols, axis = 1)
        
        Trouble2['AVERIAS']='Trouble'

        Trouble2.to_csv('AVERIAS/DT_AVERIAS_Trouble.csv',index=False)

        st.write("SER CARGO CON EXITO Trouble Tickets")

#KeyError: "None of [Index(['codreq', 'fec_regist', 'codedo', 'codctr', 'desnomctr', 'codmotv',\n       'desmotv', 'nomcli', 'desobsordtrab', 'destipvia', 'desnomvia',\n       'numvia', 'destipurb', 'codofcadm', 'desdtt', 'tiptecnologia', 'codtap',\n       'codbor', 'codtrtrn', 'desurb', 'nroplano', 'codnod', 'numtelefvoip',\n       'codpromo', 'tiplinea', 'codcli'],\n      dtype='object')] are in the [columns]"

    except Exception as e:
        print(e)
        Trouble2 = pd.read_csv('AVERIAS/DT_AVERIAS_Trouble.csv',sep=',')
        warnings.simplefilter("ignore")
        df = pd.read_excel(uploaded_file, dtype=str, engine='xlrd')


global numeric_columns
global non_numeric_columns
try:
    st.write(df)
    numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
    non_numeric_columns = list(df.select_dtypes(['object']).columns)
    non_numeric_columns.append(None)
    print(non_numeric_columns)
except Exception as e:
    print(e)
    st.write("Por favor, cargue el archivo en la aplicación.")

## borrar nombres de la pagina
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown(
    """
    <style>

    header .css-1595djx e8zbici2{
    display: flex;
    flex-direction: column;
    align-items: center;
    }

    header .logo-text{
        margin: 0;
        padding: 10px 26px;
        font-weight: bold;
        color: rgb(60, 255, 0);
        font-size: 0.8em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <header class="css-1595djx e8zbici2">
        <p class="logo-text">App Alarmas 👨🏻‍💻Giancarlos .C</p>
    </header>
    """,
    unsafe_allow_html=True
)



