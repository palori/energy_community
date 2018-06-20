import node
import time


try:

    n1 = node.Node(ip='syslab-09', 
                master_ip='syslab-10',
                #master_rpc_port=8000,
                produce=1,
                control=0)
    
    while n1.node_id == None:
        print('Try to connect...')
        n1.connect2RpcMaster()
        time.sleep(1)

    print("\n\nWelcome to the energy community!")
    print(n1.system_nodes)

    n1.subscribe_topic(str(n1.node_data['master_id']), topics={'step':4000})
    for node_id in n1.system_nodes.keys():
        if node_id != n1.node_id:
            n1.subscribe_topic(node_id) 
    step = 1
    while True:
        
        n1.subs.check_msgs(check_topic='step') #correct!!!

        #print(f"    Sockets: {n1.subs.sockets}")
        try:
            step = n1.subs.sockets[str(n1.node_data['master_id'])]['step']['last_msg']['msg']
        except KeyError:
            print('  No step received')
            
        print(f"\n\nStep {step}")



        if step==0: # publish keep alive
            print('Time to Publish keep alive')
            n1.publish_keep_alive()
            pass
        elif step==1:
            print('Time to register newcomers')
            time.sleep(1)

        elif step==2:# publish measurements
            print('Time to Publish measurements')
            n1.publish_meas(1)

        elif step==3:# check subscriptions
            print('Time to check subscriptions')
            n1.check_subscriptions()

        else:
            pass
        time.sleep(5)


except KeyboardInterrupt:
    print("Exiting")