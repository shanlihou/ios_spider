#!/bin/sh
kill -9 `ps -aux|grep watch.py |grep -v grep|awk '{print $2}'`
rm nohup.out
nohup python3 watch.py >>watch.out 2>&1 &
