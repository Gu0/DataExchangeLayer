#using:utf-8
import socket
import threading

class socketChannelManager():
    '''
    屏蔽底层实现，抽象多个独立的数传通道，进行通道管理；
    '''

    def __init__(self, host='0.0.0.0', port=6666):
        self.client_list = []

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = (host, port)
        self.server_socket.bind(address)
        self.server_socket.listen()

        t = threading.Thread(target=self.forever_accept_client)
        t.start()

    def forever_accept_client(self):
        while True:
            (client_socket, address) = self.server_socket.accept()
            self.client_list.append(client_socket)
            print('[ServerSocket]Accept a new connection:' + str(address))

    def connect(self, remote='127.0.0.1', port=6666):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = (remote, port)
        client_socket.connect(address)
        self.client_list.append(client_socket)
        print('[ClientSocket]Start a new connection:' + str(address))


# A simple test
if __name__ == '__main__':
    import time
    lManager = socketChannelManager(host='127.0.0.1', port=6666)

    rManager = socketChannelManager(host='127.0.0.2', port=5555)

    for i in range(5):
        time.sleep(10)
        rManager.connect(remote='127.0.0.1', port=6666)

        for client in lManager.client_list:
            print(client)
        print('==================================')

    print('over!')
