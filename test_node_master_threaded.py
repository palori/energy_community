import node
import time
from utils.save_data_csv import SaveDataCSV

sd = SaveDataCSV('log/master_threaded_1.csv')
sd.save_data({'Start':1})
sd_th = 0.2
try:

    n1 = node.Node(ip='localhost',#'syslab-10', 
                master_ip='localhost',#'syslab-10',
                #master_rpc_port=8000,
                produce=1,
                control=0)

    n1.rpc.start_server_thread(n1.node_ip, n1.rpc_port)
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
                pass

            elif step==1:
                print('Time to register newcomers')
                time.sleep(5) #waiting for nodes to connect
                n1.rpc.sys_nodes = n1.system_nodes
                n1.rpc.ask_node(function='set_sys_nodes', arguments=n1.system_nodes)
                #n1.wait_new_nodes()
                print(n1.system_nodes)
                for node_id, data in n1.system_nodes.items():
                    if node_id != n1.node_id:
                        n1.subscribe_topic(node_id, data['publish_ports'])
                        sd.save_data({'Subscribe':step+sd_th})

            elif step==2:# publish measurements
                print('Time to Publish measurements')
                n1.publish_meas(0)
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
