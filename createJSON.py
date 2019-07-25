import json
import pandas as pd
import configparser
import os
from pandas import concat

def createJson(pathFinalData,pathCsv, pos):
    data_u = pd.read_csv(pathCsv+'U10_'+pos+'_total.csv')
    data_v = pd.read_csv(pathCsv+'V10_'+pos+'_total.csv')
    data_u = data_u.sort_values(['fecha'], ascending=True)
    data_v = data_v.sort_values(['fecha'], ascending=True)
    data_u = data_u.reset_index(drop=True)
    data_v = data_v.reset_index(drop=True)
    data_u = data_u[data_u['fecha']<='2010-12-31 23:00:00']
    data_u = data_u['U10_0']
    U_array = convert(data_u.values)
    data_v = data_v[data_v['fecha']<='2010-12-31 23:00:00']
    data_v = data_v['V10_0']
    V_array = convert(data_v.values)

    result = {
        "U" : U_array,
        "V" : V_array
    }

    with open(pathFinalData+pos+'/'+pos+'.json','w') as file:
        json.dump(result, file)


def createJson_years(pathFinalData,pathCsv,pos):
    data_u_temp = pd.read_csv(pathCsv+'U10_'+pos+'_total.csv')
    data_v_temp = pd.read_csv(pathCsv+'V10_'+pos+'_total.csv')
    for xs in range(1979,2011):
        print(xs)
        if not os.path.exists(pathFinalData+pos+'/anuales/'):
            os.makedirs(pathFinalData+pos+'/anuales/')
        data_u = data_u_temp
        data_v = data_v_temp
        fecha_inicio = str(xs)+'-01-01 00:00:00'
        fecha_fin = str(xs)+'-12-31 23:00:00'
        u_year =  data_u[(data_u['fecha']>=fecha_inicio) & (data_u['fecha']<=fecha_fin)]
        v_year =  data_v[(data_v['fecha']>=fecha_inicio) & (data_v['fecha']<=fecha_fin)]
        u_year = u_year.sort_values(['fecha'], ascending=True)
        v_year = v_year.sort_values(['fecha'], ascending=True)
        u_year = u_year.reset_index(drop=True)
        v_year = v_year.reset_index(drop=True)
        data_u = u_year['U10_0']
        data_v = v_year['V10_0']
        U_array = convert(data_u.values)
        V_array = convert(data_v.values)
        result = {
            "U" : U_array,
            "V" : V_array
            }

        with open(pathFinalData+pos+'/anuales/'+pos+'_'+str(xs)+'.json','w') as file:
            json.dump(result, file)


def script_month(pathFinalData,pathCsv,pos):
    data_u_temp = pd.read_csv(pathCsv+'U10_'+pos+'_total.csv')
    data_v_temp = pd.read_csv(pathCsv+'V10_'+pos+'_total.csv')
    for xs in range(1,13):
        print(xs)
        data_u_total = pd.DataFrame()
        data_v_total = pd.DataFrame()
        for ys in range(1979,2011):
            data_u = data_u_temp
            data_v = data_v_temp
            print(ys)
            str_mes = str(xs)
            fecha_inicio = str(ys)+'-'+str_mes.zfill(2) +'-01 00:00:00'
            fecha_fin = str(ys)+'-'+str_mes.zfill(2) +'-31 23:00:00'
            u_year =  data_u[(data_u['fecha']>=fecha_inicio) & (data_u['fecha']<=fecha_fin)]
            v_year =  data_v[(data_v['fecha']>=fecha_inicio) & (data_v['fecha']<=fecha_fin)]
            u_year = u_year.sort_values(['fecha'], ascending=True)
            v_year = v_year.sort_values(['fecha'], ascending=True)
            u_year = u_year.reset_index(drop=True)
            v_year = v_year.reset_index(drop=True)
            data_u_total = concat([data_u_total, u_year], axis = 0)
            data_v_total = concat([data_v_total, v_year], axis = 0)
        data_u_total = data_u_total.reset_index(drop=True)
        data_v_total = data_v_total.reset_index(drop=True)
        #print(data_v_total)
        data_u = data_u_total['U10_0']
        data_v = data_v_total['V10_0']
        U_array = convert(data_u.values)
        V_array = convert(data_v.values)
        result = {
            "U" : U_array,
            "V" : V_array
            }

        with open(pathFinalData+pos+'/'+pos+'_'+str(xs)+'.json','w') as file:
            json.dump(result, file)



