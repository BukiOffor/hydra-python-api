use std::{error::Error, fmt::Display};
use iop_sdk::{hydra::TransactionData, morpheus::crypto::SyncMorpheusSigner, json_digest::Nonce264};
use serde::{Deserialize, Serialize};
use iop_sdk::vault::hydra::HydraSigner;
use pyo3::prelude::*;
use iop_sdk::{vault::{Bip39, Vault, hydra, PrivateKey, Network,morpheus,PublicKey}, ciphersuite::secp256k1::{hyd,SecpPrivateKey,SecpPublicKey,SecpKeyId}};
use iop_sdk::hydra::txtype::{
    OptionalTransactionFields,CommonTransactionFields,
    Aip29Transaction,hyd_core::Transaction
};

use iop_sdk::multicipher::MKeyId;
use iop_sdk::morpheus::data::{Did,WitnessStatement};
use iop_sdk::morpheus::crypto::{Signed,sign::PrivateKeySigner};



//=================================================MILE STONE TWO STARTS HERE==========================================================
#[pyfunction]
pub fn verify_signed_statement(data:&str)->PyResult<bool>{
    let statement:Signed<WitnessStatement> = serde_json::from_str(data).unwrap(); 
    let verified = statement.validate();
    Ok(verified)
} 

#[pyfunction]
pub fn generate_nonce()->PyResult<String>{
    let nonce = Nonce264::generate().0; 
    Ok(nonce)
}


#[pyfunction]
pub fn generate_phrase() ->PyResult<String>{
    let bip = Bip39::new();
    let phrase = bip.generate().as_phrase().to_owned();
    Ok(phrase)
}

#[pyfunction]
pub fn generate_did_by_secp_key_id(phrase: String,password:String) ->PyResult<String>{
    let keys: (SecpPrivateKey, SecpPublicKey, SecpKeyId) = get_keys(phrase, password).unwrap();
    let m_key = MKeyId::from(keys.2);
    let did = Did::new(m_key);
    let key = did.to_string();
    Ok(key)
}



#[pyfunction]
pub fn generate_did_by_morpheus(phrase: String,password:String) ->PyResult<String>{
    let v_password = password.clone();
    let mut vault = Vault::create(None, phrase, &password, &password).expect("Vault could not be initialised");
    morpheus::Plugin::init(&mut vault, v_password).unwrap();
    let morpheus_plugin = morpheus::Plugin::get(&vault).unwrap();
    let pk = morpheus_plugin.private(password).unwrap();
    let kpub = morpheus_plugin.public().unwrap().personas().unwrap().key(0).unwrap();
    let persona = pk.key_by_pk(&kpub).unwrap();
    let did = Did::from(persona.neuter().public_key().key_id());    
    Ok(did.to_string())
}

#[allow(unused_variables)]
pub fn get_witness_statement(data: &str)->Result<WitnessStatement,()>{
    let statement:WitnessStatement = serde_json::from_str(data).unwrap(); 
    Ok(statement)
}

#[pyfunction]
pub fn sign_did_statement(phrase: String,password:String, data: &[u8]) ->PyResult<(String,String)>{
    let v_password = password.clone();
    let mut vault = Vault::create(None, phrase, &password, &password).expect("Vault could not be initialised");
    morpheus::Plugin::init(&mut vault, v_password).unwrap();
    let morpheus_plugin = morpheus::Plugin::get(&vault).unwrap();
    let private_key = morpheus_plugin.private(password).unwrap()
        .resources().unwrap().key(0)
        .unwrap().private_key();
    let signer = PrivateKeySigner::new(private_key);
    let response = signer.sign(data).unwrap();
    let kpub = response.0;
    let signed_data = response.1;
    Ok((signed_data.to_string(),kpub.to_string()))
}

#[pyfunction]
pub fn sign_witness_statement(phrase: String,password:String,data: &str)->PyResult<String>{
    let v_password = password.clone();
    let mut vault = Vault::create(None, phrase, &password, &password).expect("Vault could not be initialised");
    morpheus::Plugin::init(&mut vault, v_password).unwrap();
    let morpheus_plugin = morpheus::Plugin::get(&vault).unwrap();
    let kpub = morpheus_plugin.public().unwrap().personas().unwrap().key(0).unwrap();
    let private_key = morpheus_plugin.private(password).unwrap()
        .key_by_pk(&kpub).unwrap().private_key();
    let signer = PrivateKeySigner::new(private_key);
    let statement = get_witness_statement(data).unwrap();
    let response = signer.sign_witness_statement(statement).unwrap();
    let data = serde_json::to_string(&response).unwrap();
    Ok(data)

}

//=================================================MILE STONE TWO ENDS HERE==========================================================


#[derive(Debug)]
pub enum Err{
    CouldNotSendTrsansaction
}
#[derive(Serialize, Deserialize, Debug)]
#[allow(non_snake_case)]
pub struct Data {
    address:String,
    nonce:String,
    balance:String,
    isDelegate:bool,
    isResigned:bool
    }



