#!/bin/bash
cd $OPENSHIFT_DEPLOYMENTS_DIR/201*/repo/sh
./zhidao_auto_pull.sh &
./zhidao_tar_files.sh &
