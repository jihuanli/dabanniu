#!/bin/bash
git add .
git commit -m "auto"
spider_base_name="spider"
for ((i=1;i<31;i++));do
{
  spider_name=$spider_base_name$i 
  echo "push $spider_name"
  git push $spider_name& 
}
done
