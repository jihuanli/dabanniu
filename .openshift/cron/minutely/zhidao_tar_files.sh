#!/bin/bash
# This deploy hook gets executed after dependencies are resolved and the
# build hook has been run but before the application has been started back
# up again.  This script gets executed directly, so it could be python, php,
# ruby, etc.
# 每天凌晨0-1点取一个小时前的数据文件生成tar包
spider_name="zhidao"
log_file="$OPENSHIFT_DATA_DIR/$spider_name""_tar.log"
echo $log_file
exec 2>&1 1>> $log_file &
minutes_ago=60
#时差12个小时
date_scp="$(date +%Y%m%d)12"
date_h=$(date +%Y%m%d%H)
date=$(date +%Y%m%d)
dest_dir="$OPENSHIFT_DATA_DIR/$spider_name"
result_tar_filename="$date.tar.gz"

if [ $date_h -eq $date_scp ];then
  cd $dest_dir
  #拷贝文件到日期目录下
  if [ ! -d $date ];then
    mkdir $date
  fi
  find $dest_dir -maxdepth 1 -mmin +$minutes_ago -name "*.sql" -type f | xargs -i mv {} $date 
  cd $date
  if [ ! -f "$result_tar_filename" ];then
    echo "=========start build tar file: $date============="
    #压缩
    tar -zcvf $result_tar_filename *.sql 
    md5sum $result_tar_filename > "$result_tar_filename.md5"
    echo "=========finish build tar file: $result_tar_filename============="
  fi
fi
