from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
import time

class MyServer(SimpleXMLRPCServer):

    def serve_forever(self):
        self.quit = 0
        while not self.quit:
            self.handle_request()


            
class RPC():
    
    def __init__(self):
        self.server = None
        self.client = None
        self.SEND_THRESHOLD = 10 # [s] adjust to 
        pass
    
    def kill(self):
        self.server.quit = 1
        return 1
    
    def stop_server(self): # may be grouped with kill()
        
        print(f"Server type {type(self.server)}")
        self.kill()
        print(f"Server type {type(self.server)}")
        self.server = None
        print(f"Server type {type(self.server)}")
    
    def start_server(self, node_ip='localhost', rpc_port=8000):
        if self.server == None:
            self.server = MyServer((node_ip, rpc_port))
            self.server.register_function(self.kill)
            self.server.register_function(self.stop_server)
            self.server.register_function(self.test)

            self.server.serve_forever()
            
    def ask_node(node_ip='localhost', rpc_port=9900, function='reverse', arguments='arg'):
        t_init = time.time()
        while (time.time() - t_init) < self.SEND_THRESHOLD: # may need to adjust the theshold!
            try:
                # Create the proxy in a nice way so it gets closed when we are done.
                adress = 'http://'+node_ip+':'+str(rpc_port)
                print(adress)
                with ServerProxy(adress) as proxy:
                    # Get the indicated remote function.
                    remote_function = getattr(proxy, function)
                    # Print the result of executing the remote function.
                    arguments = 1
                    print(f"Arguments {arguments} of type {type(arguments)}.")
                    print(remote_function(arguments))
                    break
            except OSError as e:
                print(e)
            time.sleep(1)
            
            
    def test(self, msg):
        print(f"test with message: {msg}")
        time.sleep(4)
        print(time.time())
        
        
        
if __name__ == '__main__': # to test the server
    rpc = RPC()
    rpc.start_server()