import pymqi
import time
from khayyam import JalaliDatetime as datetime

# export MQSERVER="ServerChannel/TCP/192.168.163.167(1418)"
# sudo -Eu mq LD_LIBRARY_PATH=/usr/lib64 /home/vahid/.virtualenvs/pymqi/bin/python ./isc.py
# sudo -Eu mq LD_LIBRARY_PATH=/usr/lib64 /home/vahid/.virtualenvs/pymqi/bin/python ./is

#
# queue_manager = 'SaptaQueueManager1418'
# channel = 'ServerChannel'
# user = 'mq'
# password = 'mq'
# queue = 'SOTP'

# export MQSERVER="CHANN1/TCP/192.168.1.70(9000)"
queue_manager = 'QMA'
channel = 'CHANN1'
user = 'mqm'
password = 'mqm'
queue = 'QUEUE1'


qm = pymqi.connect(queue_manager, channel=channel, user=user, password=password)
putq = pymqi.Queue(qm, queue)


for i in range(100000):
  msg = '<token-register-bmi unique-id="%sSOTPREGISTER%06d" phone-no="09123456789" source="SOTP-BMI-KAKISH" key="24567" />' % (
    datetime.now().strftime('%Y%m%d%H%M%S'), i
  )
  print(msg)
  putq.put(msg)


