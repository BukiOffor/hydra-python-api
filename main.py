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


