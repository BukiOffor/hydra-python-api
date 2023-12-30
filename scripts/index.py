import iop_python as iop
import asyncio
import requests
import json
import time



url = "https://test.explorer.hydraledger.io:4705/morpheus/v1/did/did:morpheus:ezbeWGSY2dqcUBqT8K7R14xr/document"

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    print(type(data)) 


async def send_transaction(phrase,receiver,amount, nonce):
    res = await iop.send_transaction_with_python(phrase,receiver,amount,nonce)
    return res



main_wallet = "blind market ability shoot topple round inmate pass lunch symbol average alpha party notice switch sea pass toy alien fuel pull angle weather scan"
seedPhrase = iop.generate_phrase()
#print(seedPhrase)
ark_wallet = iop.get_ark_wallet(main_wallet)
hyd_wallet = iop.get_wallet(main_wallet, "password")
print("ark wallet: ",ark_wallet)
print('hyd wallet: ',hyd_wallet)
ark_wallet = "taQb8gfnetDt6KtRH3n11M3APMzrWiBhhg"


# Define the URL you want to send a request to
url = f"https://test.explorer.hydraledger.io:4705/api/v2/wallets/{hyd_wallet}"

# Send a GET request to the URL
response = requests.get(url)

if response.status_code == 200:
    data = response.json()  # Assuming the response is in JSON format
    print("Received data:", data)
    nonce = int(data['data']['nonce'])
    balance = data['data']['balance']
    result = asyncio.run(send_transaction(main_wallet,ark_wallet,1000,nonce))
    print('result ==', result)
    r = json.loads(result)
    hash = r['data']['accept'][0]
    print("transction hash is ", hash)
    urll = f"https://test.explorer.hydraledger.io:4705/api/v2/transactions/{hash}"
    time.sleep(15)
    res = requests.get(urll)
    c = res.json()
    print("c is ",c)
    txid = c['data']['id']
    blockId = c['data']['blockId']
    fee = c['data']['fee']
    confirmations = c['data']['confirmations']
    time = c['data']['timestamp']['human']
    print(f' Transaction with id {txid} was sent successfully at {time} with a fee of {fee} Hyd and has {confirmations} confirmations ')
else:
    print("Failed to fetch data. Status code:", response.status_code)

