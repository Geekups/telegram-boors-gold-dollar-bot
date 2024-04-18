import anonsurf_handler
import get_dollar_and_gold
import reg
import send_to_channel
import start_and_admin
import stock



def hello_w():
    try:
        anonsurf_handler.start_anonsurf()
        start_and_admin()
        reg()
        stock()
        send_to_channel()
    except:
        return hello_w()
    
if __name__ == "__main__":
    hello_w()



