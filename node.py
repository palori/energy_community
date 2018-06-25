import time
import json
from comm.pub_subs.pub_server import Publisher
from comm.pub_subs.sub_client import Subscriber
from comm.rpc.rpc import RPC
from threading import Thread

class Node():
    
    
    def __init__(self,
                 ip='localhost', 
                 master_ip='localhost',
                 master_rpc_port=8000,
                 produce=1, 
                 control=1):
                 # meas_th=1):
        
        # Constants assigned to the initial master
        self.NODE_ID = 1000
        self.RPC_PORT = 8000
        self.KEEP_ALIVE_PORT = 5000
        self.MEASUREMENT_PORT = 6000

        # Patameters
        self.master_ip=master_ip
        self.master_rpc_port=master_rpc_port
        self.node_id=None
        self.node_ip=ip
        self.rpc_port=None
        # self.node_type=node_type
        self.master_id=None
        self.produce=produce
        self.control=control
        self.keep_alive_port=None
        self.measurement_port=None
        #self.meas_th=meas_th # measurement threshold
        
        # other
        self.prev_meas = 0 # previous measurement
        self.system_nodes = {} # sent by the master ?????????
        self.possible_nodes_down = {} # node_id and number of times checked and not got info

        self.rpc = RPC()
        
        self.connect2RpcMaster()
        
    def get_node_data(self):
        self.node_data = {'id':self.node_id, # both should be the same and unique (also used for leader election)
                                   # do we need it??????????????
                          'ip':self.node_ip,
                          'rpc_port': self.rpc_port, # given by the master
                          'master_id': self.master_id, # given by the master, int or str??
                          'produce': self.produce,
                          'control': self.control,
                          'publish_ports':{'keep_alive': self.keep_alive_port,
                                           'measurement': self.measurement_port
                                          }
                         }
        return self.node_data
    
    def connect2RpcMaster(self):
        print(f"+++ master ip: {self.master_ip}, node ip: {self.node_ip}, node id: {self.node_id}")
        # create RPC to connect and send node_data
        response = None
        if self.master_ip == self.node_ip:
            if self.node_id == None:
                self.node_id = self.NODE_ID
                self.master_id = self.NODE_ID
                self.rpc_port = self.RPC_PORT
                self.keep_alive_port = self.KEEP_ALIVE_PORT
                self.measurement_port = self.MEASUREMENT_PORT
                self.system_nodes[str(self.node_id)]= self.get_node_data()
                response = self.system_nodes
        else:
            print(f'\n  -- node data --\n {self.get_node_data()}')
            response = self.rpc.ask_node(node_ip=self.master_ip,
                                         rpc_port=self.master_rpc_port,
                                         function='new_node',
                                         arguments=json.dumps(self.get_node_data(), ensure_ascii=False))
            print(f"+++ response: {response}")
            if response != None:
                self.node_id, sys_nodes = response.split(';')
                self.system_nodes = json.loads(sys_nodes)
                self.node_data = self.system_nodes[self.node_id]

            #self.system_nodes = self.rpc.sys_nodes
        if response != None:
            print(f"Sistem nodes: {self.system_nodes}")
            # once done try to subscribe to others and start publish...
            self.pub = Publisher()
            self.pub.new_topics(self.node_data['publish_ports'])
            #{'keep_alive':self.system_nodes['publish_ports']['keep_alive'],'measurement':self.system_nodes['publish_ports']['measurement']})
            self.subs = Subscriber()
        
        
    def publish_meas(self, meas): # meas = measurement
        
        # check if meas id float/double and not NaN, None...
        if meas != None:
            #if abs(meas - self.prev_meas) > self.meas_th:
                
            # publish measurement...
            self.pub.publish(topic='measurement', data=meas)
            self.prev_meas = meas # only overwrite in this case

    
    def publish_keep_alive(self):
        
        #choose freq.
        self.pub.publish()

    def publish(self, topic, data): # generic version for the step and other topics
        # i.e: topic = 'step', data = 3
        if data != None:
            self.pub.publish(str(topic),str(data))

    def publish_nodes_list(self):
        self.pub.publish('nodes_list',json.dumps(self.system_nodes, ensure_ascii=False))
    
    def subscribe_topic(self, node_id, topics='all'):
        
        node = self.system_nodes[node_id]
        if topics == 'all':
            topics = node['publish_ports']
        #else:
        #    topics = {'topic': port, ...}
        
        if not self.control: # if this node just measure no need to get measurements from others
            try:
                del node['publish_ports']['measurement']
            except KeyError as e:
                print(f"{e}: This node has no control involved.")
        self.subs.subscribe(node_id=node_id,
            node_ip=node['ip'],
            topicfilters=topics)

    def update_nodes_list(self):
        nl = self.subs.check_msgs(check_topic='nodes_list')
        if nl!=None and nl!="":
            self.system_nodes = json.loads(nl)
            print(f'updated: {self.system_nodes}')
    
    def check_subscriptions(self): # topic, ip, port ??? maybe check all based on a list
        
        #choose freq.
        
        # if detected possible node down add to the dict -> self.possible_nodes_down
        # if node already in this list, increment the counter or via timers
        # if reached a th then notify the master -> _notify_node_down()
        
        # if not getting any data from others or from less than half of the nodes -> close RPC, stop pub, unsubscribe
        #     maybe set node_id = None like if it's not in the network, even reboot the controller
        self.subs.check_msgs() # keep_alive
        self.subs.check_msgs(check_topic='measurement')
        
        nodes = self.subs.keep_alive_dict
        count_nodes_on = 0
        total_nodes = 0
        for node_id, node_on in nodes.items():
            count_nodes_on += node_on
            total_nodes += 1
            if not node_on:
                self.possible_nodes_down[node_id]
        

        if total_nodes != 0 and count_nodes_on/total_nodes > 0.4:
            print('This node may be out of range for 40% or more other nodes.\nSuggest to reboot or check the phicical connections.\n')
        
        elif  count_nodes_on < total_nodes:
            print('Some node may be out of range also for other nodes.\nNotify the Master or others.\n')
        
        elif total_nodes == 0:
            print('No single message from other nodes')

        else:
            print('Got data from all the nodes.')


    def notify_node_down(self):
        
        # if node_id of node down == master_id -> leader election (ask if others receive info from the master)
        # else notify master via RPC and this will ask the rest of the nodes if they got sth from node down
        
        pass
    
    def whos_master(self):
        sys_nodes_int=[int(n) for n in self.system_nodes.keys()]
        print(sys_nodes_int)
        self.master_id = max(sys_nodes_int)
        print(f"Master is {self.master_id}")
        
        
    def wait_new_nodes(self, time_period=10):
        #th1 = Thread()
        #th1.start()
        self.rpc.sys_nodes = self.system_nodes
        self.rpc.start_server(self.node_ip, self.rpc_port)#, time_period=time_period)

        """
        t0 = time.time()
        while t1 - t0 < time_period:
            print('Waiting for new nodes')
            time.sleep(1)
        self.rpc.ask_node(self.node_ip, self.rpc_port, 'kill')
        th1.join()
        """


            

            
            
            
            
            
            