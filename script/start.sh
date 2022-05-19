#!/bin/sh

python3 /workdir/src/test_pipeline.py

cd ~/..

mkdir -p /opt/ml/model/
cp -r /workdir/result/ /opt/ml/model/