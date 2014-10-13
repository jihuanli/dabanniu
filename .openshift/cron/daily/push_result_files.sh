#!/bin/bash
# This deploy hook gets executed after dependencies are resolved and the
# build hook has been run but before the application has been started back
# up again.  This script gets executed directly, so it could be python, php,
# ruby, etc.
minutes_ago=60
date=$(date +%Y%m%d)
cd $OPENSHIFT_DATA_DIR
SPIDER_NAME=`cat spider.conf | grep SPIDER_NAME | awk -F'=' '{print $2}'`
#拷贝文件到日期目录下
mkdir $date
find $OPENSHIFT_DATA_DIR -mmin +$minutes_ago -name "*.sql" -type f | xargs -i mv {} $date 
#压缩
result_tar_filename="$date""_"".tar.gz"
tar -zcvf $result_tar_filename . 

#scp