def convert(data):
    data_r = []
    for xs in data:
        data_r.append(xs)
    return data_r



#names = ['total','pos1_total', 'pos2_total', 'pos3_total', 'pos4_total','pos5_total']
#names = ['24.3635819_-95.7584937','19.7265872_-95.2773272','18.5770521_-94.2038343']
#names = ['19.21_-93.00','20.8333_-97.20']
#names = ['20.79786_-97.0327']
#names = ['23.5122_-96.8253', '20.9710_-96.7158', '24.7516_-96.5650', '25.3612_-95.2581', '25.9710_-95.0162', '20.0406_-94.7674']
#names = ['20.0_-96.0', '24.0_-96.0', '28.0_-96.0', '20.0_-92.0', '24.0_-92.0', '28.0_-92.0', '24.0_-88.0', '28.0_-88.0', '20.0_-84.0', '24.0_-84.0', '28.0_-84.0', '20.0_-80.0', '24.0_-80.0', '28.0_-80.0']
# names = ['24.0000_-97.3000', '22.0000_-97.0000', '26.0000_-96.6000', '20.0000_-96.5000', '19.5000_-96.0000', '28.0000_-96.0000', '26.0000_-96.0000', '24.0000_-96.0000', '22.0000_-96.0000', '20.0000_-96.0000', '28.0000_-94.0000', '26.0000_-94.0000', '24.0000_-94.0000', '22.0000_-94.0000', '20.0000_-94.0000', '28.0000_-92.0000', '26.0000_-92.0000', '24.0000_-92.0000', '22.0000_-92.0000', '20.0000_-92.0000','28.0000_-90.0000','26.0000_-90.0000','24.0000_-90.0000','22.0000_-90.0000','30.0000_-88.0000', '28.0000_-88.0000', '26.0000_-88.0000', '24.0000_-88.0000', '22.0000_-88.0000', '18.0000_-88.0000', '30.0000_-86.0000', '28.0000_-86.0000', '26.0000_-86.0000', '24.0000_-86.0000', '22.0000_-86.0000', '20.0000_-86.0000', '18.0000_-86.0000', '30.0000_-84.0000', '28.0000_-84.0000', '26.0000_-84.0000', '24.0000_-84.0000', '20.0000_-84.0000', '18.0000_-84.0000', '26.0000_-82.0000', '24.0000_-82.0000', '22.0000_-82.0000', '20.0000_-82.0000', '18.0000_-82.0000','30.0000_-80.0000', '28.0000_-80.0000', '26.0000_-80.0000', '24.0000_-80.0000', '20.0000_-80.0000', '18.0000_-80.0000']

def create_name(lat ,lon):
    names = []
    for xs in range(len(lat)):
        name = str(lat[xs]) + '_' + str(lon[xs])
        names.append(name)
    return names

#createJson()
#createJson_years()
config = configparser.ConfigParser()
config.read('confMakeCsv.conf')
lat = config.get('makeCsv', 'lat')
lon = config.get('makeCsv', 'lon')
pathData = config.get('makeCsv', 'pathCopyData')
pathCsv = config.get('makeCsv', 'pathCsv')
pathFinalData = config.get('makeCsv', 'pathCopyData')
lat = lat.split()
lon = lon.split()
names = create_name(lat,lon)
for xs in names:
    dirTrain = pathData+xs+'/'
    if not os.path.exists(dirTrain):
        os.makedirs(dirTrain)
    print(xs)
    print('----------------------------')
    script_month(pathFinalData,pathCsv,xs)
    createJson(pathFinalData,pathCsv,xs)
    createJson_years(pathFinalData,pathCsv,xs)
