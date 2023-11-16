import iop_python as iop
import asyncio
import requests


async def send_transaction(phrase,receiver,amount, nonce):
     await iop.send_transaction_with_python(phrase,receiver,amount,nonce)



main_wallet = "blind market ability shoot topple round inmate pass lunch symbol average alpha party notice switch sea pass toy alien fuel pull angle weather scan"
seedPhrase = iop.generate_phrase()
#print(seedPhrase)
ark_wallet = iop.get_ark_wallet(main_wallet)
hyd_wallet = iop.get_wallet(main_wallet)
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
    asyncio.run(send_transaction(main_wallet,ark_wallet,1000000,nonce))
else:
    print("Failed to fetch data. Status code:", response.status_code)


