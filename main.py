from multiprocessing import Process
from start_and_admin import start_run as st
from send_to_channel import channel_run as ch
from reg import register_run as regs
from stock import stock_run as sto
from anonsurf_handler import start_anonsurf , stop_anonsurf

if __name__ == '__main__':
    p0 = Process(target=start_anonsurf(password))
    p1 = Process(target=st)
    p2 = Process(target=ch)
    p3 = Process(target=regs)
    p4 = Process(target=sto)

    p0.start()
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    
    p0.join()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
