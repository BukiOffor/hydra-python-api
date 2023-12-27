from api.hydra import HydraChain, HydraWallet
import json


#implement your logic here
chain =  HydraChain()
wallet = HydraWallet()


# sign a witness statement with your did key
statement = {
    "name":"",
    "street": "",
    "dob": "",
    "city": "",
    "country": "",
    "zipcode": "",

}
signed_witness_statement = wallet.generate_and_sign_statement(statement,"password")
print(json.loads(signed_witness_statement))


#sign a did statement with your did key
contractStr = "A long legal document, e.g. a contract with all details"
did_statement = wallet.sign_did_statement(contractStr,"password")
print(did_statement)


{'signature': {'publicKey': 'pez3XvBcGxphYLy27QZTdqb4x5QkyZX6jYcmqjKfTvvnESm', 'bytes': 'sez6kxqVzvwVUWhSZXCXBh4dV2LzzviEPVeABKw5KY2TXDc51de8NKnVJNyS7fDHeK2zAY32z2hB4GuG6cMon2kDZvS'}, 'content': {'processId': 'cjuQR3pDJeaiRv9oCZ-fBE7T8QWpUGfjP40sAXq0bLwr-8', 'claim': {'subject': 'did:morpheus:ezbeWGSY2dqcUBqT8K7R14xr', 'content': {'address': {'nonce': 'upet_E8oeyiVv8L9g8PqF2sp61SCwqXjPqdR8QSwAPHaa', 'value': {'city': {'nonce': 'uSpLc7qTk0iQzKgvO1HMxxAZsdA1frXBPVKtcDaPNSi70', 'value': ''}, 'country': {'nonce': 'uHGzpf9UiYz9RgOUiMPx4VuYOQU7g7WYG15alzkNEJ_cD', 'value': ''}, 'street': {'nonce': 'uwZXhqUTnjM9AVxw5vuUjDq2Y4Fz9MRSriBhEYUk7lA1Z', 'value': ''}, 'zipcode': {'nonce': 'uyetQne61msTgsZSbM34IwMyKkqZFt_YtjYslc0UFD22Q', 'value': ''}}}, 'birthDate': {'nonce': 'ubRA0d4wNSP64ibW5Ta4jqJJ7r2pQwF4K8JmjeYyQo6AV', 'value': ''}, 'fullName': {'nonce': 'uinKq9qChB_sLPhdUu8nv6c1B5Ux_7jPAMouVqsjJyxhV', 'value': ''}, 'userId': '5d5d9eda-d3a9-4347-b4ae-b176b75dcf51'}}, 'constraints': {'after': None, 'before': None, 'witness': 'uVIc9J4UjKx8tRs6HUEDQElksBCtF9VnHb439boVmB9cw', 'authority': 'did:morpheus:eznp9UouL3EgGKw2Q5DnYXi2', 'content': None}, 'nonce': 'uw2w_9EYyqWqPGBGtxB31t6pmehcaC3wH-WGJ_08Tw-a8'}}
