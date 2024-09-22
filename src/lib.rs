mod types;
mod api;

use crate::api::IopSdk;
use crate::types::{PyIopErrorPayload, map_error};
use pyo3::prelude::*;



#[pyclass]
struct IopPython {
    sdk: IopSdk,
}


#[pymethods]
impl IopPython {
    #[new]
    fn new() -> PyResult<IopPython> {
        Ok(IopPython {
            sdk: IopSdk::new(),
        })
    }

    fn generate_phrase(&self) -> PyResult<String> {
        let phrase = self.sdk.generate_phrase();
        Ok(phrase.unwrap())
    }

    fn get_wallet_address<'a>(&self, data: String, account: i32, idx:i32, network: &'a str) -> PyResult<String> {
        match self.sdk.get_wallet_address(data, account, idx, network) {
            Ok(address) => Ok(address),
            Err(err) => Err(map_error(err)),
        }
    }

    fn generate_transaction<'a>(
        &self,
        data: String,
        receiver: String,
        amount: u64,
        nonce: u64,
        password: String,
        account: i32,
        idx:i32,
        network: &'a str,
        vendor_field: Option<String>,
        manual_fee: Option<u64>,
    ) -> PyResult<String> {
        match self.sdk.generate_transaction(
            data,receiver,amount,
            nonce,password,account,idx,
            network,vendor_field,manual_fee
        )
        {
            Ok(signed_transaction) => Ok(signed_transaction),
            Err(err) => Err(map_error(err))
        }
    }

    fn generate_did_by_morpheus(&self,data: String, password: String, idx:i32) -> PyResult<String> {
        match self.sdk.generate_did_by_morpheus(data,password,idx) {
            Ok(res) => Ok(res),
            Err(err) => Err(map_error(err))
        }
    }

    fn sign_did_statement(&self,vault: String,password: String, data: &[u8], idx: i32 ) -> PyResult<(String, String)>{
        match self.sdk.sign_did_statement(vault,password,data,idx) {
            Ok(res) => Ok(res),
            Err(err) => Err(map_error(err))
        }
    }

    fn sign_witness_statement(&self, vault: String, password: String, data: &str, idx:i32) -> PyResult<String> {
        match self.sdk.sign_witness_statement(vault,password,data,idx){
            Ok(response) => Ok(response),
            Err(err) => Err(map_error(err))
        }
    }

    fn verify_signed_statement( &self, data: &str) -> PyResult<bool> {
        match self.sdk.verify_signed_statement(data) {
            Ok(response) => Ok(response),
            Err(err) => Err(map_error(err))
        }
    }

    fn generate_nonce(&self) -> PyResult<String> {
        let nonce = self.sdk.generate_nonce();
        Ok(nonce.unwrap())
    }

    fn get_morpheus_vault( &self, phrase: String, password: String) -> PyResult<String> {
        match self.sdk.get_morpheus_vault(phrase, password) {
            Ok(vault) => Ok(vault),
            Err(err) => Err(map_error(err))
        }
    }

    fn get_hyd_vault( &self, phrase: String, password: String, network: String, account: i32) -> PyResult<String> {
        match self.sdk.get_hyd_vault(phrase,password,network,account){
            Ok(vault) => Ok(vault),
            Err(err) => Err(map_error(err))
        }
    }

    fn get_new_acc_on_vault(
        &self,
        data: String,
        unlock_password: String,
        account: i32,
        network: String
    ) -> PyResult<String> {
        match self.sdk.get_new_acc_on_vault(data,unlock_password,account,network) {
            Ok(vault) => Ok(vault),
            Err(err) => Err(map_error(err))
        }
    }

    fn validate_statement_with_did(&self, data: &str, doc: &str) -> PyResult<String> {
        match self.sdk.validate_statement_with_did(data,doc){
            Ok(response) => Ok(response),
            Err(err) => Err(map_error(err))
        }
    }

} 




/// Python module
#[pymodule]
fn iop_python(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<IopPython>()?;
    m.add_class::<PyIopErrorPayload>()?;
    Ok(())
}