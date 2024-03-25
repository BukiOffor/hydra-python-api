mod handlers;
use actix_web::{HttpServer, App};
use handlers::api::{
    generate_phrase,get_wallet,generate_transaction,
    sign_did_statement,
    generate_did_by_morpheus,sign_witness_statement,
    verify_signed_statement,generate_nonce,get_morpheus_vault,
    get_hyd_vault, get_new_acc_on_vault,
    validate_statement_with_did,
};
use log::LevelFilter;



#[actix_web::main]
async fn main() -> std::io::Result<()> {
    env_logger::builder().filter_level(LevelFilter::Info).init();
    log::info!("server initialized and running at port 8088");
    log::info!("Running server at http://0.0.0.0:8088");
    HttpServer::new(move || {        
        App::new()    
            .service(generate_phrase)
            .service(get_wallet)
            .service(generate_transaction)
            .service(generate_did_by_morpheus)  
            .service(sign_did_statement)
            .service(sign_witness_statement)
            .service(verify_signed_statement)
            .service(generate_nonce)
            .service(get_morpheus_vault)
            .service(get_hyd_vault)
            .service(get_new_acc_on_vault)
            .service(validate_statement_with_did)        
        })
        .bind("127.0.0.1:8088")?
        .run()
        .await
}
