import websockets
import asyncio

class WebSocketClient:
    def __init__(self, server_uri):
        self.server_uri = server_uri

        print("socket client initialized");

    async def connect_to_server(self):
        try:
            async with websockets.connect(self.server_uri) as websocket:
                print("connected");

                #await asyncio.sleep(2);
                #await websocket.send('{"add":[{"id":"vp1","lat":61.5033155,"long":23.807138}]}');

                while True:
                    message = await websocket.recv();
                    
                    print(f"Received from server: {message}");
                    
                    
                    if message == "close":
                        await websocket.send(message);
        
        except websockets.exceptions.ConnectionClosedOK:
            print("Connection closed peacefully")
        
        except websockets.exceptions.ConnectionClosedError:
            print("Connection closed on error")

        except Exception:
            print("Unable to connect to server")      

    async def send_message(self, message):
        async with websockets.connect(self.server_uri) as websocket:
            await websocket.send(message);



if __name__ == "__main__":
    # WebSocket server host and port
    host = "server"  # Websocket server
    port = 8765  # port
    server_uri = f"ws://{host}:{port}"


    client = WebSocketClient(server_uri);
    asyncio.run(client.connect_to_server());