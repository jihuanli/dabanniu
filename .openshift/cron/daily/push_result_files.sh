#!/bin/bash
# This deploy hook gets executed after dependencies are resolved and the
# build hook has been run but before the application has been started back
# up again.  This script gets executed directly, so it could be python, php,
# ruby, etc.
log_file="$OPENSHIFT_DATA_DIR/tar.log"
exec 2>&1 1>> $log_file &
minutes_ago=60
date=$(date +%Y%m%d)
cd $OPENSHIFT_DATA_DIR
#拷贝文件到日期目录下
mkdir $date
find $OPENSHIFT_DATA_DIR -mmin +$minutes_ago -name "*.sql" -type f | xargs -i mv {} $date 
cd $date
#压缩
result_tar_filename="$date.tar.gz"
tar -zcvf $result_tar_filename . 
