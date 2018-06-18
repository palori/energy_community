
from xmlrpc.client import ServerProxy
import time

def ask_node(node_ip='localhost', rpc_port=9900, function='reverse', arguments='arg'):
    t_init = time.time()
    while (time.time() - t_init) < 10:
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
    
if __name__ == '__main__':
    #ask_node(arguments = ['hola', 'adeu', 'caca'])
    #ask_node(function='caca', arguments = {'measurement': 24})
    time.sleep(5)
    ask_node(rpc_port=8000,function='test')
