#!/bin/bash
spider_name="tmall_fp_product"
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
