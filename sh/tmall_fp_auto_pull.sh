#!/bin/bash
spider_name="tmall_fp_product"
log_file="$OPENSHIFT_DATA_DIR/$spider_name""_auto_pull.txt"
exec 2>&1 1>> $log_file &
cd $OPENSHIFT_DEPLOYMENTS_DIR/201*/repo/spider/$spider_name/$spider_name/spiders
PID_CNT=`ps -ef |grep scrapy |grep $spider_name |grep -v grep | wc -l`
if [ $PID_CNT != 1 ]; then
  ps -ef | grep scrapy | grep $spider_name |grep -v grep | awk '{print $2}' | xargs -n 1 -r kill -9
  scrapy crawl $spider_name >"$OPENSHIFT_DATA_DIR/$spider_name""_log.txt" 2>&1 &
fi
