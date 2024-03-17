
use iop_sdk::hydra::txtype::{
    hyd_core::Transaction, Aip29Transaction, CommonTransactionFields, OptionalTransactionFields,
};
use iop_sdk::vault::hydra::HydraSigner;
use iop_sdk::{
    ciphersuite::secp256k1::{hyd, SecpKeyId, SecpPrivateKey, SecpPublicKey},
    vault::{hydra, morpheus, Bip39, Vault},
};
use iop_sdk::{
    hydra::TransactionData,
    json_digest::Nonce264,
    morpheus::{crypto::SyncMorpheusSigner, data::DidDocument},
    vault::{hydra::Plugin, PublicKey},
};
use serde::{Deserialize, Serialize};
use std::{error::Error, fmt::Display};

//use iop_sdk::multicipher::MKeyId;
//use iop_sdk::vault::{PrivateKey,Network,};
use iop_sdk::morpheus::crypto::{sign::PrivateKeySigner, Signed};
use iop_sdk::morpheus::data::{Did, WitnessStatement};
use iop_sdk::multicipher::MPublicKey;
use iop_sdk::vault::morpheus::Private;


#[derive(Debug)]
pub enum Err {
    CouldNotDeserialiseVault
}



#[derive(Serialize, Deserialize, Debug)]
#[allow(non_snake_case)]
pub struct Data {
    address: String,
    nonce: String,
    balance: String,
    isDelegate: bool,
    isResigned: bool,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct Response {
    data: Data,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct Transactions {
    transactions: Vec<TransactionData>,
}

impl Display for Err {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{:?}", self)
    }
}
impl Error for Err {}

#[derive(Serialize, Debug)]
struct SendTxnsReq<'a> {
    transactions: Vec<&'a TransactionData>,
}

#[allow(unused_variables)]
pub fn get_hyd_vault(phrase: String, password: String) -> Result<String,Err> {
    let mut vault =
        Vault::create(None, phrase, &password, &password).expect("Vault could not be initialised");
    let params = hydra::Parameters::new(&hyd::Testnet, 0);
    hydra::Plugin::init(&mut vault, &password, &params).expect("plugin could not be initialised");
    let wallet = hydra::Plugin::get(&vault, &params).expect("wallet could not be initialized");
    let admin = serde_json::to_string_pretty(&vault).unwrap();
    Ok(admin)
}

#[allow(unused_variables)]
pub fn get_morpheus_vault(phrase: String, password: String) -> Result<String,Err> {
    //let mut vault = Vault::create(None, phrase, &password, &password).expect("Vault could not be initialised");
    let vault = Vault::create(None, phrase, &password, &password);
    match vault {
        Ok(mut vault) => {
            morpheus::Plugin::init(&mut vault, &password).unwrap();
            let admin = serde_json::to_string_pretty(&vault).unwrap();
             Ok(admin)
            },
        
        Err(_err) => {
            Err(Err::CouldNotDeserialiseVault)
        }
        }
    }
    

#[allow(unused_variables)]
pub fn get_new_acc_on_vault(
    data: String,
    unlock_password: String,
    account: i32,
) -> Result<String,Err> {
    let mut vault: Vault = serde_json::from_str(&data).unwrap();
    let params = hydra::Parameters::new(&hyd::Testnet, account);
    Plugin::create(&mut vault, unlock_password, &params).expect("vault could not be created");
    let admin = serde_json::to_string_pretty(&vault).unwrap();
    Ok(admin)
}

#[allow(unused)]
fn deserialize_hydra(
    data: String,
    unlock_password: String,
    account: i32,
) -> Result<(SecpPrivateKey, SecpPublicKey, SecpKeyId), ()> {
    let vault: Vault = serde_json::from_str(&data).unwrap();
    let params = hydra::Parameters::new(&hyd::Testnet, account);
    let wallet = hydra::Plugin::get(&vault, &params).expect("wallet could not be gotten");
    let wallet_private = wallet
        .private(&unlock_password)
        .expect("private struct could not be unwrapped")
        .key_mut(0)
        .expect("private key could not be unwrapped")
        .to_private_key();
    let wallet_public = wallet.public().unwrap().key(0).unwrap().to_public_key();
    let wallet_key_id = wallet.public().unwrap().key(0).unwrap().to_key_id();
    Ok((wallet_private, wallet_public, wallet_key_id))
}

#[allow(unused)]
fn deserialize_morpheus(
    data: String,
    unlock_password: String,
) -> Result<(Private, MPublicKey), ()> {
    let mut vault: Vault = serde_json::from_str(&data).unwrap();
    let morpheus_plugin = morpheus::Plugin::get(&vault).unwrap();
    let pk = morpheus_plugin.private(unlock_password).unwrap();
    let kpub = morpheus_plugin
        .public()
        .unwrap()
        .personas()
        .unwrap()
        .key(0)
        .unwrap();
    let persona = pk.key_by_pk(&kpub).unwrap();
    Ok((pk, kpub))
}

