import websockets
import asyncio
import json
import threading
import time

class WebSocketClient:
    def __init__(self, server_uri):
        self.server_uri = server_uri
        print("socket client intiated")

    async def connect_to_server(self):
        try:
            async with websockets.connect(self.server_uri) as websocket:
                print("connected");
                await websocket.send('{"name":"John", "age":30, "city":"New York"}');
                time.sleep(3);
                await websocket.send('{"name":"TEST", "age":2, "city":"New"}');
                while True:
                    message = await websocket.recv();
                    
                    #print(f"Received from server: {message}");
                    
                    
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
            await websocket.send(message)



if __name__ == "__main__":
    # WebSocket server host and port
    host = "0.0.0.0"  # Listen on all available network interfaces
    port = 8765  # Replace with your desired port
    server_uri = f"ws://{host}:{port}"


    client = WebSocketClient(server_uri);
    asyncio.run(client.connect_to_server());