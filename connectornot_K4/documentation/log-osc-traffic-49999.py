
""" receiving OSC with pyOSC
logs messages received from the android app 'Connect or Not'
(the app sends data on conversation minutes, data packets, sms and signalstrength every 10s)
and writes them to a file log+timestamp.csv
https://trac.v2.nl/wiki/pyOSC
adapted example by www.ixi-audio.net based on pyOSC documentation
"""


import OSC
import time, threading, codecs
from datetime import datetime


f_out=codecs.open("logs/log"+str(int(time.time()))+".csv", "w", encoding="utf-8") 

f_out.write('ID; address; value; timestamp;\n')


# tupple with ip, port. i dont use the () but maybe you want -> send_address = ('127.0.0.1', 9000)
receive_address = '0.0.0.0', 49999


# OSC Server. there are three different types of server. 
s = OSC.OSCServer(receive_address) # basic
##s = OSC.ThreadingOSCServer(receive_address) # threading
##s = OSC.ForkingOSCServer(receive_address) # forking



# this registers a 'default' handler (for unmatched messages), 
# an /'error' handler, an '/info' handler.
# And, if the client supports it, a '/subscribe' & '/unsubscribe' handler
s.addDefaultHandlers()



# define a message-handler function for the server to call.
def all_handler(addr, tags, stuff, source):
    print "received new osc msg from %s" % OSC.getUrlStr(source)
    f_out.write(OSC.getUrlStr(source)+'; ')
    print "with addr : %s" % addr
    f_out.write(addr+'; ')
    print "typetags %s" % tags
    print "data %s" % stuff
    f_out.write(addr+'; ')
    f_out.write(str(stuff[0])+'; ')
    f_out.write(str(time.time())+'; ')
    f_out.write('humanreadable: '+datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S'))
    f_out.write('\n')

    
s.addMsgHandler("/conversation", all_handler) # adding our function
s.addMsgHandler("/data", all_handler) 
s.addMsgHandler("/sms", all_handler) 
s.addMsgHandler("/signal", all_handler) 

# just checking which handlers we have added
print "Registered Callback-functions are :"
for addr in s.getOSCAddressSpace():
    print addr


# Start OSCServer
print "\nStarting OSCServer. Use ctrl-C to quit."
st = threading.Thread( target = s.serve_forever )
st.start()


try :
    while 1 :
        time.sleep(5)

except KeyboardInterrupt :
    print "\nClosing OSCServer."
    s.close()
    print "Waiting for Server-thread to finish"
    st.join() ##!!!
    print "Done"
    f_out.close()
        
