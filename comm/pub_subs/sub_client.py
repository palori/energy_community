import sys
#import python3-zmq as zmq
import zmq
import json
import time

class Subscriber():
    
    def __init__(self):
        self.sockets = {}
        #                   = {'node_id1': {'topic1': {'node_ip10':'localhost', 'port':5556, 'socket':soc,
        #                                              'last_msg': {'time':time, 'msg':msg},
        #                                   'topic2': {...}}
        #                      'node_id2': {'topic1': {...}}}
        self.keep_alive_dict = {} # {'node_id1': 0, 'node_id2': 1} # 1:alive, 0:stopped
        self.KEEP_ALIVE_TIME_THRESHOLD = 20 # seconds
        self.KEEP_ALIVE_TOPIC = 'keep_alive'
        self.KEEP_ALIVE_MSG = 'Still here!'
        self.MEASUREMENT_TOPIC = 'measurement'
        
        self.step = 4 # updated by the master with its keep_alive.
        #               new node starts trying to reach the master for the first time!
        
    #@property
    def sockets(self):
        return self.sockets

    def subscribe(self, node_id='0', node_ip='localhost', topicfilters={'keep_alive':5556, 'measurement':5557}):
        
        # Ceck if topics asked to subscribe of a certain node are already in use and also the ports
        already_subs = {}
        for node,data in self.sockets.items():
            if node == node_id:
                for topic,data1 in data.items():
                    port = data1['port']
                    for new_topic, new_port in topicfilters.items():
                        if new_topic == topic:
                            print(f"Already subscribed in topic {topic} of node {node_id}.")
                            already_subs[new_topic] = port
                        elif new_port == port:
                            print(f"Port {port} already in use for an other topic of node {node_id}.")
                            already_subs[new_topic] = port
        
        for k in already_subs.keys():
            del topicfilters[k]

        # With the topics and ports that are not subscribed/used yet
        for topic, port in topicfilters.items():
            if(port >= 2000 and port<9000): # improve port checking (fine for testing)
                self._subs(node_id, topic, node_ip, port)
            else:
                print(f"Port {port} out of range [2000,9500].")

                                        
    def _subs(self, node_id, topic, node_ip, port):
        # Socket to talk to server
        context = zmq.Context()
        socket = context.socket(zmq.SUB)

        #print("Collecting updates from time server at tcp://localhost:{port}")
        socket.connect(f"tcp://{node_ip}:{port}")
        
        # Filter by topic
        socket.setsockopt_string(zmq.SUBSCRIBE, topic)
        
        # Save data
        data = {'ip':node_ip,
                'port': port,
                'socket': socket,
                'last_msg':{}}
        try: # already subscribed to some topic of this node?
            node = self.sockets[node_id]
            node[topic] = data
        except KeyError as e: # subscribe to the first topic of this node
            self.sockets[node_id] = {topic: data}
    
    def unsubscribe(self, node_id='0', topic='all'):
        # unsubscribe from 1 or all topics
        try:
            node_sockets = self.sockets[node_id]
        except KeyError as e:
            print(e)
            pass
            
        if topic == 'all':
            for top, data in node_sockets.items():
                socket = data['socket']
                # socket.setsockopt_string(zmq.UNSUBSCRIBE, topic)
                socket.close()
                
            try:
                del self.sockets[node_id]
            except KeyError as e:
                print(e)
            
        else:
            for top, data in node_sockets.items():
                if top == topic:
                    socket = data['socket']
                    # socket.setsockopt_string(zmq.UNSUBSCRIBE, topic)
                    socket.close()
                    try:
                        del self.sockets[node_id][topic]
                    except KeyError as e:
                        print(e)
                    
                    
    def check_msgs(self, check_topic='keep_alive', node_id='all'): # Check either 1 or all nodes
        is_check_master = False
        if node_id=='all':
            # Check last message of a topic for all open sockets
            for node_id, data in self.sockets.items():
                for topic, data1 in data.items():
                    if check_topic == topic:
                        socket = data1['socket']
                        self._check_msg(is_check_master, node_id, topic, socket)
        else:
            is_check_master = True
            socket = self.sockets[node_id][check_topic]['socket']
            self._check_msg(is_check_master, node_id, topic, socket)
                
        
    def _check_msg(self, is_check_master, node_id, topic, socket):
        print(f"_check_msg({node_id}, {topic})")
        t_init = time.time()
        while time.time()-t_init < 2:
            try:
                string = socket.recv_string(flags=zmq.NOBLOCK)
                t1 = time.time()
                
                if is_check_master: # master sends also the steps
                    topic, messagedata, t0, self.step = string.split(';')
                else:
                    topic, messagedata, t0 = string.split(';')
                print(f"Received on topic {topic}: {messagedata} (Delta t = {t1-float(t0)})\n")
                    
                # save data
                self.sockets[node_id][topic]['last_msg'] = {'time':t1, 'msg':messagedata}
                break
            except zmq.error.Again as e:
                print(e)
            time.sleep(1)
        
        # if topic == self.KEEP_ALIVE_TOPIC: and not getting anytihg new update self.keep_alive_dict !!!!!!!!!!!!!!!!
        # compare time of last_msg and now if > seconds_threshold
        try:
            if (time.time() - self.sockets[node_id][topic]['last_msg']['time']) > self.KEEP_ALIVE_TIME_THRESHOLD:
                self.keep_alive_dict[node_id] = 0
            else:
                self.keep_alive_dict[node_id] = 1
        except KeyError as e:
            print(e)



    # may be done in the Node class
    def revise_keep_alives(self):
        print(self.keep_alive_dict)
        # what to do in case of detecting that a node may be down -> notify Master or others
        pass
    
    def get_last_measurements(self): # some may be None
        meas_list = set()
        for node_id in self.sockets.keys():
            meas_list.add(self._get_last_measurement(node_id))
        return meas_list

    def _get_last_measurement(self, node_id): # may be None
        try:
            return self.sockets[node_id][self.MEASUREMENT_TOPIC]['last_msg']
        except KeyError as e:
            # node may not exist for it or may not need to get measurement
            print(e)
            return None
                        
if __name__ == '__main__':
    print('subs start')
    test = Subscriber()
    test.subscribe(topicfilters={'keep_alive':5556, 'measurement':5557})
    time.sleep(2)
    print('check msgs')
    for i in range(5):
        test.check_msgs()
        test.check_msgs('measurement')
        test.revise_keep_alives()
        time.sleep(1)
    time.sleep(2)
    test.unsubscribe()
    print('subs stop')
    
