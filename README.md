# Viento_Json
Script para la creación de archivos json con la información de las variable U y V que sirven en la creación de rosas de viento

## Primeros pasos
Para obtener la copia del proyecto solo es necesario clonar el proyecto usando la instrucción:

`git clone  https://github.com/grupoioa/viento_Json.git`

### Prerrequisitos

Se requieren las siguientes bibliotecas
* pandas
* netCDF4
* Gzip
* Tarfile

Se recomienda instalar todas las bibliotecas mediante [conda](https://conda.io).

Para crear un ambiente se usa la instrucción:

`conda create --nombreAmbiente`

Ya creado el ambiente se puede cambiar a él usando la instrucción:

`conda activate nombreAmbiente`

dentro del ambiente se instalan la bibliotecas correspondientes.

### pandas:
`conda install -c anaconda pandas`

### netCDF4:
`conda install -c anaconda netcdf4`

### Gzip:
`conda install -c ostrokach gzip`

### Tarfile:
`conda install -c conda-forge tar`


## Probando

Para ejecutar el script hay que ejecutar:

`./make_Json.sh`

Como resultado de la ejecución creará una carpeta por cada punto a extraer en la dirección que se proporcione en el archivo de configuración

## Deployment

Se cuenta con un archivo de configuración de nombre **confMakeCsv.conf**, en dicho archivo se puede modificar la carpeta donde se crearan los archivos JSON, de donde se tomarán los archivos NetCDF, el periodo de donde se extraen los datos de **U** y **V**

## Construido con

* [Python](https://www.python.org/)

## Autores
* **Pablo Camacho Gonzalez** -[GitHub](https://github.com/Pablocg0)
