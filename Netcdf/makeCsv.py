from datetime import datetime, timedelta
import pandas as df
from netCDF4 import Dataset
from NewBBOX import NewBBOX as ne
import numpy as np
from pandas import concat
import re
import os
import tarfile
import gzip
import shutil
import tempfile
import sys
import configparser
from time import time


def conver1D(array):
    """
    Function to convert an array to a list

    :param array: array with the data
    :type array = matrix float32
    :return : list with the data
    :return type: list float32
    """
    l = array.shape
    total = np.zeros((0, l[1] * l[2]), dtype=np.float32)
    i = 0
    for i in range(24):
        tempData = array[i]
        array1D = []
        for x in tempData:
            for s in x:
                array1D.append(s)
        total = np.insert(total, i, array1D, axis=0)
    return total




def makeDates(date):
    """
    Function to create a list with the format year-month-day hours:minutes:seconds

    from 00 hours to 23 hours
    :param date : initial date
    :param type : string
    :return : list with the dates
    :return type : list datatime
    """
    listDates = []
    date = date + ' 00:00:00'
    d = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    listDates.append(d)
    for x in range(23):
        d = d + timedelta(hours=1)
        listDates.append(d)
    allData = df.DataFrame(listDates, columns=['fecha'])
    return allData


def nameColumns(name, numbColumns):
    """
    Function to create list with the name of the columns

    from the variables
    :param name : Variable name
    :param type : string
    :param numbColumns : Number of columns
    :param type: int
    :return : list with the name of the columns
    :return type: list string
    """
    namesColumns = []
    for i in range(numbColumns):
        nColumn = name + '_' + str(i)
        namesColumns.append(nColumn)
    return namesColumns


def makeCsv(net, date, opt, path, minlat, maxlat, minlon, maxlon, variables, estaciones):
    """
    Function to create .csv files of some variables that are in a NetCDF file,

    the .cvs file is saved in the data/NetCDF path of the project
    :param net : NetCDF file information
    :param type: NetCDF type
    :param date: initial date
    :param type: string
    """

    # data_lon = Dataset('/ServerData/KRAKEN/Reanalisis/a1979/wrfout_c15d_d01_1979-08-15_00:00:00.1979')
    # LON = data_lon.variables['XLONG'][:]
    # LAT = data_lon.variables['XLAT'][:]
    #
    # LON = LON[0][0]
    # LAT = LAT[0]
    #
    # LONsize = len(LON)
    # LATsize = len(LAT)
    #
    # celda = []
    var_cut = []
    for i in variables:
        var = net.variables[i][:,int(minlat):int(maxlat),int(minlon):int(maxlon)]
        #print(LON)
        #print(var)
        #return
        # celda.append(var)
        # result = ne(var, LON, LAT, LONsize, LATsize, minlat, maxlat, minlon, maxlon)
        var_cut.append(var)

    for ls in range(len(var_cut)):
        saveData(var_cut[ls], variables[ls], date, opt, path, estaciones)



def getInfo(dir, minlat, maxlat, minlon, maxlon):
    """
    Function to create .csv files of some variables that are in a NetCDF file,

    the .cvs file is saved in the data/NetCDF path of the project
    :param net : NetCDF file information
    :param type: NetCDF type
    :param date: initial date
    :param type: string
    """

    data_lon = Dataset(dir+'a1979/salidas/wrfout_c15d_d01_1979-12-28_00:00:00.a1979')
    LON = data_lon.variables['XLONG'][:]
    LAT = data_lon.variables['XLAT'][:]

    LON = LON[0][0]
    LAT = LAT[0]

    LONsize = len(LON)
    LATsize = len(LAT)
    celda = []
    var_cut = []
    result = ne(LON, LAT, LONsize, LATsize, minlat, maxlat, minlon, maxlon)

    return result


