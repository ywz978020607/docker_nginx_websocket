from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import json

id_clients = {}
clients_id = {}
class SimpleChat(WebSocket):
    def handleMessage(self):
        print("handleMessage self.data", self.data)
        recv_dict = json.loads(self.data)
        if "id" in recv_dict and not recv_dict["id"] in id_clients:
            id_clients[str(recv_dict["id"])] = self
            clients_id[self] = str(recv_dict["id"])
        if recv_dict.get("toid", ""):
            client = id_clients.get(str(recv_dict["toid"]), None)
            if client:
                client.sendMessage(recv_dict.get("msg", 'null'))

    def handleConnected(self):
        print(self.address, 'connected')
        # for client in clients_id:
        #     client.sendMessage(self.address[0] + u' - connected')
        # clients.append(self)

    def handleClose(self):
        #  clients.remove(self)
        id_clients.pop(clients_id[self])
        clients_id.pop(self)
        print(self.address, 'closed')
        for client in clients_id:
            client.sendMessage(self.address[0] + u' - disconnected')

# server = SimpleWebSocketServer('', 8000, SimpleChat)
server = SimpleWebSocketServer('0.0.0.0', 8000, SimpleChat)
server.serveforever()