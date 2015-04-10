#!/bin/bash
spider_name="zhidao"
log_file="$OPENSHIFT_DATA_DIR/$spider_name""_auto_pull.txt"
exec 2>&1 1>> $log_file &
cd $OPENSHIFT_DEPLOYMENTS_DIR/201*/repo/spider/baiduzhidao/baiduzhidao/spiders
PID_CNT=`ps -ef |grep scrapy |grep zhidao |grep -v grep | wc -l`
if [ $PID_CNT != 1 ]; then
#  ps -ef | grep scrapy | grep zhidao |grep -v grep | awk '{print $2}' | xargs -n 1 -r kill -9
  scrapy crawl zhidao >"$OPENSHIFT_DATA_DIR/$spider_name""_log.txt" 2>&1 &
fi