def saveData(var, variables, date, opt, path, estaciones):
    """
    function to save the information in a .csv file

    :param var: information of NetCDF
    :type var: NetCDF
    :param variables: meteorological variables
    :type variables: String
    :param date: date of day
    :type date: date
    :param opt: option to save file
    :type opt: int
    :param path: address where it is saved in .cvs file
    :type path: String
    """
    dateVal = makeDates(date)
    allData = makeDates(date)
    temp = conver1D(var);
    #temp = divData(var, numRow, numColumns)
    dataMatrix = temp
    name = variables + '_' +estaciones + '_' + date +'.csv'
    myIndex = nameColumns(variables, len(temp[0]))
    tempFrame = df.DataFrame(dataMatrix, columns=myIndex)
    allData = concat([allData, tempFrame], axis=1)
    allData = allData.fillna(value=0)
    meanAllData = allData.mean(axis=1)
    meanValues = meanAllData.as_matrix()
    mean = df.DataFrame(meanValues, columns=[variables + '_mean'])
    dateVal[variables + '_mean'] = mean
    if opt == 0:
        allData.to_csv(path + name, encoding='utf-8', index=False)
    elif opt == 1:
        filq = path + name
        dateVal.to_csv(filq, encoding='utf-8', index=False)
    elif opt == 2:
        filq = path + name
        allData.to_csv(filq, encoding='utf-8', index=False)


def readCsv(variables, path, pathCsv, estacion):
    """
    function to join the information of the variables in a single file

    :param variables : netCDF4 file name
    :type variables: string
    :param path: address where it is saved in .cvs file
    :type path: String
    :param pathCsv: address of csv files
    :type pathCsv: String
    """
    # os.makedirs('../data/totalData/')
    dataVa = df.DataFrame()
    variables = variables
    mypath = path
    patron = re.compile(variables + '_'+estacion+'_\d\d\d\d-\d\d-\d\d' + '.*')
    for base, dirs, filess in os.walk(mypath, topdown=False):
        filess = sorted(filess)
        for value in filess:
            if patron.match(value) != None:
                tempData = df.read_csv(mypath + value)
                #tempData = completeMet(tempData)
                tempData = tempData.iloc[0:24, :]
                dataVa = concat([tempData, dataVa], axis=0)
    dataVa = dataVa.reset_index()
    dataVa = dataVa.drop(labels='index', axis=1)
    dataVa.to_csv(pathCsv + variables + '_'+ estacion +'_total.csv', encoding='utf-8', index=False)
    dataVa = df.DataFrame()



def open_netcdf(ls, nameFile, cadena, pathCopyData):
    """
    Function to open a NetCDF file

    :param ls: address file
    :type ls: String
    :param nameFile: file name
    :type nameFile: String
    :param cadena: name of the file without extension
    :type cadena: String
    :param pathCopyData: address to copy the file
    :type pathCopyData: String
    :return : data in NetCDF
    :type return: NetCDF
    """
    name = '.nc.tar.gz'
    name1 = '.nc.gz'
    patron = re.compile('.*' + name)
    patron2 = re.compile('.*' + name1)
    fname = pathCopyData + nameFile
    if patron.match(nameFile) != None:
        comp = tarfile.open(ls, 'r')
        comp.extract(cadena, pathCopyData)
        comp.close()
        data = Dataset(pathCopyData + cadena)
        os.remove(pathCopyData + cadena)
    elif patron2.match(nameFile) != None:
        shutil.copy(ls, fname)
        infile = gzip.open(fname, 'rb')
        tmp = tempfile.NamedTemporaryFile(delete=False)
        shutil.copyfileobj(infile, tmp)
        infile.close()
        tmp.close()
        data = Dataset(tmp.name)
        os.unlink(tmp.name)
        os.remove(fname)
    else:
        data = Dataset(ls)
    # os.remove(fname);
    return data


