#!/bin/bash
git add .
git commit -m "auto-commit"
git push spider1 &
set spider_base_name = "spider"
for ((i=1;i<31;i++));do
{
  set spider_name = ${spider_base_name}${i} 
  echo $spider_name
  #git push $spider_name 
}
done
