

class Control_node(Node):
    
    def __init__(self, 
                 # node_id=None, 
                 ip='192.168.0.101', 
                 rpc_port=9001, 
                 # rpc_status=1,
                 node_type='pv', 
                 produce=1, 
                 control=1, 
                 # keep_alive_port=5001,
                 # measurement_port=6001,
                 meas_th=1):
        
        # copy to initialize Node
        
        self.kp=kp
        self.ki=ki
        self.sp=sp
        self.tot_err=0
        
        self.curr_total_cons = 0
        pass
    

    
    #sp = Setpoint
    def compute_sp(self):
        # for loop with all nodes and check_subscriptions(topic='measurement') -> add to all_meas
        # check if they are coeherent (ex: in a certain pre-known range...)
        # called from RPC when comm_btw_controllers (initiated by the master)
        meas = self.subs.get_last_measurements()
        self.curr_total_cons = 0
        for m in meas:
            if n != None:
                self.curr_total_cons += m

        # Based on self.curr_total_cons modify self.sp !!!!!!!!!!!!!!!!!!!!!!!!
        pass

    def set_sp(self, new_sp):
        self.sp = new_sp
    
    def control_signal(self):
        
        err = self.sp - self._get_meas()
        tot_err += err
        
        u = self.kp*err + self.ki*tot_err
        return u
    
    def comm_btw_controllers(self):
        pass