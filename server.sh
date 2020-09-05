#!/bin/sh
kill -9 `ps -aux|grep rasp_server |grep -v grep|awk '{print $2}'`
rm rasp.out
nohup python3 rasp_server.py >>rasp.out 2>&1 &