def readFiles(opt, path, pathCopyData,minlat, maxlat, minlon, maxlon , variables, estaciones):
    """
    Function to read all NetCDF files that are in the specified path
    and named by the format Dom1_year-month-day.nc

    :param opt: option to save data
    :return opt: int
    :param path: address file
    :return path: String
    :param pathCopyData: address to copy the file
    :type pathCopyData: String
    """
    date = '\d\d\d\d-\d\d-\d\d'
    dirr = pathCopyData
    patron2 = re.compile(date)
    print(dirr + 'tfile.txt')
    tempfile = df.read_csv(dirr + 'tfile.txt')
    tempbase = df.read_csv(dirr + 'tbase.txt')
    tfile = list(tempfile.values.flatten())
    tbase = list(tempbase.values.flatten())
    tfileCopy = list(tempfile.values.flatten())
    tbaseCopy = list(tempbase.values.flatten())
    l = len(tfile)
    for i in range(l):
        tfil = tfile[i]
        tbas = tbase[i]
        ls = tbas + '/' + tfil
        f = patron2.findall(tfil)
        cadena = clearString(tfil)
        print(cadena)
        try:
            #net = open_netcdf(ls, tfil, cadena, pathCopyData)
            net = Dataset(ls)
            for xs in range(len(estaciones)):
                minlat1 = minlat[xs]
                maxlat1 = maxlat[xs]
                minlon1 = minlon[xs]
                maxlon1 = maxlon[xs]
                estacion = estaciones[xs]
                #checkFile(net, tfil, f[0], opt, path, minlat1, maxlat1, minlon1, maxlon1, variables, estacion)
                var_cut = []
                for i in variables:
                    var = net.variables[i][:,int(minlat1):int(maxlat1),int(minlon1):int(maxlon1)]
                    #print(LON)
                    #print(var)
                    #return
                    # celda.append(var)
                    # result = ne(var, LON, LAT, LONsize, LATsize, minlat, maxlat, minlon, maxlon)
                    var_cut.append(var)

                for ls in range(len(var_cut)):
                    saveData(var_cut[ls], variables[ls], f[0], opt, path, estacion)
            tfileCopy.remove(tfil)
            tbaseCopy.remove(tbas)
        except (OSError, EOFError) as e:
            print(e)
            fdata = df.DataFrame(tfileCopy, columns=['nameFile'])
            fbas = df.DataFrame(tbaseCopy, columns=['nameBase'])
            fdata.to_csv(dirr + 'tfile.txt', encoding='utf-8', index=False)
            fbas.to_csv(dirr + 'tbase.txt', encoding='utf-8', index=False)
            if os.path.exists(pathCopyData + cadena):
                os.remove(pathCopyData + cadena)
            sys.exit()
            # readFiles(1);
        except tarfile.ReadError:
            print('error2')
            # fdata = df.DataFrame(tfile,columns=['nameFile']);
            # fbas = df.DataFrame(tbase,columns=['nameBase']);
            # fdata.to_csv(dirr+'tfile.txt',encoding='utf-8',index=False);
            # fbas.to_csv(dirr+'tbase.txt',encoding='utf-8',index=False);
            # readFiles(1);
        except (KeyError, FileNotFoundError):
            print('ERROR DE LECTURA')


def totalFiles(pathCopyData, pathNetCDF, dateInit, dateFinal):
    """
    Function to save the address of the netCDF in a txt file

    :param pathCopyData: address to copy the file
    :type pathCopyData: String
    :param pathNetCDF: address where the net files are located
    :type pathNetCDF: String
    """
    dateInit = datetime.strptime(dateInit, '%Y-%m-%d')
    dateFinal = datetime.strptime(dateFinal, '%Y-%m-%d')
    dirr = pathCopyData
    dirr2 = pathNetCDF
    #name = 'wrfout_c1h_d01_\d\d\d\d-\d\d-\d\d_00:00:00.\d\d\d\d.nc'
    name = 'wrfout_c1h_d01_\d\d\d\d-\d\d-\d\d_00:00:00.a\d\d\d\d'
    date = '\d\d\d\d-\d\d-\d\d'
    fil = []
    ba = []
    patron2 = re.compile(date)
    patron = re.compile(name + '.*')
    for base, dirs, files in os.walk(dirr2, topdown=True):
        for value in files:
            if patron.match(value) != None:
                f = patron2.findall(value)
                dateNetCDF = datetime.strptime(f[0], '%Y-%m-%d')
                if (dateNetCDF < dateFinal) & (dateNetCDF > dateInit):
                    fil.append(value)
                    ba.append(base)
    fdata = df.DataFrame(fil, columns=['nameFile'])
    fbase = df.DataFrame(ba, columns=['nameBase'])
    fdata.to_csv(dirr + 'tfile.txt', encoding='utf-8', index=False)
    fbase.to_csv(dirr + 'tbase.txt', encoding='utf-8', index=False)


