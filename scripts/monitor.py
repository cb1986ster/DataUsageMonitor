from UsageView.models import AppUsageLog
import time
import os,sys
import threading
from subprocess import Popen, PIPE
import setproctitle
import re

data = {}
is_running = False

def nethogs_reader(interval):
    global data
    global is_running
    in_read = False
    try:
        with Popen(["nethogs", "-td {}".format(interval)], stdout=PIPE, stderr=PIPE) as p:
            for line in p.stdout:
                if not is_running:
                    p.kill()
                    p.wait()
                    return True
                line = line.decode('utf-8')
                if line.startswith('unknown TCP/'): in_read = False
                if in_read:
                    elements = line.strip().split()
                    (proc,tx,rx) = elements[0] , elements[-2], elements[-1]
                    tx = float(tx)
                    rx = float(rx)
                    if proc[0] == '/':
                        if re.match('^.*/\d+/\d+$',proc):
                            proc = proc.split('/')[-3]
                        else:
                            proc = proc.split('/')[-1]
                        if proc in data.keys():
                            data[proc]['tx'] += tx
                            data[proc]['rx'] += rx
                        else:
                            data[proc] = {'rx': rx, 'tx': tx}
                if line.startswith('Refreshing:'): in_read = True
    except Exception as e:
        print(line,e)
        is_running = False
    except KeyboardInterrupt:
        is_running = False
    return False
def saver(interval):
    global data
    global is_running
    try:
        while is_running:
            time.sleep(interval)
            for proc in data:
                AppUsageLog.objects.create(
                    app=proc,
                    tx=int(data[proc]['tx']*1024),
                    rx=int(data[proc]['rx']*1024)
                )
            data = {}
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        is_running = False

def check_root():
    if os.geteuid() != 0:
        print('Run this as root!')
        sys.exit(1)

def main():
    nethogs_reader_th = threading.Thread(target=nethogs_reader,args=(1,))
    nethogs_reader_th.start()
    saver(60)
    nethogs_reader_th.join()

def run():
    check_root()
    setproctitle.setproctitle('data_usage_monitor')
    global is_running
    while 1:
        is_running = True
        main()
        time.sleep(1)
