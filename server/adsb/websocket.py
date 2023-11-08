import asyncio
import websockets
from logger import Logger

class WebSocketServer:
    def __init__(self, host: str, port: int, worker = None):
        self.logger = Logger("WebSocket");
        self.logger.info("Websocket server initiated");

        self.host = host;                   #ip
        self.port = port;                   #port
        self.server = None;                 #server
        self.clients = set();               #clients - connections
        self.worker = worker;               #adsb -worker
    
    async def start_server(self):
        self.server = await websockets.serve(self.handle_client, self.host, self.port);

    async def stop_server(self):
        if self.server:
            await self.broadcast("Websocket connection closed");
            self.server.close()

    async def handle_client(self, websocket, path):
        self.logger.info("CLIENT CONNECTION");
        self.clients.add(websocket); # add to set 
        await websocket.send(self.worker.adsb_client.get_client_status()); # responds with adsb-client status on h

        try:
            async for message in websocket:

                try:
                    self.logger.info(message);
                    self.worker.handle_websocket_msg(message);

                except TypeError:
                    self.logger.error("Mistyped message: {message}");
                    await websocket.send('{ "error": 400 }');
                
        except websockets.exceptions.ConnectionClosedError:
            pass  # Client disconnected

        finally:
            self.clients.remove(websocket) # remove from set

    # poll
    async def poll(self, message, time):
        while True:
            await self.broadcast(message)
            await asyncio.sleep(time)

    # Send a message to all connected clients
    async def broadcast(self, message): 
        if self.clients:
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
    