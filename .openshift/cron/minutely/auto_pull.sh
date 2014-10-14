#!/bin/bash
cd $OPENSHIFT_DEPLOYMENTS_DIR/201*/repo/spider/baiduzhidao/baiduzhidao/spiders
PIDS=`ps -ef |grep scrapy |grep -v grep | awk '{print $2}'`
if [ "$PIDS" ]; then
  scrapy crawl zhidao >$OPENSHIFT_DATA_DIR/log.txt 2>&1 &
fi
