import node
import time
from utils.sava_data_csv import SaveDataCSV


try:
    n1 = node.Node(ip='localhost',#'syslab-10', 
                master_ip='localhost',#'syslab-10',
                #master_rpc_port=8000,
                produce=1,
                control=0)


    if n1.master_id == n1.node_id:
        n1.system_nodes[str(n1.master_id)]['publish_ports']['step'] = 4000
        n1.pub._pub('step',4000)
        step = 1
        while True:
            if step == 6:
                step = 0
            print(f"\n\nStep {step}")
            n1.publish('step',str(step))

            if step==0:# publish keep alive
                print('Time to Publish keep alive')
                n1.publish_keep_alive()
                pass

            elif step==1:
                print('Time to register newcomers')
                n1.wait_new_nodes()
                print(n1.system_nodes)
                for node_id, data in n1.system_nodes.items():
                    if node_id != n1.node_id:
                        n1.subscribe_topic(node_id, data['publish_ports'])

            elif step==2:# publish measurements
                print('Time to Publish measurements')
                n1.publish_meas(0)

            elif step==3:# check subscriptions
                print('Time to check subscriptions')
                n1.check_subscriptions()
                
            else:
                pass
            time.sleep(5)
            step += 1

except KeyboardInterrupt:
    print("Exiting")
    sd.save_data({'Stop':1})
    sd.save_csv()
