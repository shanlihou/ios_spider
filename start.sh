#!/bin/sh
kill -9 `ps -aux|grep crawler |grep -v grep|awk '{print $2}'`
rm nohup.out
nohup python3 crawler.py >nohup.out&
