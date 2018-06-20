from xmlrpc.server import SimpleXMLRPCServer
#from xmlrpc.server import SimpleThreadedXMLRPCServer
from xmlrpc.client import ServerProxy
import time
import json
import threading

class MyServer(SimpleXMLRPCServer):

    def serve_forever(self):#, infinite=False, time_period=10):
        #time_period [s] to wait
        self.quit = 0
        print('Start server')
        #while not self.quit:
        print('Waiting for new node...')
        self.handle_request()
        time.sleep(1)
        if self.quit==1:
            print('Closing server...')

class ServerThread(threading.Thread):
    def __init__(self, node_ip, rpc_port, sys_nodes):
        threading.Thread.__init__(self)
        #self.localServer = SimpleThreadedXMLRPCServer((node_ip, rpc_port))
        self.localServer = SimpleXMLRPCServer((node_ip, rpc_port))
        self.localServer.register_function(self.new_node) #just return a string
        self.localServer.register_function(self.set_sys_nodes)
        self.sys_nodes = sys_nodes

    def run(self):
         self.localServer.serve_forever()

    def set_sys_nodes(self, sys_nodes):
        self.sys_nodes = sys_nodes

    def new_node(self, node_data):
        node_data = json.loads(node_data)
        print('Adding node to the system')
        sys_nodes_int=[int(n) for n in self.sys_nodes.keys()]
        new_node_id = min(sys_nodes_int)-1
        
        # add data to node_data
        node_data['id'] = new_node_id
        node_data['rpc_port'] = max([v['rpc_port'] for k,v in self.sys_nodes.items()])+1
        node_data['master_id'] = max(sys_nodes_int)
        pub_ports_ka = [v['publish_ports']['keep_alive'] for k,v in self.sys_nodes.items()]
        pub_ports_m = [v['publish_ports']['measurement'] for k,v in self.sys_nodes.items()]
        node_data['publish_ports'] = {'keep_alive': max(pub_ports_ka)+1,
                                      'measurement': max(pub_ports_m)+1
                                     }
        # add new node_data to syst_nodes
        self.sys_nodes[str(new_node_id)] = node_data
        # Return the node_id for the newcomer and the sys_nodes dict.
        
        # To stop the server
        self.quit = 1

        return str(new_node_id)+';'+json.dumps(self.sys_nodes, ensure_ascii=False)
        
            
class RPC():
    
    def __init__(self):
        self.server = None
        self.client = None
        self.SEND_THRESHOLD = 60 # [s] adjust to
        self.sys_nodes = {}
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
    
    def start_server(self, node_ip='localhost', rpc_port=8000): #, infinite=False, time_period=10):
        if self.server == None:
            self.server = SimpleXMLRPCServer((node_ip, rpc_port))
            #self.server = MyServer((node_ip, rpc_port)

            self.server.register_function(self.kill)
            self.server.register_function(self.stop_server)
            self.server.register_function(self.test)
            self.server.register_function(self.new_node, 'new_node')
            
            self.server.serve_forever()#infinite=False, time_period=10)
            #self.server.handle_request()

    def start_server_thread(self, node_ip='localhost', rpc_port=8000):
        self.server = ServerThread(node_ip, rpc_port, self.sys_nodes)
        self.server.start()
        print('RCP Server running but we can continue')


    def ask_node(self, node_ip='localhost', rpc_port=8000,
        function='reverse', arguments='arg'):
        t_init = time.time()
        while time.time() - t_init < 3:
        #while (time.time() - t_init) < self.SEND_THRESHOLD: # may need to adjust the theshold!
            try:
                # Create the proxy in a nice way so it gets closed when we are done.
                adress = 'http://'+node_ip+':'+str(rpc_port)
                print(adress)
                with ServerProxy(adress) as proxy:
                    # Get the indicated remote function.
                    remote_function = getattr(proxy, function)
                    # Print the result of executing the remote function.
                    #print(f"Arguments {arguments} of type {type(arguments)}.")
                    #print(remote_function(arguments))
                    response = proxy.new_node(arguments)
                    node_id, sys_nodes = response.split(';')
                    self.sys_nodes = json.loads(sys_nodes)
                    return response
            except OSError as e:
                print(e)
            time.sleep(0.2)
        return None
            
    def test(self, msg):
        print(f"test with message: {msg}")
        time.sleep(4)
        print(time.time())
        
    def set_sys_nodes(self, sys_nodes): # do it also when updating the list for all the nodes!!!
        self.sys_nodes = sys_nodes
        
    def new_node(self, node_data):
        node_data = json.loads(node_data)
        print('Adding node to the system')
        sys_nodes_int=[int(n) for n in self.sys_nodes.keys()]
        new_node_id = min(sys_nodes_int)-1
        
        # add data to node_data
        node_data['id'] = new_node_id
        node_data['rpc_port'] = max([v['rpc_port'] for k,v in self.sys_nodes.items()])+1
        node_data['master_id'] = max(sys_nodes_int)
        pub_ports_ka = [v['publish_ports']['keep_alive'] for k,v in self.sys_nodes.items()]
        pub_ports_m = [v['publish_ports']['measurement'] for k,v in self.sys_nodes.items()]
        node_data['publish_ports'] = {'keep_alive': max(pub_ports_ka)+1,
                                      'measurement': max(pub_ports_m)+1
                                     }
        # add new node_data to syst_nodes
        self.sys_nodes[str(new_node_id)] = node_data
        # Return the node_id for the newcomer and the sys_nodes dict.
        
        # To stop the server
        self.quit = 1

        return str(new_node_id)+';'+json.dumps(self.sys_nodes, ensure_ascii=False)
        
        
        
if __name__ == '__main__': # to test the server
    rpc = RPC()
    rpc.start_server()