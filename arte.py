import numpy as np
import streamlit as st
#import plotly_express as px
import pandas as pd

from os import devnull, sep
import xlrd
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
        df.to_csv('AVERIAS/DT_AVERIAS_Trouble.csv',index=False)

        datos = {
            'CONTRATA_TOA__c': ['ANALISIS DE RUIDO PEX','ANOVO','CABECERA','COBRA','COMFICA','CUARENTENA COE','DOMINION','ENERGIA','EZENTIS','FIBRA','GAC-VOIP','INGENIERIA HFC',
                    'LARI','LITEYCA','TRABAJOS PROGRAMADOS','TRANSMISIONES','TRATAMIENTO INTERMITENCIA','TRIAJE HFC','TRATAMIENTO CALL PIN TV-M1'],
            'codctr' : ['485','333','60','15','363','429','335','211','19','209','353','435','245','470','365','210','483','474','434']
        }
        df = pd.DataFrame(datos)
        #print(df)
        datos2 = {
            'Categorization Tier 3': ['Control Remoto'],
            'codmotv' : ['I129']
        }
        df2 = pd.DataFrame(datos2)
        #print(df2)
        Trouble = pd.read_csv('AVERIAS/DT_AVERIAS_Trouble.csv', sep=',', low_memory=False)
        Trouble=Trouble[['Incident Number','CREATION_DATE_CRM__c','Tipo de incidencia padre','CONTRATA_TOA__c','Categorization Tier 3','CUSTOMER_NAME_CRM__c',
        'OBSERVATIONS_CRM__c','STREETTYPE_CRM__c','STREETNAME_CRM__c','STREETNUMBER_CRM__c','SUBUNITTYPE_CRM__c','DEPARTMENT_CRM','DISTRICT_CRM__c',
        'Network Technology__c','LEX_NIL__c','BORNE_NIL__c','TROBA_ TYPE_NIL__c','TAP_STREET_NIL__c','PLANE_OLT_PORT','NODE_HFC_OLT_HOSTNAME',
        'currentVozTelephone_OMS__c','currentVozProduct_OMS__c','currentVozServiceTechnology_OMS__c','currentBafAccessid_OMS__c','CFS_SERVICE_TECHNOLOGY_NIL__c'
        ]]
        #<<------------------------->>
        #comvertir año 1070-01-01 con  FECHA REAL
        Trouble['CREATION_DATE_CRM__c'] = pd.to_datetime(Trouble['CREATION_DATE_CRM__c'], errors='coerce', unit='d', origin='1899-12-30')
        Trouble['CREATION_DATE_CRM__c'] = pd.to_datetime(Trouble.CREATION_DATE_CRM__c, errors = 'coerce').dt.strftime("%Y/%m/%d  %H:%M:%S")
        #concatenated_df=pd.concat([Trouble,cms],ignore_index=True)
        union1 = pd.merge(left=Trouble,right=df, how='left', left_on='CONTRATA_TOA__c', right_on='CONTRATA_TOA__c')
        union2 = pd.merge(left=union1,right=df2, how='left', left_on='Categorization Tier 3', right_on='Categorization Tier 3')
        Trouble2=union2[['Incident Number','CREATION_DATE_CRM__c','Tipo de incidencia padre','codctr','CONTRATA_TOA__c','codmotv','Categorization Tier 3','CUSTOMER_NAME_CRM__c',
        'OBSERVATIONS_CRM__c','STREETTYPE_CRM__c','STREETNAME_CRM__c','STREETNUMBER_CRM__c','SUBUNITTYPE_CRM__c','DEPARTMENT_CRM','DISTRICT_CRM__c',
        'Network Technology__c','LEX_NIL__c','BORNE_NIL__c','TROBA_ TYPE_NIL__c','TAP_STREET_NIL__c','PLANE_OLT_PORT','NODE_HFC_OLT_HOSTNAME',
        'currentVozTelephone_OMS__c','currentVozProduct_OMS__c','currentVozServiceTechnology_OMS__c','currentBafAccessid_OMS__c','CFS_SERVICE_TECHNOLOGY_NIL__c'
        ]]
        Trouble2["CFS_SERVICE_TECHNOLOGY_NIL__c"] = Trouble2["CFS_SERVICE_TECHNOLOGY_NIL__c"].replace({'VOIP':'VOZ','GPON':'DATOS','CATV':'TV','DOCSIS':''}, regex=True)
        Trouble2 = Trouble2.rename(columns={'CFS_SERVICE_TECHNOLOGY_NIL__c':'BORRAR',})
        Trouble2.columns = ['codreq','fec_regist','codedo','codctr','desnomctr','codmotv','desmotv','nomcli','desobsordtrab','destipvia','desnomvia','numvia','destipurb','codofcadm',
        'desdtt','tiptecnologia','codtap','codbor','codtrtrn','desurb','nroplano','codnod','numtelefvoip','codpromo','tiplinea','codcli','BORRAR']
        Trouble2['AVERIAS']='Trouble'

        Trouble2.to_csv('AVERIAS/DT_AVERIAS_Trouble.csv',index=False)

        st.write("SER CARGO CON EXITO Trouble Tickets")


    except Exception as e:
        print(e)
        Trouble2 = pd.read_csv('AVERIAS/DT_AVERIAS_Trouble.csv',sep=',')
        warnings.simplefilter("ignore")
        df = pd.read_excel(uploaded_file, dtype=str, engine='xlrd')

        cms=df[['codreq','fec_regist','codedo','codctr','desnomctr','codmotv','desmotv','nomcli','desobsordtrab','destipvia','desnomvia','numvia','destipurb','codofcadm',
        'desdtt','tiptecnologia','codtap','codbor','codtrtrn','desurb','nroplano','codnod','numtelefvoip','codpromo','tiplinea','codcli'
        ]]
        cms['AVERIAS']='CMS'
        cms['BORRAR']=''
        cms=pd.concat([Trouble2,cms],ignore_index=True)
        #cms.to_csv('borrarrrr.csv',index=False, sep=";")
        #print(cms)
        profesiones=["DECO","TV","SEÑAL","TARJETA","REMOTO","CONTROL","CABLE","CANAL","HD","PIX","VISUA","PANTALL"]
        cond=[cms['desobsordtrab'].str.contains(profesion,case=False).fillna(False) for profesion in profesiones]
        cms['TV']=np.select(cond,profesiones,default = '')
        profesiones=["NAVE","LENT","CORTE","INTER","POTEN","WI","IP","VELOC","NAT","DUO","TRIO","PARAM","TAP","ELECT","LEVAN","EGA","SPEED","ERNET","MASIV",
        "LLEGA","SEÑA","SERVI","MODEM","LUCES","ROUT","CONECT","SRN","DOWN","REPET","NIVEL","RNET","NAEV","NAV","OFFLINE","SATURAC","MODEN",
        "CLIENTE ACTIVO","RECOMIE","RUTINA","TRIAJE","SATUR","SNR","ANULAC","MAISVA","CLEAR","PEX","PAQUET","MASVIA","SIVA","MASVI","AMP","SE TRANS",
        "INFANC","UP","M´DEM","MÓDEM","PORTADO","TOA","NVGA","PUERTO"]
        cond=[cms['desobsordtrab'].str.contains(profesion,case=False).fillna(False) for profesion in profesiones]
        cms['DATOS']=np.select(cond,profesiones,default = '')
        profesiones=["LINEA","VOZ","VOLUMEN","TELEFO","LLAMA","FIJ","LOCU","RECIB","FONO","SALID","VOIP","CASILLA","TLF","REGISTR","REALIZA","LLAMDAS","MUERTA","MUERTO",
        "TONO","MULTIDESTINO","LLMAR","TELF","IDENTIF","RUIDO","ESCUCHA"]
        cond=[cms['desobsordtrab'].str.contains(profesion,case=False).fillna(False) for profesion in profesiones]
        cms['VOZ']=np.select(cond,profesiones,default = '')
        profesiones=["NAT","JUEGO","CAMARA","PUERTO","CAMBIO IP","CAMBIO DE IP","SERVIDOR"]
        cond=[cms['desobsordtrab'].str.contains(profesion,case=False).fillna(False) for profesion in profesiones]
        cms['CAMBIO_IP']=np.select(cond,profesiones,default = '')
        #CAMBIAR todo lo encontrado y poner por puerto
        cms['CAMBIO_IP'] = cms['CAMBIO_IP'].replace(profesiones,'PUERTO')
        #Reordenar para ver TRUE O FALSE
        cms["TV"] = cms["TV"].str.len() != 0
        cms["TV"] = cms["TV"].replace({True:'TV',False:''}, regex=True)
        cms["DATOS"] = cms["DATOS"].str.len() != 0
        cms["DATOS"] = cms["DATOS"].replace({True:'DATOS',False:''}, regex=True)
        cms["VOZ"] = cms["VOZ"].str.len() != 0
        cms["VOZ"] = cms["VOZ"].replace({True:'VOZ',False:''}, regex=True)
        cms["PRIORIDAD"] = cms['TV'] + " " + cms['DATOS'] + " " + cms['VOZ']
        cms["PRIORIDAD"] = cms["PRIORIDAD"].str.lstrip()
        cms["PRIORIDAD"] = cms["PRIORIDAD"].str.rstrip()
        cms["PRIORIDAD"] = cms["PRIORIDAD"].replace({' ':'-'}, regex=True)
        cms["PRIORIDAD"] = cms["PRIORIDAD"].replace({'--':'-'}, regex=True)
        cms[['TV','DATOS','VOZ']] = cms[['TV','DATOS','VOZ']].replace(r'^\s*$', np.nan, regex=True)
        cms['PRIORIDAD_2'] = np.where(cms['TV'].isna(), cms['DATOS'], cms['TV'])
        cms['PRIORIDAD_2'] = np.where(cms['PRIORIDAD_2'].isna(), cms['VOZ'], cms['PRIORIDAD_2'])
        #JUNTAR DE LA COLUMNA AL COSTADO
        cms['PRIORIDAD_2'] = np.where(cms['PRIORIDAD_2'].isna(),
                                cms['BORRAR'],
                                cms['PRIORIDAD_2'])
        cms[['PRIORIDAD','PRIORIDAD_2']] = cms[['PRIORIDAD','PRIORIDAD_2']].replace({'':'OTROS', np.nan:'OTROS'})
        cms.rename(columns={'PRIORIDAD':'Total_Prioridad','PRIORIDAD_2':'Primera_Variable','PORT_ID':'Codigo_Gpon'},inplace=True)


        #convertir columna a numero
        regex = re.compile(r'[^0-9]') # Eliminamos todo lo que no sean números
        cms['codcli']=cms['codcli'].replace(regex, '').fillna(0).astype(int)
        #TODO proceso de union de averias y gponticket
        #print("listo")
        # EXTARER DATOS
        gpontick = pd.read_csv('PLANTA_GPON/Gpon_ticket.csv', sep=',')
        gpontick['SUBSCRIPCION']=gpontick['SUBSCRIPCION'].apply(pd.to_numeric, errors='ignore')
        #print(gpontick)
        #gpontick = pd.read_csv('PLANTA_GPON/Gpon_ticket.csv', sep=',')
        union = pd.merge(left=cms,right=gpontick, how='left', left_on='codcli', right_on='SUBSCRIPCION')
        union['Date'] = pd.to_datetime(union['fec_regist'], errors='coerce')
        union['Date'] = union['Date'].dt.strftime('%B-%d')
        #TODO tabla dinamica
        uu  = pd.pivot_table(union, index=['OLT_ALIAS'], columns=['Date'], aggfunc='size')
        ##################################################################
        #uu.to_csv("EXPORTADO/ticket_averias.csv", sep=';')
        #gpontick = pd.read_csv('EXPORTADO/ticket_averias.csv', sep=';')
        #df1 = uu.iloc[3:-1, : ]
        #aa = gpontick.drop(['Date'], axis=1)
        #añss = (aa.columns)
        #gpontick[añss] = gpontick[añss].fillna(0)
        #gpontick[añss] = gpontick[añss].astype(int)
        tb_olt = pd.read_csv('PLANTA_GPON/Tabla_dinamica_OLT.csv', sep=',')
        #print(tb_olt)
        #tb_olt = pd.read_csv('EXPORTADO/Tabla_dinamica_OLT.csv', sep=',')
        #TODO sumar una tabla dinamica
        gpontick = uu.apply(pd.to_numeric, downcast='signed',errors='ignore')
        gpontick['Total'] = gpontick.sum(axis=1)
        union2 = pd.merge(left=gpontick,right=tb_olt, how='left', left_on='OLT_ALIAS', right_on='OLT_ALIAS')
        #TODO para dividir
        #union2['formula'] = union2.Total / union2.value
        #TODO para color
        #df_style = union2.style.applymap(lambda x: 'color:blue', subset=["OLT_ALIAS"]) \
        #.background_gradient(cmap="coolwarm",axis=None, vmin=0.0039, vmax=0.005, subset=["formula"])
        #df_style
        union = pd.merge(left=union,right=tb_olt, how='left', left_on='OLT_ALIAS', right_on='OLT_ALIAS')
        union = union.rename(columns={'value':'Cliente',})
        union['fec_regist'] = pd.to_datetime(union['fec_regist'], errors='coerce')
        union['Year'] = union['fec_regist'].dt.year
        union['Month'] = union['fec_regist'].dt.month
        union['day'] = union['fec_regist'].dt.day
        union = union.drop(['Date'], axis=1)
        #gpontick=gpontick.drop([0])
        #gpontick.to_csv("EXPORTADO/ticket_averias.csv", sep=';')
        #TODO CRUCE CON OLT
        df = pd.read_excel('NODO/NODO.xlsx')
        #Trouble = pd.read_excel('OLT/OLT.xlsx')
        df = df[['NODO','Descripcion','Nombre OLT']]
        df = df[df['NODO'].notna()]
        df = df.drop_duplicates(subset=['NODO'])
        df = df.groupby(['NODO','Descripcion','Nombre OLT']).agg(NODO_size=('NODO', 'size')).reset_index()
        ###########
        #print(df)
        #print(union)
        union3 = pd.merge(left=union,right=df, how='left', left_on='codnod', right_on='NODO')
        #print(union3)
        union = union3.drop(['NODO','NODO_size'], axis=1)
        union["tiptecnologia"] = union["tiptecnologia"].replace({'FTTH':'GPON'}, regex=True)
        union = union.drop(['BORRAR','Nombre OLT'], axis=1)
        #df_style.to_excel("EXPORTADO/Tabla_dinamica.xlsx", index=False)
        union.to_csv("EXPORTADO/ticket_averias_total_22.csv", index=False, sep=';')
        Trouble = pd.read_excel('NODO/NODO.xlsx')
        #Trouble = pd.read_excel('OLT/OLT.xlsx')
        tbla = pd.read_csv('PLANTA_GPON/Tabla_dinamica_OLT.csv', sep=',')
        tbla.to_csv("EXPORTADO/Tabla_dinamica_OLT.csv", index=False, sep=",")
        tblanodo = pd.merge(left=Trouble,right=tbla, how='left', left_on='Nombre OLT', right_on='OLT_ALIAS')
        tblanodo.to_csv("EXPORTADO/Tabla_Nodo.csv", index=False, sep=',')

        df = pd.read_csv('EXPORTADO/ticket_averias_total_22.csv', sep=';')
        df = df.fillna('')
        #abrir la web googleshett
        gc = gspread.service_account(filename='datacargar-947843f340e2.json')
        sh = gc.open("Gpon_ticket_WEB")
        #  el 0 simbol del numero de hoja en este caso es la primera hoja = 0
        worksheet = sh.get_worksheet(0)
        #borrar datos total y dejar encabezado
        worksheet.resize(rows=1)
        worksheet.resize(rows=30)
        #cargar datos df
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        df = pd.read_csv('EXPORTADO/Tabla_Nodo.csv', sep=',')
        #la carga de los nodos
        df = df.fillna('')
        gc = gspread.service_account(filename='datacargar-947843f340e2.json')
        sh = gc.open("NODO_APP")
        worksheet = sh.get_worksheet(0)
        worksheet.resize(rows=1)
        worksheet.resize(rows=30)
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        #la carga de los OLT TABLA DINAMICA
        df = pd.read_csv('EXPORTADO/Tabla_dinamica_OLT.csv', sep=',')
        df = df.fillna('')
        gc = gspread.service_account(filename='datacargar-947843f340e2.json')
        sh = gc.open("OLT_APP")
        worksheet = sh.get_worksheet(0)
        worksheet.resize(rows=1)
        worksheet.resize(rows=30)
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())

        st.write("SER CARGO CON EXITO CMS AHORA YA PUEDES ACTUALIZAR \n EL EXCEL DE LAS TABLAS DINAMICAS")

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