def clearString(name):
    """
    function to remove the extension of a file

    :param name: file name
    :type name: String
    :return: name file witout extension
    :return type: String
    """
    if name.find(".tar") != 0:
        name = name.replace(".tar", "")

    if name.find(".gz") != 0:
        name = name.replace(".gz", "")
    return name


def checkFile(net, name, date, opt, path, minlat, maxlat, minlon, maxlon, variables,estaciones):
    """
    Function to check if the file has
    the requiered parameters.

    :param net : information that contains the file
    :type net: Dataset
    :param name: file name
    :type name : string
    :param date: date
    :type date: string
    :param opt: option
    :type opt: int
    """
    try:
        #net.variables['XLONG'][:]
        #net.variables['XLAT'][:]
        #print(net.variables['XLAT'][:])
        makeCsv(net, date, opt, path, minlat, maxlat, minlon, maxlon, variables, estaciones)
    except KeyError:
        print('error in file: ' + name)


#if not os.path.exists('data/NetCDF'):
#    os.makedirs('data/NetCDF')
#if not os.path.exists('data/totalData'):
#    os.makedirs('data/totalData')
def create_name(lat ,lon):
    names = []
    for xs in range(len(lat)):
        name = str(lat[xs]) + '_' + str(lon[xs])
        names.append(name)
    return names


def getMaxMin(dir, lat, lon):
    minlat = []
    maxlat = []
    minlon = []
    maxlon = []
    for xs in range(len(lat)):
        info = getInfo(dir, float(lat[xs]), float(lat[xs]), float(lon[xs]), float(lon[xs]))
        minlat.append(info[0])
        maxlat.append(info[1])
        minlon.append(info[2])
        maxlon.append(info[3])
    return [minlat,maxlat,minlon,maxlon]




def init():
    mode = str(sys.argv[1])
    config = configparser.ConfigParser()
    config.read('confMakeCsv.conf')
    path = config.get('makeCsv', 'path')
    pathCsv = config.get('makeCsv', 'pathCsv')
    pathCopyData = config.get('makeCsv', 'pathCopyData')
    pathNetCDF = config.get('makeCsv', 'pathNetCDF')
    lat = config.get('makeCsv', 'lat')
    lon = config.get('makeCsv', 'lon')
    dateInit = config.get('makeCsv', 'dateInit')
    dateFinal = config.get('makeCsv', 'dateFinal')
    variables = config.get('makeCsv', 'variables')
    lat = lat.split()
    lon = lon.split()
    #mode = config.get('makeCsv', 'mode')
    variables = variables.split()
    ml = getMaxMin(pathNetCDF,lat,lon)
    minlat = ml[0]
    maxlat = ml[1]
    minlon = ml[2]
    maxlon = ml[3]
    estaciones = create_name(lat,lon)
    if not os.path.exists(path):
       os.makedirs(path)
    if not os.path.exists(pathCsv):
       os.makedirs(pathCsv)
    if mode == 'S':
        print('save')
        totalFiles(pathCopyData, pathNetCDF, dateInit, dateFinal)
    elif mode == 'P':
        print('procesamiento')
        readFiles(2, path, pathCopyData, minlat, maxlat, minlon, maxlon, variables, estaciones)
        for i in variables:
            print(i)
            for xs in estaciones:
                readCsv(i, path, pathCsv,xs)

init()
