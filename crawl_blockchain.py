import requests
from tqdm import tqdm_notebook
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import time
import copy
import networkx as nx
import glob
import pickle

## recusively get txs
def get_etherscan_nft_txs(wallet_id):
    base_url = 'https://api.etherscan.io/api?module=account'

    base_url+='&action=tokennfttx'
    base_url+='&address='+wallet_id

    # etherscan api key
    etherscan_key = ''
    base_url+='&apikey='+etherscan_key

    # sort asc
    base_url+='&sort=asc'

    s_block = 0
    continue_crawl = True
    all_data = pd.DataFrame()

    while continue_crawl:
        # set block limits
        base_url+='&startblock='+str(s_block)+'&endblock=99999999'

        r = requests.get(base_url)
        r = r.json()

        tmp_data = organize_nft_data(r['result'],wallet_id)
        all_data = all_data.append(tmp_data, ignore_index=True)

        if len(tmp_data)>=10000:
            s_block =all_data.blockNumber.max()
        else:
            continue_crawl = False

    return all_data

def get_polygonscan_nft_txs(wallet_id):
    base_url = 'https://api.polygonscan.com/api?module=account'

    base_url+='&action=tokennfttx'
    base_url+='&address='+wallet_id

    # etherscan api key
    api_key = ''
    base_url+='&apikey='+api_key

    # sort asc
    base_url+='&sort=asc'
    continue_crawl = True
    s_block = 0

    all_data = pd.DataFrame()

    while continue_crawl:
        time.sleep(2)
        # set block limits
        base_url+='&startblock='+str(s_block)#+'&endblock=999999999'

        r = requests.get(base_url)
        r = r.json()

        tmp_data = organize_nft_data(r['result'], wallet_id)
        all_data = all_data.append(tmp_data, ignore_index = True)

        if len(tmp_data)==10000:
            s_block = all_data.blockNumber.max()
        else:
            continue_crawl = False

    return all_data


def organize_nft_data(result_l, origin_acc):
    # organizes the transsactions of an user
    block_number = []
    timestamp = []
    tx_hash = []

    from_acc = []
    to_acc = []
    contract_add = []

    token_id = []
    token_name = []
    token_symbol = []
    token_decimal = []

    gas_price_l = []
    gas_used = []

    for tmp_tx in result_l:
        block_number.append(tmp_tx['blockNumber'])
        timestamp.append(tmp_tx['timeStamp'])
        tx_hash.append(tmp_tx['hash'])

        # tx gas
        n_gas_var = len(tmp_tx['gasPrice'])
        tmp_val = '0.'+ '0'*(18-n_gas_var)+tmp_tx['gasPrice']
        if tmp_val != '.':
            gas_price_l.append(float(tmp_val))
        else:
            gas_price_l.append(0)

        gas_used.append(tmp_tx['gasUsed'])


        # accounts transfer
        from_acc.append(tmp_tx['from'])
        to_acc.append(tmp_tx['to'])
        contract_add.append(tmp_tx['contractAddress'])
        token_id.append(tmp_tx['tokenID'])
        token_name.append(tmp_tx['tokenName'])
        token_symbol.append(tmp_tx['tokenSymbol'])
        token_decimal.append(tmp_tx['tokenDecimal'])



    df = pd.DataFrame({"txhash":tx_hash, 'blockNumber':block_number,
                      'timeStamp':timestamp,'from':from_acc,
                      'to':to_acc,
                       'gas_value':gas_price_l,'gas_used':gas_used,
                      'contract_add':contract_add, 'token_id':token_id,
                      'token_name':token_name,'token_symbol':token_symbol,
                      'token_decimal':token_decimal})

    df['origin_acc'] = origin_acc
    return copy.deepcopy(df)

###
## notes
# 1. the above code can be run in a recursive fashion (minding the rate control limits)
# 2. the same structure can be modified to get the NFTs from specific contracts (e.g. Foundation)
# 3. the same structure can be modified to get monetary transactions (money) and token purchases (ERC-20)
###

## example use -- given a user id return their nfts purchased:
user_id = ""
ethereum_nfts = get_etherscan_nft_txs(user_id)
polygon_nfts = get_polygonscan_nft_txs(user_id)

ethereum_nfts_df = organize_nft_data(ethereum_nfts['result'], user_id)
polygon_nfts_df = organize_nft_data(polygon_nfts['result'], user_id)

print(ethereum_nfts_df.head())
print(polygon_nfts_df.head())
