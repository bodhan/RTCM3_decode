import socket
import time
import RTCM3

address = ('192.168.1.113',3000)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)

def byte_to_hex(byte_data):
    hex_data = []
    for byte in byte_data:
        hex_data.append("%02x" % byte)
    return ''.join(hex_data).strip()

rtcm3 = RTCM3.RTCM3()
while True:
    new_data = bytearray(s.recv(4096))
    rtcm3.buffer1 = new_data
    if len(rtcm3.buffer1) and rtcm3.buffer1[0] == 0xD3:
        rtcm3.length = ((rtcm3.buffer1[1] & 0x03) << 8) | rtcm3.buffer1[2]
        rtcm3.msg_id = (rtcm3.buffer1[3] << 4) | ((rtcm3.buffer1[4] & 0xf0) >> 4)

        if(rtcm3.length+8 < len(rtcm3.buffer1)):
            rtcm3.buffer2 = rtcm3.buffer1[6+rtcm3.length:]
            rtcm3.buffer1 = rtcm3.buffer1[:6+rtcm3.length]
            rtcm3.length2 = ((rtcm3.buffer2[1] & 0x03) << 8) | rtcm3.buffer2[2]
            rtcm3.msg_id2 = (rtcm3.buffer2[3] << 4) | ((rtcm3.buffer2[4] & 0xf0) >> 4)
        else:
            rtcm3.length2 = 0
            rtcm3.msg_id2 = 0
        print ""
        print "data_len:" + str(len(new_data))
        print "buffer_len:" + str(len(rtcm3.buffer1))

        print byte_to_hex(rtcm3.buffer1)
        print str(rtcm3.msg_id) + '(' + str(rtcm3.length) + ')'
        print ''
#        if rtcm3.msg_id2 != 0:
#            print byte_to_hex(rtcm3.buffer2)
#            print str(rtcm3.msg_id2) + '(' + str(rtcm3.length2) + ')'
#            print ''

        if(len(rtcm3.buffer1) == rtcm3.length + 6):
            rtcm3.decode(rtcm3.buffer1, rtcm3.length, rtcm3.msg_id)
        else:
            print "msg length error"
        if rtcm3.msg_id2 != 0 and rtcm3.buffer2[0] == 0xD3:
            #rtcm3.decode(rtcm3.buffer2, rtcm3.length2, rtcm3.msg_id2)
            pass

    rtcm3.buffer1 = bytearray('')
    rtcm3.buffer2 = bytearray('')
    rtcm3.length = 0
    rtcm3.length2 = 0
    rtcm3.msg_id = 0
    rtcm3.msg_id2 = 0
    time.sleep(0.1)

s.close()
