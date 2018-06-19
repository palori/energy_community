from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
import time

class MyServer(SimpleXMLRPCServer):

    def serve_forever(self):
        self.quit = 0
        while not self.quit:
            self.handle_request()


            
class RPC():
    
    def __init__(self, sys_nodes):
        self.server = None
        self.client = None
        self.SEND_THRESHOLD = 10 # [s] adjust to
        self.sys_nodes = sys_nodes
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
        
    def set_sys_nodes(self, sys_nodes): # do it also when updating the list for all the nodes!!!
        self.sys_nodes = sys_nodes
        
    def new_node(self, node_data):
        sys_nodes_int=[int(n) for n in self.sys_nodes.keys()]
        new_node_id = min(sys_nodes_int)-1
        
        # add data to node_data
        node_data['id'] = new_node_id
        node_data['rpc_port'] = max([v['rpc_port'] for k,v in nodes.items()])+1
        node_data['rpc_status'] = 0
        node_data['id'] =
        
        self.sys_nodes[str(new_node_id)] = node_data
               'rpc_port': 9001,
               'rpc_status':1, #1=master, 0=slave
               'produce':1, #1=yes, 0=no
               'control':1, #1=yes, 0=no
               'publish_ports':{'keep_alive':5001,
                                'measurement':6001
                               }
               #'subscribed_ports':{} #it will fill in when adding to the system
              }
        
        
        
        
        
if __name__ == '__main__': # to test the server
    rpc = RPC()
    rpc.start_server()