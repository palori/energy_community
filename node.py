import time
import json
from comm.pub_subs.pub_server import Publisher
from comm.pub_subs.sub_client import Subscriber
from comm.rpc.rpc import RPC

class Node():
    
    # Constants assigned to the initial master
    NODE_ID = 1000
    RPC_PORT = 9000
    KEEP_ALIVE_PORT = 5000
    MEASUREMENT_PORT = 6000
    
    
    def __init__(self,
                 ip='192.168.0.101', 
                 master_ip='192.168.0.101'
                 master_rpc_port=9001,
                 produce=1, 
                 control=1):
                 # meas_th=1):
        
        self.node_id=None
        self.node_ip=ip
        self.rpc_port=None
        # self.node_type=node_type
        self.master_id=None
        self.produce=produce
        self.control=control
        self.keep_alive_port=None
        self.measurement_port=None
        self.meas_th=meas_th # measurement threshold
        
        # other
        self.prev_meas = 0 # previous measurement
        self.system_nodes = {} # sent by the master ?????????
        self.possible_nodes_down = {} # node_id and number of times checked and not got info

        self.pub = Publisher()
        self.pub.new_topics({'keep_alive':self.keep_alive_port, 'measurement':self.measurement_port})
        self.subs = Subscriber()
        self.rpc = RPC()
        
        self.connect2RpcMaster(master_ip, master_rpc_port)
        
    def get_node_data(self):
        self.node_data = {'id':self.node_id, # both should be the same and unique (also used for leader election)
                                   # do we need it??????????????
                          'ip':self.node_ip,
                          'rpc_port': self.rpc_port, # given by the master
                          'master_id': self.master_id, # given by the master, int or str??
                          'produce': self.produce,
                          'control': self.control
                          'publish_ports':{'keep_alive': self.keep_alive_port,
                                           'measurement': self.measurement_port
                                          }
                         }
        return self.node_data
    
    def connect2RpcMaster(self, master_ip, rpc_port)
    
        # create RPC to connect and send node_data
        
        if master_ip == self._node_ip:
            if self.node_id == None:
                self.node_id = NODE_ID
                self.master_id = NODE_ID
                self.rpc_port = RPC_PORT
                self.keep_alive_port = KEEP_ALIVE_PORT
                self.measurement_port = MEASUREMENT_PORT
        else:
            pass
            response = self.rpc.ask_node(node_ip=master_ip, rpc_port=rpc_port,
                                         function='new_node', arguments=get_node_dataself.())
            self.node_id, sys_nodes = response.split(';')
            self.system_nodes = json.loads(sys_nodes)
            self.node_data = self.system_nodes[self.node_id]
        
        # once done try to subscribe to others and start publish... 
        
        
    def publish_meas(self, meas): # meas = measurement
        
        # check if meas id float/double and not NaN, None...
        if meas != None:
            if abs(meas - self.prev_meas) > self.meas_th:
                
                # publish measurement...
                self.pub.publish(topic='measurement', data=meas)
                self.prev_meas = meas # only overwrite in this case

    
    def publish_keep_alive(self):
        
        #choose freq.
        self.pub.publish()
        
    
    def subscribe_topic(self, node_id, topics): # topic, ip, port ???
        #choose freq.
        node = system_nodes[node_id]
        if not self.control: # if this node just measure no need to get measurements from others
            del node['publish_ports']['measurement']
        test.subscribe(node_id=node_id,
            node_ip=self.node['ip'],
            topicfilters=self.node['publish_ports'])

    
    def check_subscriptions(self): # topic, ip, port ??? maybe check all based on a list
        
        #choose freq.
        
        # if detected possible node down add to the dict -> self.possible_nodes_down
        # if node already in this list, increment the counter or via timers
        # if reached a th then notify the master -> _notify_node_down()
        
        # if not getting any data from others or from less than half of the nodes -> close RPC, stop pub, unsubscribe
        #     maybe set node_id = None like if it's not in the network, even reboot the controller
        self.subs.check_msgs()
        self.subs.check_msgs(topic='measurement')
        nodes = self.subs.keep_alive_dict()
        count_nodes_on = 0
        total_nodes = 0
        for node_id, node_on in nodes.items():
            count_nodes_on += node_on
            total_nodes += 1
            if not node_on:
                self.possible_nodes_down[node_id]
        
        if count_nodes_on/total_nodes > 0.4:
            print('This node may be out of range for 40% or more other nodes.\nSuggest to reboot or check the phicical connections.\n')
            pass
        elif count_nodes_on < total_nodes:
            print('Some node may be out of range also for other nodes.\nNotify the Master or others.\n')
            pass


    def notify_node_down(self):
        
        # if node_id of node down == master_id -> leader election (ask if others receive info from the master)
        # else notify master via RPC and this will ask the rest of the nodes if they got sth from node down
        
        pass
    
    def whos_master(self):
        sys_nodes_int=[int(n) for n in self.system_nodes.keys()]
        print(sys_nodes_int)
        self.master_id = max(sys_nodes_int)
        print(f"Master is {self.master_id}")
        
        
    def wait_new_nodes(self):
        while True:
            print('Waiting for new nodes')
            rpc.start_server(node.node_ip, node.rpc_port)
            time.sleep(1)
            
            

            
            
            
            
            
            