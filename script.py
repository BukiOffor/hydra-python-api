from api.hydra import HydraChain, HydraWallet
import json


#implement your logic here
chain =  HydraChain()
wallet = HydraWallet("/Users/mac/.hydra")


# sign a witness statement with your did key
statement = {
    "name":"Buki Offor",
    "street": "Brick City Estate",
    "dob": "01/03/1996",
    "city": "Abuja",
    "country": "Nigeria",
    "zipcode": "987554",

}
signed_witness_statement = wallet.generate_and_sign_statement(statement,"password")
print(json.loads(signed_witness_statement))

# Verify Signed Statement
# result = chain.verify_signed_statement(signed_witness_statement, False)
# print("The signed statement returned: ",result) #should always return true


#sign a did statement with your did key
# contractStr = "A long legal document, e.g. a contract with all details"
# did_statement = wallet.sign_did_statement(contractStr,"password")
# print(did_statement)

