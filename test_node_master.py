import node
import time
from utils.save_data_csv import SaveDataCSV

file_name = 'master1_1'
# Ensure we got enough arguments coming in
assert len(sys.argv) >= 1, "Must supply at least 1 argument.\n" + \
    "Usage: rpc_sync_pi_master.py N [argument2 ...]"
# Split incoming arguments into the number of throws to use.
# Note that sys.argv[0] is the name of the script itself.
scriptname, *_file_name = sys.argv
if _file_name!=list():
    file_name = _file_name[0]

sd = SaveDataCSV(f'log/{file_name}.csv')
sd.save_data({'Start':1})
sd_th = 0.2

try:
    n1 = node.Node(ip='syslab-10', 
                master_ip='syslab-10',
                #master_rpc_port=8000,
                produce=1,
                control=0)

    sd.save_data({'Start RPC server':1})

    if n1.master_id == n1.node_id:
        n1.system_nodes[str(n1.master_id)]['publish_ports']['step'] = 4000
        n1.pub._pub('step',4000)
        step = 1
        while True:
            if step == 4:
                step = 0
            print(f"\n\nStep {step}")
            n1.publish('step',str(step))
            sd.save_data({'Step':step})

            if step==0:# publish keep alive
                print('Time to Publish keep alive')
                n1.publish_keep_alive()
                sd.save_data({'Keep-alive':step+sd_th})

            elif step==1:
                print('Time to register newcomers')
                n1.wait_new_nodes()
                print(n1.system_nodes)
                for node_id, data in n1.system_nodes.items():
                    if node_id != n1.node_id:
                        n1.subscribe_topic(node_id, data['publish_ports'])
                        sd.save_data({'Subscribe':step+sd_th})

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
