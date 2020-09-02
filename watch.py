import time
import os

cmd_str = "ps -aux|grep 'python3 rasp_server.py'|grep -v 'grep'"

def watch_once():
    with os.popen(cmd_str) as r:
        ret = r.read().strip()
        rets = ret.split()
        if not rets:
            os.system('sh server.sh')

def main():
    while 1:
        watch_once()
        time.sleep(5)

if __name__ == '__main__':
    main()