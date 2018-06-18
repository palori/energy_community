import zmq
import random
import sys
import time
from zmq.utils.monitor import recv_monitor_message

class Publisher():
    
    def __init__(self):
        self.sockets = {} # = {'topic1': {'port':5556, 'socket': soc}, 'topic2': ...}
        self.KEEP_ALIVE_TOPIC = 'keep_alive'
        self.KEEP_ALIVE_MSG = 'Still here!'
        self.MEASUREMENT_TOPIC = 'measurement'
        
    #@property
    def sockets(self):
        return self.sockets
        
    def new_topics(self, new_topics={}):#'keep_alive':5556, 'measurement':5557}):
        
        # Check if topic already published or port in use
        for topic,data in self.sockets.items():
            port = data['port']
            for new_topic, new_port in new_topics.items():
                if new_topic == topic:
                    print(f"Already publishing in topic {topic}.")
                    del new_topics[new_topic]
                elif new_port == port:
                    print(f"Port {port} already in use for an other topic.")
                    del new_topics[new_topic]
                    
        # With the topics and ports that are not used yet
        for topic, port in new_topics.items():
            if(port >= 2000 and port<9500): # improve port checking (fine for testing)
                self._pub(topic, port)
            else:
                print(f"Port {port} out of range [2000,9500].")
                
    def _pub(self, topic, port):
        # Create socket to publish
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind(f"tcp://*:{port}")
        
        # Save data
        self.sockets[topic] = {'port': port,
                               'socket': socket}
        
    def publish(self, topic='keep_alive', data='Still here!'): # only 1 msg and 1 topic

        """
        # Get a monitoring socket where we can sniff information about new subscribers.
        monitor = socket.get_monitor_socket()

        sub_list = set()

        while True:
            # Run through monitoring messages and check if we have new subscribers
            while True:
                try:
                    status = recv_monitor_message(monitor, flags=zmq.NOBLOCK)
                    print(f"Status: {status}")
                    if status['event'] == zmq.EVENT_ACCEPTED:
                        print(f"Subscriber \'{status['value']}\' has joined :D")
                        sub_list.add(status['value']) #can we get more info about the nodes that are subscribed? (ie. node_id)
                    if status['event'] == zmq.EVENT_DISCONNECTED:
                        print(f"Subscriber \'{status['value']}\' has left :(")
                        sub_list.remove(status['value'])
                except zmq.Again as e:
                    break
            # Time to publish the latest time!
            messagedata = time.ctime()
            #messagedata = json.dumps(nodes, ensure_ascii=False)
            # Note the use of XXX_string here;
            # the non-_string-y methods only work with bytes.
            socket.send_string(f"{topic};{messagedata}")
            print(f"Published topic {topic}: {messagedata} to subscribers: {sub_list}")
            time.sleep(5)
        """
        # Just send, now don't care about how many subscribers and when they connect or disconnect
        try:
            socket = self.sockets[topic]['socket']
        except KeyError as e:
            print(e)
            pass
        messagedata = data #????????????????????????????????????????????
        socket.send_string(f"{topic};{messagedata};{time.time()}")
        print(f"Published topic {topic}: {messagedata}.")
        time.sleep(1)
        
    def stop_publishing(self, topic):
        pass
        
        
if __name__ == '__main__':

    test = Publisher()
    test.new_topics({'keep_alive':5556, 'measurement':5557})
    count = 0
    while count<3:
        test.publish(data=str(count))
        test.publish(topic='measurement', data=str(time.time()))
        time.sleep(10)
        count += 1