
from rpc import RPC

    
if __name__ == '__main__':
    client = RPC()
    client.ask_node(rpc_port=8000,function='test')
