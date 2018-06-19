
# This is the structure of how the dictionary of the system nodes will look like


nodes = {'1': {'id':1, # both should be the same and unique (also used for leader election)
                       # do we need it??????????????
               'ip':'192.168.0.101',
               'rpc_port': 9001, # given by the master
               'master_id': '1000', # given by the master, int or str??
               'produce':1, #1=yes, 0=no
               'control':1, #1=yes, 0=no
               'publish_ports':{'keep_alive':5001,
                                'measurement':6001
                               }
               #'subscribed_ports':{} #it will fill in when adding to the system
              },
         
         '10': {'id':10, #both should be the same and unique (also used for leader election)
               'ip':'192.168.0.110',
               'rpc_port': 9010,
               'rpc_status':10, #1=master, 0=slave
               'produce':10, #1=yes, 0=no
               'control':10, #1=yes, 0=no
               'publish_ports':{'keep_alive':5010,
                                'measurement':6010
                               }
               #'subscribed_ports':{} #it will fill in when adding to the system
              }
        }

# store data in file???
