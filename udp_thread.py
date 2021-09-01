import socket
import threading
import time

# UDP Model
class UDPServer:   

    def __init__(self, ip="127.0.0.1", port=8080):
        self.ip=ip
        self.port=port
        self.tx_buffer=""
        self.rx_buffer=""
        self.rx_flag=False
        self.Is_running=False
        self.send_is_running=False
        self.delay=0
        self.send_ip=0
        self.send_port=0

    def get_flag(self):
        return self.get_flag

    def set_ip(self,ip):
        self.ip=ip
        pass

    def set_port(self,port):
        self.port=port
        pass

    def set_tx_buffer(self,data):
        self.tx_buffer=data
        pass

    def set_send_config(self,ip,port):
        self.send_ip=ip
        self.send_port=port

    def send(self): ### Call this as new procces 
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        while self.send_is_running:
            msg=self.tx_buffer
            packet=msg.encode(encoding='UTF-8',errors='strict')
            sock.sendto(packet, (self.send_ip, self.send_port))
            if self.delay==0:
                break
            time.sleep(self.delay)
            pass
            
    def start_send(self):
        if self.send_is_running==False :
            self.send_is_running=True
            self.thead1 = threading.Thread(target=self.send)
            self.thead1.daemon = True
            self.send_is_running=True
            self.thead1.start()

    def set_send_interval(self,delay):
        self.delay=delay

    def end_send_loop(self):
        if self.send_is_running:
            self.send_is_running=False

    def listen(self):
        bufferSize=1024
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPServerSocket.bind((self.ip, self.port))
        print("UDP server up and listening" ,self.ip, self.port)
        while self.Is_running:
            try:
                packet=self.UDPServerSocket.recvfrom(bufferSize)
                self.rx_buffer = packet[0].decode("utf-8")
                self.rx_flag=True
                print("Recived: ",self.rx_buffer)
            except Exception :
                pass
        self.UDPServerSocket.close()

    def start_listen(self):
        if self.Is_running:
            self.stop_listen()

        self.thead2 =threading.Thread(target=self.listen)
        self.thead2.daemon = True
        self.thead2.start()
        self.Is_running=True
            
    def stop_listen(self):
        if self.Is_running:
            self.Is_running=False
            self.UDPServerSocket.close()
            print("UDP Server Closed")

    def get_rx_buffer(self):
        return self.rx_buffer

if __name__ == "__main__":
    my_server=UDPServer()
    my_server.set_ip("127.0.0.1")
    my_server.set_port(8080)
    my_server.start_listen()
    time.sleep(0.5)
    my_server.set_tx_buffer("Hi Darsh")
    print(my_server.get_rx_buffer())
    time.sleep(0.1)
    my_server.set_send_interval(1)
    my_server.start_send()
    time.sleep(3)
    my_server.end_send_loop()
    time.sleep(5)
    my_server.stop_listen()
    time.sleep(4)
    pass