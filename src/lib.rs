use std::{error::Error, fmt::Display,sync::mpsc};
use async_std::task;
use iop_sdk::hydra::TransactionData;
use serde::{Deserialize, Serialize};
use iop_sdk::vault::hydra::HydraSigner;
use reqwest::{get,Client,Url};
use pyo3::prelude::*;
use iop_sdk::{vault::{Bip39, Vault, hydra, PrivateKey, Network}, ciphersuite::secp256k1::{hyd,SecpPrivateKey,SecpPublicKey,SecpKeyId}};
use iop_sdk::hydra::txtype::{
    OptionalTransactionFields,CommonTransactionFields,
    Aip29Transaction,hyd_core::Transaction
};
//use iop_sdk::vault::Networks;

//use iop_sdk::ciphersuite::secp256k1::Secp256k1;
//use std::marker::{Send,Sync};

// struct MyType(&'static dyn Network<Suite = Secp256k1 > );

// impl MyType {
//     fn new(network: &'static dyn Network<Suite = Secp256k1>) -> Self{
//         Self(network)
//     }

//     fn network( &self, name: &str) -> & dyn Network<Suite = Secp256k1> 
//     {
//         let n = Networks::by_name(name).unwrap();
//         n 
//     }
// }

// unsafe impl Sync for MyType{}

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

#[derive(Serialize, Debug)]
struct SendTxnsReq<'a> {
    transactions: Vec<&'a TransactionData>,
}

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
pub async fn send_transaction(signed:Vec<TransactionData>) -> Result<String, Box< dyn Error>>{ 
    let url = Url::parse("https://test.explorer.hydraledger.io:4705/api/v2/transactions")?;
    let mut transactions = Vec::new();
    signed.iter().for_each(|i| transactions.push(i));
    let response = Client::new()
        .post(url)
        .json(&SendTxnsReq { transactions })
        .send()
        .await?;
    let result: String = response.text().await?;
    Ok(result)

}


#[allow(unused_variables)]
pub async fn generate_transaction<'a>(phrase:String,receiver:String,amount:u64,nonce:u64,
) -> Result<Vec<TransactionData>,()>{
    let mut transactions = Vec::new();
    let wallet_phrase = phrase.clone();
    let signer = get_keys(phrase).unwrap();
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
    Ok(transactions)
    
}
async fn _get_wallet_data(addr:String)->Result<Response,()> { 
    let (tx, rx) = mpsc::channel();
    task::spawn(async move {
    let url = Url::parse("https://test.explorer.hydraledger.io:4705/api/v2/")
        .unwrap()
        .join(&format!("wallets/{addr}")).unwrap();
    let response = get(url).await.unwrap();
    if response.status().is_success(){
        let body = response.text().await.unwrap();
        let input = format!(r#"{body}"#);
        let object: Response = serde_json::from_str(&input).unwrap();
        tx.send(object).unwrap();

    }
    }).await; 
    let result = rx.recv().unwrap();
    Ok(result)
    
} 

#[pyfunction]
pub fn generate_phrase() ->PyResult<String>{
    let bip = Bip39::new();
    let phrase = bip.generate().as_phrase().to_owned();
    Ok(phrase)
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
pub fn send_transaction_with_python(py: Python, phrase: String,receiver:String,amount:u64, nonce:u64) -> PyResult<&PyAny> {
    //let _network = Networks::by_name("testnet").unwrap();
    let signed = generate_transaction(phrase, receiver, amount, nonce);
    pyo3_asyncio::async_std::future_into_py(py, async move {
        let res = send_transaction(signed.await.unwrap()).await.unwrap();
        println!("{res}");
        Ok(res)
    })
}

/// A Python module implemented in Rust.
#[pymodule]
fn iop_python(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(generate_phrase, m)?)?;
    m.add_function(wrap_pyfunction!(get_wallet, m)?)?;
    m.add_function(wrap_pyfunction!(get_ark_wallet, m)?)?;
    m.add_function(wrap_pyfunction!(send_transaction_with_python, m)?)?;
    Ok(())
}
