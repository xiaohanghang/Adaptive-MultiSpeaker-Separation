#!/bin/bash
#$ -S /bin/bash
#$ -cwd
#$ -jc nvcr-tensorflow-1712_g1
#$ -e err_pretraining.o
#$ -o std_pretraining.o

export MY_PROXY_URL="http://10.1.10.1:8080/"
export HTTP_PROXY=$MY_PROXY_URL
export HTTPS_PROXY=$MY_PROXY_URL
export FTP_PROXY=$MY_PROXY_URL
export http_proxy=$MY_PROXY_URL 
export https_proxy=$MY_PROXY_URL
export ftp_proxy=$MY_PROXY_URL


. /fefs/opt/dgx/env_set/common_env_set.sh

export PATH="/home/anthony/anaconda2/bin:$PATH"
export LD_LIBRARY_PATH="/home/anthony/anaconda2/lib:$LD_LIBRARY_PATH"
export PATH="/home/anthony/anaconda2/lib:$PATH"
export LIBRARY_PATH="/home/anthony/anaconda2/lib:$LIBRARY_PATH"
export PATH="/home/anthony/.local/bin:$PATH"

python -u -m experiments.pretraining --dataset h5py_files/train-clean-100-8-s.h5 --chunk_size 20480 \
--nb_speakers 4 --epochs 10 --batch_size 16 --learning_rate 0.001 --window_size 1024 --max_pool 512 \
--filters 512 --regularization 0.0001 --beta 0.01 --sparsity 0.01 --overlap_coef 0.001 > overlapping_test512512.txt
