use std::{error::Error, fmt::Display};
use async_std::task;
use serde::{Deserialize, Serialize};




use reqwest::{get, Url};



use pyo3::prelude::*;
use iop_sdk::{vault::{Bip39, Vault, hydra, PrivateKey, Network}, ciphersuite::secp256k1::{hyd,SecpPrivateKey,SecpPublicKey,SecpKeyId}};
use iop_sdk::hydra::txtype::{OptionalTransactionFields,CommonTransactionFields};
use iop_sdk::hydra::txtype::{Aip29Transaction,hyd_core::Transaction};
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

impl Display for Err{
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{:?}", self)
    }
}
impl Error for Err{}

#[allow(unused_variables)]
pub fn send_tx(
    amount: u64, manual_fee:Option<u64>, vendor_field:Option<String>, nonce:u64,
    sender_public_key:SecpPublicKey,recipient_id:&SecpKeyId
)->PyResult<String>{
    let optional = OptionalTransactionFields{amount, manual_fee,vendor_field};
    let common_fields = CommonTransactionFields{
        network: &hyd::Testnet,
        sender_public_key,
        nonce,
        optional
    };
    let transfer = Transaction::transfer(common_fields, recipient_id);
    let res = &transfer.to_data();
    Ok(res.get_id().expect("Something went wrong with the transaction"))

}
#[allow(unused_variables)]
pub async fn send_transaction(phrase:String,receiver:&str,amount:u64) -> Result<String, Box< dyn Error>>{
    //let (signer,public_key, key_id) = get_keys(phrase).unwrap();
    let signer = get_keys(phrase).unwrap();
    let recipient_id = SecpKeyId::from_p2pkh_addr(receiver, &hyd::Testnet).unwrap();

    Err(Box::new(Err::CouldNotSendTrsansaction))
}
async fn get_wallet_data<'a>(addr:String ){ 
    task::spawn(async move {
    let url = Url::parse("https://test.explorer.hydraledger.io:4705/api/v2/")
        .unwrap()
        .join(&format!("wallets/{addr}")).unwrap();
    let response = get(url).await.unwrap();
    if response.status().is_success(){
        let body = response.text().await.unwrap();
        let input = format!(r#"{body}"#);
        let object: Response = serde_json::from_str(&input).unwrap();
        let address = object.data.address;        
        println!("Response body: {}", address);
    }
}).await; 
    
} 

#[pyfunction]
pub fn generate_phrase() ->PyResult<String>{
    let bip = Bip39::new();
    let phrase = bip.generate().as_phrase().to_owned();
    Ok(phrase)
}

#[pyfunction]
#[allow(unused_variables)]
pub fn get_wallet(phrase: String) -> PyResult<String> {
    let mut vault = Vault::create(None, phrase, "password", "password").expect("Vault could not be initialised");
    let params = hydra::Parameters::new(&hyd::Testnet,0);
    hydra::Plugin::init(&mut vault, "password", &params).expect("plugin could not be initialised");
    let wallet = hydra::Plugin::get(&vault, &params).expect("wallet could not be initialized");
    let wallet_private = wallet.private("password");
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


fn get_keys(phrase: String) -> Result<(SecpPrivateKey,SecpPublicKey,SecpKeyId),()> {
    let mut vault = Vault::create(None, phrase, "password", "password").expect("Vault could not be initialised");
    let params = hydra::Parameters::new(&hyd::Testnet,0);
    hydra::Plugin::init(&mut vault, "password", &params).expect("plugin could not be initialised");
    let wallet = hydra::Plugin::get(&vault, &params).expect("wallet could not be initialized");
    let wallet_private = wallet.private("password")
        .expect("private struct could not be unwrapped")
        .key(0)
        .expect("private key could not be unwrapped").to_private_key();  
    let wallet_public = wallet.public().unwrap().key(0).unwrap().to_public_key(); 
    let wallet_key_id = wallet.public().unwrap().key(0).unwrap().to_key_id();
    Ok((wallet_private,wallet_public,wallet_key_id))
}



#[pyfunction]
pub fn call_wallet(py: Python, addr:String) -> PyResult<&PyAny> {
    pyo3_asyncio::async_std::future_into_py(py, async move {
        get_wallet_data(addr).await;
        Ok(())
    })
}


/// A Python module implemented in Rust.
#[pymodule]
fn iop_python(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(generate_phrase, m)?)?;
    m.add_function(wrap_pyfunction!(get_wallet, m)?)?;
    m.add_function(wrap_pyfunction!(get_ark_wallet, m)?)?;
    m.add_function(wrap_pyfunction!(call_wallet, m)?)?;

    


    Ok(())
}
