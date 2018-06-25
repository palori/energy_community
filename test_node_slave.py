import node
import time
from utils.save_data_csv import SaveDataCSV
import sys

file_name = 'slave1_1'
node_ip = 'syslab-09'
master_ip = 'syslab-10'

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
                master_ip=master_ip,
                #master_rpc_port=8000,
                produce=1,
                control=1)

    sd.save_data({'Start RPC client':1})
    while n1.node_id == None:
        print('Try to connect...')
        n1.connect2RpcMaster()
        sd.save_data({'Try to connect to master':1+sd_th})
        time.sleep(1)

    print("\n\nWelcome to the energy community!")
    print(n1.system_nodes)
    sd.save_data({'Added to the list':2})

    n1.subscribe_topic(str(n1.node_data['master_id']), topics={'step':4000})
    sd.save_data({'Subscribe to':f'Step'})

    n1.subscribe_topic(str(n1.node_data['master_id']), topics={'nodes_list':4001})
    sd.save_data({'Subscribe to':f'Nodes list'})

    for node_id in n1.system_nodes.keys():
        if node_id != n1.node_id:
            #n1.subscribe_topic(node_id)
            n1.subs.subscribe(node_id, n1.system_nodes[node_id]['ip'], n1.system_nodes[node_id]['publish_ports'])
            sd.save_data({f"Subscribe to":f'Keep-alive {node_id}'})
            sd.save_data({f"Subscribe to":f'Measurement {node_id}'})
    step = 1
    while True:
        
        n1.subs.check_msgs(check_topic='step') #correct!!!
        n1.update_nodes_list()
        #print(f"    Sockets: {n1.subs.sockets}")
        try:
            step = n1.subs.sockets[str(n1.node_data['master_id'])]['step']['last_msg']['msg']
            sd.save_data({f"Get step":step})
        except KeyError:
            print('  No step received')
            
        print(f"\n\nStep {step}")



        if step==0: # publish keep alive
            print('Time to Publish keep alive')
            n1.publish_keep_alive()
            sd.save_data({'Keep-alive':step+sd_th})

        elif step==1:
            print('Time to register newcomers')
            time.sleep(1)
            #sd.save_data({'Subscribe':step+sd_th})

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


except KeyboardInterrupt:
    print("Exiting")
    sd.save_data({'Stop':1})
    sd.save_csv()