import node
import time
from utils.save_data_csv import SaveDataCSV
import sys

# Default params
file_name = 'master_threaded_2'
node_ip = 'syslab-10',

# Ensure we got enough arguments coming in
assert len(sys.argv) >= 1, "Must supply at least 1 argument.\n" + \
    "Usage: rpc_sync_pi_master.py N [argument2 ...]"
# Split incoming arguments into the number of throws to use.
# Note that sys.argv[0] is the name of the script itself.
scriptname, *args = sys.argv
if args!=list():
	if len(args)>=1:
		file_name = args[0]
	if len(args)>=2:
		node_ip = args[1]
	if len(args)>=3:
		master_ip = args[2]


sd = SaveDataCSV(f'log/{file_name}.csv')
sd.save_data({'Start':1})
sd_th = 0.2

try:

    n1 = node.Node(ip=node_ip,
                master_ip=node_ip,
                #master_rpc_port=8000,
                produce=1,
                control=1)

    n1.rpc.start_server_thread(n1.node_ip, n1.rpc_port)
    sd.save_data({'Start RPC server':1})

    if n1.master_id == n1.node_id:
        n1.system_nodes[str(n1.master_id)]['publish_ports']['step'] = 4000
        n1.pub._pub('step',4000)

        n1.system_nodes[str(n1.master_id)]['publish_ports']['nodes_list'] = 4001
        n1.pub._pub('nodes_list',4001)

        n1.rpc.sys_nodes = n1.system_nodes
        n1.rpc.server.sys_nodes = n1.rpc.sys_nodes

        step = 1
        while True:
            if step == 4:
                step = 0
            print(f"\n\nStep {step}")
            n1.publish('step',str(step))
            sd.save_data({'Step':step})
            
            #update system_nodes to update all nodes
            n1.rpc.sys_nodes = n1.rpc.server.sys_nodes
            n1.system_nodes =  n1.rpc.sys_nodes
            n1.publish_nodes_list()

            if step==0:# publish keep alive
                print('Time to Publish keep alive')
                n1.publish_keep_alive()
                sd.save_data({'Keep-alive':step+sd_th})

            elif step==1:
                print('Time to register newcomers')
                time.sleep(5) #waiting for nodes to connect
                print(f'system_nodes: {n1.rpc.sys_nodes}')
                print(f'system_nodes: {n1.system_nodes}')
                #n1.rpc.sys_nodes = n1.system_nodes
                #n1.rpc.ask_node(function='set_sys_nodes', arguments=n1.system_nodes)
                #n1.system_nodes = n1.rpc.sys_nodes
                
                #n1.wait_new_nodes()
                print(n1.system_nodes)
                for node_id, data in n1.system_nodes.items():
                    if node_id != n1.node_id:
                        n1.subscribe_topic(node_id, data['publish_ports'])
                        sd.save_data({'Subscribe to':node_id})

            elif step==2:# publish measurements
                print('Time to Publish measurements')
                n1.publish_meas(step+sd_th)
                sd.save_data({'Measurement':step+sd_th})

            elif step==3:# check subscriptions
                print('Time to check subscriptions')
                n1.check_subscriptions()
                sd.save_data({'Check subscriptions':step+sd_th})
                
            else:
                pass
            time.sleep(5)
            step += 1


except KeyboardInterrupt:
    print("Exiting")
    sd.save_data({'Stop':1})
    sd.save_csv()
