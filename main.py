import asyncio
from scripts.webServer import WebServer

def main():
    def start_asyncio():
        asyncio.set_event_loop(asyncio.new_event_loop())
        asyncio.get_event_loop().run_forever()
    
    WebServer.run()
    start_asyncio()

if __name__ == "__main__":
    main()