//=================================================MILE STONE TWO STARTS HERE==========================================================
pub fn verify_signed_statement(data: &str) -> Result<bool, Err> {
    let statement: Signed<WitnessStatement> = serde_json::from_str(data).unwrap();
    let verified = statement.validate();
    Ok(verified)
}

pub fn generate_nonce() -> Result<String, Err> {
    let nonce = Nonce264::generate().0;
    Ok(nonce)
}

pub fn generate_phrase() -> Result<String, Err> {
    let bip = Bip39::new();
    let phrase = bip.generate().as_phrase().to_owned();
    Ok(phrase)
}

pub fn generate_did_by_morpheus(data: String, password: String) -> Result<String, Err> {
    let (pk, kpub) = deserialize_morpheus(data, password).unwrap();
    let persona = pk.key_by_pk(&kpub).unwrap();
    let did = Did::from(persona.neuter().public_key().key_id());
    Ok(did.to_string())
}

#[allow(unused_variables)]
pub fn get_witness_statement(data: &str) -> Result<WitnessStatement, ()> {
    let value = serde_json::from_str(data).unwrap();
    let digest = json_digest::canonical_json(&value).unwrap();
    let statement: WitnessStatement = serde_json::from_str(&digest).unwrap();
    Ok(statement)
}

pub fn sign_did_statement(
    vault: String,
    password: String,
    data: &[u8],
) -> Result<(String, String), Err> {
    let (pk, kpub) = deserialize_morpheus(vault, password).unwrap();
    let private_key = pk.key_by_pk(&kpub).unwrap().private_key();
    let signer = PrivateKeySigner::new(private_key);
    let response = signer.sign(data).unwrap();
    let kpub = response.0;
    let signed_data = response.1;
    Ok((signed_data.to_string(), kpub.to_string()))
}

pub fn sign_witness_statement(vault: String, password: String, data: &str) -> Result<String, Err> {
    let (pk, kpub) = deserialize_morpheus(vault, password).unwrap();
    let private_key = pk.key_by_pk(&kpub).unwrap().private_key();
    let signer = PrivateKeySigner::new(private_key);
    let statement = get_witness_statement(data).unwrap();
    let response = signer.sign_witness_statement(statement).unwrap();
    let data = serde_json::to_string(&response).unwrap();
    Ok(data)
}

//================================================= MILE STONE TWO ENDS HERE ==========================================================

#[allow(unused_variables)]
pub fn generate_transaction<'a>(
    data: String,
    receiver: String,
    amount: u64,
    nonce: u64,
    password: String,
    account: i32,
) -> Result<String,Err> {
    let mut transactions = Vec::new();
    let signer = deserialize_hydra(data, password, account).unwrap();
    let recipient_id = SecpKeyId::from_p2pkh_addr(receiver.as_str(), &hyd::Testnet).unwrap();
    let nonce = nonce + 1;
    let optional = OptionalTransactionFields {
        amount,
        manual_fee: None,
        vendor_field: None,
    };
    let common_fields = CommonTransactionFields {
        network: &hyd::Testnet,
        sender_public_key: signer.1,
        nonce,
        optional,
    };
    let unsigned = Transaction::transfer(common_fields, &recipient_id);
    let mut signed = unsigned.to_data();
    signer.0.sign_hydra_transaction(&mut signed).unwrap();
    transactions.push(signed);
    let data = serde_json::to_string(&Transactions { transactions }).unwrap();
    Ok(data)
}

#[allow(unused_variables)]
pub fn get_wallet(data: String, account: i32) -> Result<String, Err> {
    let vault: Vault = serde_json::from_str(&data).unwrap();
    let params = hydra::Parameters::new(&hyd::Testnet, account);
    let wallet = hydra::Plugin::get(&vault, &params).expect("wallet could not be gotten");
    let wallet_address = wallet.public().unwrap().key_mut(0).unwrap().to_p2pkh_addr();
    Ok(wallet_address)
}

pub fn validate_statement_with_did(data: &str, doc: &str) -> Result<String, Err> {
    let did_doc: DidDocument = serde_json::from_str(doc).unwrap();
    let statement: Signed<WitnessStatement> = serde_json::from_str(data).unwrap();
    let response = statement
        .validate_with_did_doc(&did_doc, None, None)
        .expect("Validation could not be ascertained");
    let data = serde_json::to_string(&response).unwrap();
    Ok(data)
}
