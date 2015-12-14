#!/bin/bash
set -e
source activate construct
echo Constructing physical network...
python3 -m physical
echo Constructing extrasynaptic network...
python3 -m extrasyn
echo Constructing metadata...
python3 -m metadata
echo Combining...
python3 -m combine
source deactivate
echo Finished! Output in ./combine/tgt_data 
echo "Don't forget to commit the changes"

