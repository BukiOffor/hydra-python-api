use actix_web::{get,post,Responder,HttpResponse, web::Json};
use crate::handlers::types::MorpheusVault;
use crate::handlers::{utils, types::{
    GetWallet,GenerateTransaction,SignDidWallet,
     Wallet, SignWitnessStatement,WitnessStatement,
     AccountVault, DidStatement
    }} ;



#[get("/api/generate_phrase")]
pub async fn generate_phrase() -> impl Responder {
    let phrase = utils::generate_phrase().unwrap();
    HttpResponse::Ok().json(phrase)
}

#[post("/api/get_wallet")]
pub async fn get_wallet(
    body: Json<GetWallet>,
) -> impl Responder {
    let account = body.account.parse::<i32>().unwrap();
    let data = body.0.data;
    let wallet = utils::get_wallet(data, account).unwrap();
    HttpResponse::Ok().json(wallet)
}

#[post("/api/generate_transaction")]
pub async fn generate_transaction(
    body: Json<GenerateTransaction>,
) -> impl Responder {
    let req = body.0;
    let transaction = utils::generate_transaction(
        req.data, req.receiver, req.amount,
        req.nonce, req.password, req.account
    ).unwrap();
    HttpResponse::Ok().json(transaction)
}

#[post("/api/sign_did_statement")]
pub async fn sign_did_statement(
    body: Json<SignDidWallet>,
) -> impl Responder {
    let req = body.0;
    let (signature, public_key) = utils::sign_did_statement(
        req.vault, req.password, &req.data
    ).unwrap();
    HttpResponse::Ok().json(format!("signature: {signature}, public_key:{public_key}"))
}

#[post("/api/generate_did_by_morpheus")]
pub async fn generate_did_by_morpheus(
    body: Json<Wallet>,
) -> impl Responder {
    let req = body.0;
    let did = utils::generate_did_by_morpheus(
        req.vault, req.password
    ).unwrap();
    //HttpResponse::Ok().json(format!("did :{did}"))
    HttpResponse::Ok().json(did)
}


#[post("/api/sign_witness_statement")]
pub async fn sign_witness_statement(
    body: Json<SignWitnessStatement>,
) -> impl Responder {
    let req = body.0;
    let signature = utils::sign_witness_statement(
        req.vault, req.password, &req.data
    ).unwrap();
    HttpResponse::Ok().json(signature)
}



#[post("/api/verify_signed_statement")]
pub async fn verify_signed_statement(
    body: Json<WitnessStatement>,
) -> impl Responder {
    let req = body.0;
    let result = utils::verify_signed_statement(&req.data).unwrap();
    HttpResponse::Ok().json(result)
}

#[get("/api/generate_nonce")]
pub async fn generate_nonce() -> impl Responder {
    let nonce = utils::generate_nonce().unwrap();
    HttpResponse::Ok().json(nonce)
}

#[post("/api/get_morpheus_vault")]
pub async fn get_morpheus_vault(
    body: Json<MorpheusVault>, 
) -> impl Responder {
    let req = body.0;
    let morpheus_vault = utils::get_morpheus_vault(req.phrase, req.password).unwrap();
    HttpResponse::Ok().json(morpheus_vault)
}

#[post("/api/get_hyd_vault")]
pub async fn get_hyd_vault(
    body: Json<MorpheusVault>, 
) -> impl Responder {
    let req = body.0;
    let hyd_vault = utils::get_hyd_vault(req.phrase, req.password).unwrap();
    HttpResponse::Ok().json(hyd_vault)
}

#[post("/api/get_new_acc_on_vault")]
pub async fn get_new_acc_on_vault(
    body: Json<AccountVault>, 
) -> impl Responder {
    let req = body.0;
    let account = utils::get_new_acc_on_vault(req.vault, req.password, req.account).unwrap();
    HttpResponse::Ok().json(account)
}


#[post("/api/validate_statement_with_did")]

pub async fn validate_statement_with_did(
    body: Json<DidStatement>, 

) -> impl Responder {
    let req = body.0;
    let result = utils::validate_statement_with_did(&req.data, &req.doc).unwrap();
    HttpResponse::Ok().json(result)
}