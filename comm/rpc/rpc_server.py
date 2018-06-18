import logging
import time
from xmlrpc.server import SimpleXMLRPCServer


def reverse_list(l):
    logging.debug(f'Call received: reverse_list({l!r}), calculating for 1 second')
    time.sleep(1)
    return l[::-1]

def pudor(d):
    logging.debug(f'per no fer pudor amb aquesta {d}')
    time.sleep(1)
    return f"Tamany de la caca = {str(d['measurement'])} km!!!!!!!!!!!!!"

def kill():
    server.quit = 1
    return 1


class MyServer(SimpleXMLRPCServer):

    def serve_forever(self):
        self.quit = 0
        while not self.quit:
            self.handle_request()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    server = MyServer(('localhost', 9900), logRequests=True)
    # Register the function we are serving
    server.register_function(reverse_list, 'reverse')
    server.register_function(pudor, 'caca')
    server.register_function(kill, 'kill')
    quit = 0
    try:
        print("Use Control-C to exit")
        # Start serving our functions
        server.serve_forever()
        #server.handle_request()
    except KeyboardInterrupt:
        print("Exiting")
            
            
            
