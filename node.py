import time
from comm.pub_subs.pub_server import Publisher
from comm.pub_subs.sub_client import Subscriber
from comm.rpc.rpc import RPC

class Node():
    
    def __init__(self,
                 # node_id=None,
                 ip='192.168.0.101', 
                 rpc_port=9001, 
                 node_type='pv', 
                 produce=1, 
                 control=1, 
                 # keep_alive_port=5001,
                 # measurement_port=6001, 
                 meas_th=1):
        # self.node_id=node_id
        self.ip=ip
        self.rpc_port=port
        self.node_type=node_type
        self.produce=produce
        self.control=control
        # self.keep_alive_port=keep_alive_port
        # self.measurement_port=measurement_port
        self.meas_th=meas_th # measurement threshold
        
        self.prev_meas = 0 # previous measurement
        self.system_nodes = {} # sent by the master ?????????
        self.possible_nodes_down = {} # node_id and number of times checked and not got info
        
        self.connect2RpcMaster(master_ip='192.168.0.101', rpc_port=9001)
        
        
        self.pub = Publisher()
        self.pub.new_topics({'keep_alive':self.keep_alive_port, 'measurement':self.measurement_port})
        self.subs = Subscriber()
        
        
    def connect2RpcMaster(self, master_ip='192.168.0.101', rpc_port=9001)
    
        # send RPC to connect and send node_data
        
        if master_ip == self.ip:
            if self.control>0.5:
                self.node_id = 199
            else:
                self.node_id = 99
        else:
            pass
        
        self.node_id=node_id
        self.master_id=master_id
        self.keep_alive_port=keep_alive_port
        self.measurement_port=measurement_port
        # once done try to subscribe to others and start publish... 
        
        
    def publish_meas(self): # meas = measurement
        meas = _get_meas()
        
        # check if meas id float/double and not NaN, None...
        if meas != None:
            if abs(meas - self.prev_meas) > self.meas_th:
                
                # publish measurement...
                self.pub.publish(topic='measurement', data=meas)
                self.prev_meas = meas # only overwrite in this case
        
    def _get_meas(self):
        # specific for each node
        meas = None
        if self.node_type = 'pv':
            meas = _get_pv_data()
        elif self.node_type = 'wb':
            meas = _get_wb_data()
        elif self.node_type = 'wt':
            meas = _get_wt_data()
        elif self.node_type = 'house':
            meas = _get_house_data()
        elif self.node_type = 'batt':
            meas = _get_batt_data()
        else:
            print("Unexpected {1} as 'node_type'.".format(self.node_type))
            # logging this text and may throw an error??
        return meas
        
    # PV
    def _get_pv_data(self):
        pass
    
    # WB = water boiler
    def _get_wb_data(self): 
        pass
    
    # WT = wind turbine
    def _get_wt_data(self):
        pass
    
    # House(s)
    def _get_house_data(self):
        pass
    
    # Battery
    def _get_batt_data(self):
        pass
    
    
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
    
    def start_rpc_master(self):
        pass
    
    def start_rpc_slave(self):
        pass
    
    def stop_rpc_master(self):
        pass
    
    def stop_rpc_slave(self):
        pass
    
    def stop_pub(self):
        pass
    
    # no need to stop subs, the rest of the nodes will delete it from their list so won't be subscribed any more.
    