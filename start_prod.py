import glob
import os
import sys
workspace = os.path.dirname(os.path.abspath(__file__))
sys.path.append(workspace)
sys.path.append(os.getcwd())
import sysvars
import datetime
from AlertCypher import AlertCypher
from subprocess import *
from time import sleep
import argparse
from RDAS_MEMGRAPH_APP.Alert import Alert
from RDAS_MEMGRAPH_APP.Transfer import Transfer
from datetime import datetime

#!!! Script has to be ran with SUDO !!!

email_client = Alert()
transfer_module = Transfer('prod')
db = AlertCypher('system')
init = True

while True:
    try:
        print('checking for update...')
        # Detect new dumps in the production server
        transfer_detection,last_updates = transfer_module.detect(sysvars.transfer_path)
        new_dumps = transfer_detection

        # Sets the current db files last transfer date to today so it doesnt load and send emails upon script starting
        if init:
            init = False
            continue

        # Seed the seed cluster with the new dumps
        for db_name in new_dumps:
            db_single = AlertCypher(db_name)

            print('update found::', db_name)
            last_update_obj = datetime.fromtimestamp(float(last_updates[db_name]))
            print('starting database loading')
            transfer_module.seed(db_name, sysvars.transfer_path)

            if transfer_module.get_isSeeded():
                db_single.run('MATCH (x:UserTesting) DETACH DELETE x') # Removes UserTesting Node
                
                print('starting email service')
                email_client.trigger_email([db_name], date_start=datetime.strftime(last_update_obj, "%m/%d/%y"))

                transfer_module.set_isSeeded(False)

        # Sleep for a minute before checking for new dumps again
        sleep(60)
    except Exception as e:
        print(e)


