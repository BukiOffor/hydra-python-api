use serde::{Deserialize, Serialize};
use validator::Validate;



#[derive(Validate, Deserialize, Serialize, )]
pub struct GetWallet {
    pub data: String,
    pub account: String
}

#[derive(Validate, Deserialize, Serialize, )]
pub struct GenerateTransaction{
    pub data: String,
    pub receiver: String,
    pub amount: u64,
    pub nonce: u64,
    pub password: String,
    pub account: i32,
}
#[derive(Validate, Deserialize, Serialize, )]
pub struct SignDidWallet {
    pub vault: String,
    pub password: String,
    pub data: Vec<u8>
}

#[derive(Validate, Deserialize, Serialize)]
pub struct Wallet {
    pub vault: String,
    pub password: String,
}


#[derive(Validate, Deserialize, Serialize)]
pub struct SignWitnessStatement {
    pub vault: String,
    pub password: String,
    pub data: String
}


#[derive(Validate, Deserialize, Serialize)]
pub struct WitnessStatement {
    pub data: String
}


#[derive(Validate, Deserialize, Serialize)]
pub struct MorpheusVault {
    pub phrase: String,
    pub password: String,
}


#[derive(Validate, Deserialize, Serialize, )]
pub struct AccountVault {
    pub vault: String,
    pub password: String,
    pub account: i32
}


#[derive(Validate, Deserialize, Serialize, )]
pub struct DidStatement {
    pub data: String,
    pub doc: String,
}