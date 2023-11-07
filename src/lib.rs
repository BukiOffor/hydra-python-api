use pyo3::prelude::*;
use iop_sdk::{vault::{Bip39, Vault, hydra}, ciphersuite::secp256k1::{hyd,SecpPrivateKey,SecpPublicKey,SecpKeyId}};
use iop_sdk::hydra::txtype::{OptionalTransactionFields,CommonTransactionFields};
use iop_sdk::hydra::txtype::{Aip29Transaction,hyd_core::Transaction};

//use std::error::Error;


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

#[pyfunction]
pub fn generate_phrase() ->PyResult<String>{
    let bip = Bip39::new();
    let phrase = bip.generate().as_phrase().to_owned();
    //println!("{}", phrase);
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
        .key(0).expect("Error while getting wallet Address").to_p2pkh_addr();
    Ok(wallet_address)
}

pub fn get_signer(phrase: String) -> Result<SecpPrivateKey,()> {
    let mut vault = Vault::create(None, phrase, "password", "password").expect("Vault could not be initialised");
    let params = hydra::Parameters::new(&hyd::Testnet,0);
    hydra::Plugin::init(&mut vault, "password", &params).expect("plugin could not be initialised");
    let wallet = hydra::Plugin::get(&vault, &params).expect("wallet could not be initialized");
    let wallet_private = wallet.private("password")
        .expect("private struct could not be unwrapped")
        .key(0)
        .expect("private key could not be unwrapped").to_private_key();    
    Ok(wallet_private)
}




/// A Python module implemented in Rust.
#[pymodule]
fn iop_python(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(generate_phrase, m)?)?;
    m.add_function(wrap_pyfunction!(get_wallet, m)?)?;

    Ok(())
}
