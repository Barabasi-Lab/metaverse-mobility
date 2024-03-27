import numpy as np
import pandas as pd
import time
from datetime import datetime
import tqdm.notebook as tq
import requests
import matplotlib.pyplot as plt

## this function organizes the data frame
def get_peer_positions(island_lists):
    island_id_l = []
    island_center = []
    island_radius = []

    # peers
    peer_id_l = []
    peer_address = []
    peer_last_ping = []
    peer_parcel_x = []
    peer_parcel_y = []
    peer_position_x = []
    peer_position_y = []
    peer_position_z = []


    for i in island_lists:
        for j in i['peers']:
            if 'address' not in j:
                continue
            island_id_l.append(i['id'])
            island_center.append(i['center'])
            island_radius.append(i['radius'])

            peer_id_l.append(j['id'])
            peer_address.append(j['address'])
            peer_last_ping.append(j['lastPing'])
            peer_parcel_x.append(j['parcel'][0])
            peer_parcel_y.append(j['parcel'][1])

            peer_position_x.append(j['position'][0])
            peer_position_y.append(j['position'][1])
            peer_position_z.append(j['position'][2])

    df = pd.DataFrame({'island_id':island_id_l,'island_center':island_center,
                      'island_rad':island_radius,
                      'peer_id':peer_id_l,'peer_address':peer_address,
                      'parcel_x':peer_parcel_x,'parcel_y':peer_parcel_y,
                      'position_x':peer_position_x,'position_y':peer_position_y,
                      'position_z':peer_position_z})

    # add the timestamp of crawl
    df['timestamp_crawl'] = time.mktime(datetime.now().timetuple())
    return df

## location where the ping originates
base_url = 'https://peer.decentraland.org'
base_url+='/comms/islands'

# mobility of all players
all_df = pd.DataFrame()

# max time step iteration
# -- this basically controls whether you want a 20s delay between data calls or 1 minute.
max_time = 10

for i in tq.tqdm(range(max_time)):
    r = requests.get(base_url)
    peer_df = get_peer_positions(r.json()['islands'])
    all_df = all_df.append(peer_df, ignore_index=True)

print(all_df.head())
