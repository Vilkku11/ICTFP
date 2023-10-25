import asyncio
import websockets
import json
from logger import Logger

class WebSocketServer:
    def __init__(self, host: str, port: int, worker = None):
        self.host = host
        self.port = port
        self.server = None
        self.clients = set()

        #ADS-B worker
        self.worker = worker;
        self.logger = Logger("WebSocket");

        self.logger.info("Websocket server initiated");
    
    async def start_server(self):
        self.server = await websockets.serve(self.handle_client, self.host, self.port)

    async def stop_server(self):
        if self.server:
            await self.broadcast("Websocket connection closed");
            self.server.close()

    # On new connections - handle
    async def handle_client(self, websocket, path):
        
        self.logger.info("CLIENT CONNECTION");
        self.clients.add(websocket);

        try:
            async for message in websocket:

                try:
                    json_msg = json.loads(message);
                    self.logger.info(json_msg);

                except TypeError:
                    self.logger.error("Mistyped message: {message}");
                    await websocket.send('{"error": 400}');
                
                


        except websockets.exceptions.ConnectionClosedError:
            pass  # Client disconnected

        finally:
            self.clients.remove(websocket) # remove from set


    async def handle_client_message(self, msg):
        pass


    # Send a message to all connected clients
    async def broadcast(self, message): 
        if self.clients:
            print("clients and msg");
            await asyncio.gather(*[client.send(message) for client in self.clients])

    # Start websocket
    async def run(self):
        await self.start_server()
        self.logger.info(f"WebSocket server started on ws://{self.host}:{self.port}");

        try:
            await self.server.wait_closed()
            self.logger.info(f"WebSocket server stopped on ws://{self.host}:{self.port}");
        
        except websockets.ConnectionClosedError: #connection dropped unexpectedly
            #TODO
            pass


    async def get_adsb_status(self):
        if self.worker:
            self.worker.get_adsb_status();
        else:
            raise TypeError


if __name__ == "__main__":
    # WebSocket server host and port standalone
    host = "0.0.0.0"
    port = 8765

    server = WebSocketServer(host, port);
    asyncio.get_event_loop().run_until_complete(server.run());
    