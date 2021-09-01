import socket
import multiprocessing
import time

# Extend the gui with some new functionality
class UDPServer:   

    def __init__(self, ip="127.0.0.1", port=8080):
        self.ip=ip
        self.port=port
        self.tx_buffer=""
        self.rx_buffer=""
        self.rx_flag=False
        self.Is_running=False

    def set_ip(self,ip):
        self.ip=ip
        pass

    def set_port(self,port):
        self.port=port
        pass

    def set_tx_buffer(self,data):
        self.tx_buffer=data
        pass

    def start_send(self):
        self.proc2 = multiprocessing.Process(target=self.send)
        self.proc2.daemon = True
        self.proc2.start()
        pass  

    def send(self):
        msg=self.tx_buffer
        packet=msg.encode(encoding='UTF-8',errors='strict')
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        sock.sendto(packet, (self.ip, self.port))
        

    def listen(self):
        bufferSize=1024
        UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        UDPServerSocket.bind((self.ip, self.port))
        print("UDP server up and listening" ,self.ip, self.port)
        while True:
            packet=UDPServerSocket.recvfrom(bufferSize)
            self.rx_buffer = packet[0].decode("utf-8")

            self.rx_flag=True
            print("Recieved: ",self.rx_buffer)

    def start_listen(self):
        if self.Is_running:
            self.stop_listen()

        self.proc1 = multiprocessing.Process(target=self.listen)
        self.proc1.daemon = True
        self.proc1.start()
        self.Is_running=True
            

    def stop_listen(self):
        self.proc1.kill()
        self.Is_running=False
        print("UDP Server killed")
        

    def get_rx_buffer(self):
        return self.rx_buffer

if __name__ == "__main__":
    my_server=UDPServer()
    my_server.set_ip("127.0.0.1")
    my_server.set_port(8080)
    my_server.start_listen()
    time.sleep(0.5)
    my_server.set_tx_buffer("Hi Darsh")
    my_server.send()
    print(my_server.get_rx_buffer())
    time.sleep(10)
    my_server.stop_listen()
    pass