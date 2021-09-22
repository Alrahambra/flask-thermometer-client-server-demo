import json 
import numbers
import sys
import mariadb
from config import *
from datetime import datetime

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user=mysql_user,
        password=mysql_password,
        host=mysql_host,
        port=mysql_port,
        database=mysql_database,
        autocommit=True

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()


#Sanity check for input data, check that we are actually processing just numbers and expected keys match to what we want to receive
def ThermalDataValidator(tempdata):
    expected_keys = ['temperature', 'humidity', 'timestamp']
    received_keys = []
    #Assuming data is valid
    sanity_state = True
    for key in tempdata:
        if key in expected_keys and isinstance(tempdata[key], numbers.Real): 
            pass
        else:
            sanity_state = False
        received_keys.append(key)
    #Additional check to see if match to what we expect to see
    #Sort and then compare
    expected_keys.sort()
    received_keys.sort()
    if expected_keys == received_keys:
        pass
    else:
        sanity_state = False
    return sanity_state


#Stores values into MariaDB/MySQL database, automatic commits are online and require no further actions
def Store_thermo_entry(device_id, temp, humidity,timestamp):
    sql = "INSERT INTO data_entries (device_id,temp,humidity,timestamp) VALUES ('{}','{}','{}','{}')".format(str(device_id), temp, humidity,timestamp)
    try:
        cur.execute(sql)
        #When commit is OK
        return True
    except Exception as e:
        #Error is logged into console or syslog depending on deployment, return false to tell about error in DB 
        print(f"Error: {e}")
        return False



def Get_thermo_entries(device_id):
    #SQL query...
    sql = '''SELECT temp, humidity, timestamp FROM data_entries where device_id = "{}" order by timestamp desc limit 10080'''.format(device_id)
    #Preprocess...
    cur.execute(sql)
    full_data = cur.fetchall()
    temp_list = []
    humidity_list= []
    timestamp_list = []
    for line in full_data:
        temp = line[0]
        humidity = line[1]
        timestamp = line[2]

        temp_list.append(temp)
        humidity_list.append(humidity)
        #convert to ISO for Plotly
        #sample: 2021-08-30 22:15:37
        iso_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        timestamp_list.append(str(iso_timestamp))
    
    data_dict = {}
    data_dict['temp_data'] = temp_list
    data_dict['hum_data'] = humidity_list
    data_dict['time_data'] = timestamp_list
        


    return data_dict