#[derive(Serialize, Deserialize, Debug)]
pub struct Response {data: Data}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct Transactions {
    transactions: Vec<TransactionData>
}


impl Display for Err {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{:?}", self)
    }
}
impl Error for Err{}

#[derive(Serialize, Debug)]
struct SendTxnsReq<'a> {
    transactions: Vec<&'a TransactionData>,
}


#[pyfunction]
#[allow(unused_variables)]
pub fn generate_transaction<'a>(
    phrase:String,receiver:String,amount:u64,nonce:u64,password:String
) -> PyResult<String>{
    let mut transactions = Vec::new();
    let signer = get_keys(phrase,password).unwrap();
    let recipient_id = SecpKeyId::from_p2pkh_addr(receiver.as_str(), &hyd::Testnet).unwrap();
    let nonce = nonce +1 ;
    let optional = OptionalTransactionFields{amount, manual_fee:None,vendor_field:None};
    let common_fields = CommonTransactionFields{
        network:&hyd::Testnet,
        sender_public_key: signer.1,
        nonce,
        optional
    };
    let unsigned = Transaction::transfer(common_fields, &recipient_id);
    let mut signed = unsigned.to_data();
    signer.0.sign_hydra_transaction(&mut signed).unwrap();
    transactions.push(signed);
    let data = serde_json::to_string(&Transactions{transactions}).unwrap();
    Ok(data)    
}



#[pyfunction]
#[allow(unused_variables)]
pub fn get_wallet(phrase: String, password:String) -> PyResult<String> {
    let mut vault = Vault::create(None, phrase, &password, &password).expect("Vault could not be initialised");
    let params = hydra::Parameters::new(&hyd::Testnet,0);
    hydra::Plugin::init(&mut vault, &password, &params).expect("plugin could not be initialised");
    let wallet = hydra::Plugin::get(&vault, &params).expect("wallet could not be initialized");
    let wallet_private = wallet.private(&password);
    let wallet_address = wallet.public()
        .expect("ERROR while unwrapping public key")
        .key_mut(0).expect("Error while getting wallet Address").to_p2pkh_addr();
    Ok(wallet_address)
}

#[pyfunction]
#[allow(unused_variables)]
pub fn get_ark_wallet(phrase:String) -> PyResult<String> {
    let network = &hyd::Testnet;
    let ark_pk = SecpPrivateKey::from_ark_passphrase(phrase).unwrap();
    let ark_kpub = ark_pk.public_key();
    let ark_key_id = ark_kpub.ark_key_id();
    let ark_address = ark_key_id.to_p2pkh_addr(network.p2pkh_addr());
    Ok(ark_address)
}
fn get_keys(phrase: String, password:String) -> Result<(SecpPrivateKey,SecpPublicKey,SecpKeyId),()> {
    let mut vault = Vault::create(None, phrase, &password, &password).expect("Vault could not be initialised");
    let params = hydra::Parameters::new(&hyd::Testnet,0);
    hydra::Plugin::init(&mut vault, &password, &params).expect("plugin could not be initialised");
    let wallet = hydra::Plugin::get(&vault, &params).expect("wallet could not be initialized");
    let wallet_private = wallet.private(&password)
        .expect("private struct could not be unwrapped")
        .key(0)
        .expect("private key could not be unwrapped").to_private_key();  
    let wallet_public = wallet.public().unwrap().key(0).unwrap().to_public_key(); 
    let wallet_key_id = wallet.public().unwrap().key(0).unwrap().to_key_id();
    Ok((wallet_private,wallet_public,wallet_key_id))
}

#[pyfunction]
pub fn get_public_key(phrase: String, password:String) -> PyResult<String> {
    let mut vault = Vault::create(None, phrase, &password, &password).expect("Vault could not be initialised");
    let params = hydra::Parameters::new(&hyd::Testnet,0);
    hydra::Plugin::init(&mut vault, &password, &params).expect("plugin could not be initialised");
    let wallet = hydra::Plugin::get(&vault, &params).expect("wallet could not be initialized");
    let  wallet_public = wallet.public().unwrap().key(0).unwrap().to_public_key().to_string(); 
    Ok(wallet_public)
}


/// A Python module implemented in Rust.
#[pymodule]
fn iop_python(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(generate_phrase, m)?)?;
    m.add_function(wrap_pyfunction!(get_wallet, m)?)?;
    m.add_function(wrap_pyfunction!(get_ark_wallet, m)?)?;
    m.add_function(wrap_pyfunction!(generate_transaction, m)?)?;
    m.add_function(wrap_pyfunction!(get_public_key, m)?)?;
    m.add_function(wrap_pyfunction!(generate_did_by_morpheus, m)?)?;
    m.add_function(wrap_pyfunction!(generate_did_by_secp_key_id, m)?)?;
    m.add_function(wrap_pyfunction!(sign_did_statement, m)?)?;
    m.add_function(wrap_pyfunction!(sign_witness_statement, m)?)?;
    m.add_function(wrap_pyfunction!(verify_signed_statement, m)?)?;
    m.add_function(wrap_pyfunction!(generate_nonce, m)?)?;




    Ok(())
}
