#!/bin/bash
log_file="$OPENSHIFT_DATA_DIR/auto_pull.txt"
exec 2>&1 1>> $log_file
cd $OPENSHIFT_DEPLOYMENTS_DIR/201*/repo/spider/baiduzhidao/baiduzhidao/spiders
PIDS=`ps -ef |grep scrapy |grep -v grep | awk '{print $2}'`
if [ "$PIDS" ]; then
  scrapy crawl zhidao
fi