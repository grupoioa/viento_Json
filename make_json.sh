
#!/bin/bash

export LD_LIBRARY_PATH=/usr/local/cuda/lib64/
source ~/anaconda3/envs/tensorflow/bin/activate tensorflow

python Netcdf/makeCsv.py S
python Netcdf/makeCsv.py P
python createJSON.py
