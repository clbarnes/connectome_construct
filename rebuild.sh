#!/bin/bash
set -e
source activate construct
echo Constructing physical network...
python -m physical
echo Constructing extrasynaptic network...
python -m extrasyn
echo Constructing metadata...
python -m metadata
echo Combining...
python -m combine
python -m unittest test/validate_data.py
#source deactivate
echo Finished! Output in ./combine/tgt_data 
echo "Don't forget to commit the changes"

