"""
You can run this file to start the control server.

Author:
    Yu-Ren Liu
"""

import threading
import socket
from zoosrv.components.receive import receive
from zoosrv.components.tool_function import ToolFunction
import copy


class ControlServer:
    """
    Control server is responsible for managing all evaluation servers.
    """
    def __init__(self, ip, port):
        """
        Initialization.

        :param ip: ip address of the control server, e.g., "127.0.0.1"
        :param port:
            ports occupied by the control server, it's a list having four elements, e.g., [10000, 10001, 10002, 10003]
            respectively are occupied by function receive_from_evaluation_server, send_to_client and receive_from_client, restart_evaluation_server
        """
        self.ip = ip
        self.port = port
        # for example, elements are ["192.168.1.101:5555", "192.168.1.102:10000"]
        self.evaluation_server = []

    def start(self):
        """
        Start this control server.
        :return: no return
        """
        lock = threading.RLock()
        # start threads
        worker = []
        worker.append(threading.Thread(target=self.communication))
        for t in worker:
            t.setDaemon(True)
            t.start()
        # start main thread
        while True:
            cmd = int(raw_input("[zoojl] Please input command sequence number, 1: print evaluation servers, 2: "
                                "shut down evaluation servers, 3: exit\n"))
            with lock:
                if cmd == 1:
                    ToolFunction.log("The number of evaluation servers: %s" % len(self.evaluation_server))
                    ToolFunction.log(str(self.evaluation_server))
                elif cmd == 2:
                    self.shut_down_control()
                elif cmd == 3:
                    return

    def communication(self):
        """
        main process
        :return:
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #
        s.bind((self.ip, self.port))
        s.listen(20)
        while True:
            client, address = s.accept()
            cmd = receive(1024, client)
            client.sendall("success#\n")
            # receive from evaluation servers
            if cmd == "evaluation server":
                ip_port = receive(1024, client)
                if ip_port not in self.evaluation_server:
                    self.evaluation_server.append(ip_port)
                    ToolFunction.log("Receive ip_port from evaluation server: " + ip_port)
            # send to client
            elif cmd == "client: require servers":
                require_num = int(receive(1024, client))
                require_num = min(require_num, len(self.evaluation_server))
                msg = ""
                for i in range(require_num):
                    if i == 0:
                        msg += self.evaluation_server[i]
                    else:
                        msg = msg + ' ' + self.evaluation_server[i]
                if require_num == 0:
                    msg += "No available evaluation process"
                msg += '\n'
                self.evaluation_server = self.evaluation_server[require_num:]
                if require_num <= 1:
                    client.sendall('Get %d evaluation process\n' % require_num)
                else:
                    client.sendall('Get %d evaluation processes\n' % require_num)
                client.sendall(msg)
            # receive from client
            elif cmd == "client: return servers":
                data_str = receive(1024, client)
                ToolFunction.log("Receive ip_port from client: " + data_str)
                ip_ports = data_str.split()
                for ip_port in ip_ports:
                    if ip_port not in self.evaluation_server:
                        self.evaluation_server.append(ip_port)
            # exception happens at client. restart evaluation servers
            elif cmd == "client: restart":
                data_str = receive(1024, client)
                ToolFunction.log("Client exception, receive ip_port from client: " + data_str)
                ip_ports = data_str.split()
                for ip_port in ip_ports:
                    if ip_port not in self.evaluation_server:
                        ip, port = ip_port.split(":")
                        port = int(port)
                        addr = (ip, port)
                        s.connect(addr)
                        s.sendall("control server: restart\n")
                        self.evaluation_server.append(ip_port)
            else:
                ToolFunction.log("Command error")

    def shut_down_control(self):
        """
        Shut down evaluation servers.

        :return: no return
        """
        try:
            ToolFunction.log("you can input three different kinds of commands")
            ToolFunction.log("1.all ==> shut down all servers. e.g. all")
            ToolFunction.log("2.ip:ip1 ==> shut down all servers having ip1 as ip. e.g. ip:127.0.0.1")
            ToolFunction.log("3.ip_port: ip1:port1 ip2:port2 ip3:port3 ... ==> shut down specific servers. e.g. ip_port: 127.0.0.1:20000 127.0.0.1:20001")
            msg = raw_input("")
            new_cal_server = copy.deepcopy(self.evaluation_server)
            if msg == "all":
                for ip_port in self.evaluation_server:
                    self.shut_down(ip_port)
                    new_cal_server.remove(ip_port)
            elif msg[:7] == "ip_port":
                ip_ports = msg[9:].split(' ')
                for ip_port in ip_ports:
                    self.shut_down(ip_port)
                    new_cal_server.remove(ip_port)
            elif msg[:2] == "ip":
                ip = msg[3:]
                for ip_port in self.evaluation_server:
                    sip, port = ip_port.split(":")
                    if sip == ip:
                        self.shut_down(ip_port)
                        new_cal_server.remove(ip_port)
            else:
                ToolFunction.log("No such command")
            self.evaluation_server = new_cal_server
        except Exception as e:
            ToolFunction.log("input error", e)

    def shut_down(self, ip_port):
        """
        Shut down one evaluation server, which bounds to ip_port.

        :param ip_port: ip:port of the evaluation server
        :return: no return
        """
        es = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #
        if ip_port not in self.evaluation_server:
            ToolFunction.log("no such ip:port")
            return
        ip, port = ip_port.split(":")
        port = int(port)
        addr = (ip, port)
        es.connect(addr)
        es.sendall("control server: shutdown#")
        result = receive(1024, es)
        if result == "success":
            ToolFunction.log("%s: manage to shut down" % ip_port)
        else:
            ToolFunction.log("fail to shut down")
        es.close()


def start(port):
    """
    Start the control server.

    :param port:
        The port occupied by the control server
    :return: no return
    """
    local_ip = socket.gethostbyname(socket.gethostname())
    ToolFunction.log("Control server ip_port: %s:%s" %(local_ip, port))
    cs = ControlServer(local_ip, port)
    cs.start()
