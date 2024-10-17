mod api;
mod types;

use std::str::FromStr;

use crate::api::IopSdk;
use crate::types::{map_error, PyIopErrorPayload};
use iop_sdk::ciphersuite::secp256k1::SecpPublicKey;
use pyo3::prelude::*;

#[pyclass]
struct IopPython {
    sdk: IopSdk,
}

#[pymethods]
impl IopPython {
    #[new]
    fn new() -> PyResult<IopPython> {
        Ok(IopPython { sdk: IopSdk::new() })
    }
    /// generates a random 24 word mnemonic.
    fn generate_phrase(&self) -> PyResult<String> {
        let phrase = self.sdk.generate_phrase();
        Ok(phrase.unwrap())
    }

    /// Computes the wallet address when given a vault and an account index.
    fn get_wallet_address<'a>(
        &self,
        data: String,
        account: i32,
        idx: i32,
        network: &'a str,
    ) -> PyResult<String> {
        match self.sdk.get_wallet_address(data, account, idx, network) {
            Ok(address) => Ok(address),
            Err(err) => Err(map_error(err)),
        }
    }

    /// Signs a layer 1 transaction and returns a valid signature
    fn sign_transaction<'a>(
        &self,
        data: String,
        receiver: String,
        amount: u64,
        nonce: u64,
        password: String,
        account: i32,
        idx: i32,
        network: &'a str,
        vendor_field: Option<String>,
        manual_fee: Option<u64>,
    ) -> PyResult<String> {
        match self.sdk.sign_transaction(
            data,
            receiver,
            amount,
            nonce,
            password,
            account,
            idx,
            network,
            vendor_field,
            manual_fee,
        ) {
            Ok(signed_transaction) => Ok(signed_transaction),
            Err(err) => Err(map_error(err)),
        }
    }

    /// computes a did from a morpheus vault
    fn generate_did_by_morpheus(
        &self,
        data: String,
        password: String,
        idx: i32,
    ) -> PyResult<String> {
        match self.sdk.generate_did_by_morpheus(data, password, idx) {
            Ok(res) => Ok(res),
            Err(err) => Err(map_error(err)),
        }
    }

    /// signs a did statement when given a vault and a valid password
    fn sign_did_statement(
        &self,
        vault: String,
        password: String,
        data: &[u8],
        idx: i32,
    ) -> PyResult<(String, String)> {
        match self.sdk.sign_did_statement(vault, password, data, idx) {
            Ok(res) => Ok(res),
            Err(err) => Err(map_error(err)),
        }
    }

    /// signs a witness statement when given a vault and a valid password
    fn sign_witness_statement(
        &self,
        vault: String,
        password: String,
        data: &str,
        idx: i32,
    ) -> PyResult<String> {
        match self.sdk.sign_witness_statement(vault, password, data, idx) {
            Ok(response) => Ok(response),
            Err(err) => Err(map_error(err)),
        }
    }

    /// verify a signed statement
    fn verify_signed_statement(&self, data: &str) -> PyResult<bool> {
        match self.sdk.verify_signed_statement(data) {
            Ok(response) => Ok(response),
            Err(err) => Err(map_error(err)),
        }
    }

    /// generates a random nonce
    fn generate_nonce(&self) -> PyResult<String> {
        let nonce = self.sdk.generate_nonce();
        Ok(nonce.unwrap())
    }

    /// creates a morpheus vault
    fn get_morpheus_vault(&self, phrase: String, password: String) -> PyResult<String> {
        match self.sdk.get_morpheus_vault(phrase, password) {
            Ok(vault) => Ok(vault),
            Err(err) => Err(map_error(err)),
        }
    }

    /// creates a hyd vault
    fn get_hyd_vault(
        &self,
        phrase: String,
        password: String,
        network: String,
        account: i32,
    ) -> PyResult<String> {
        match self.sdk.get_hyd_vault(phrase, password, network, account) {
            Ok(vault) => Ok(vault),
            Err(err) => Err(map_error(err)),
        }
    }

    /// derives a new account from an existing vault
    fn get_new_acc_on_vault(
        &self,
        data: String,
        unlock_password: String,
        account: i32,
        network: String,
    ) -> PyResult<String> {
        match self
            .sdk
            .get_new_acc_on_vault(data, unlock_password, account, network)
        {
            Ok(vault) => Ok(vault),
            Err(err) => Err(map_error(err)),
        }
    }

    /// validate a statement with did
    fn validate_statement_with_did(&self, data: &str, doc: &str) -> PyResult<String> {
        match self.sdk.validate_statement_with_did(data, doc) {
            Ok(response) => Ok(response),
            Err(err) => Err(map_error(err)),
        }
    }
    fn vote<'a>(
        &self,
        data: String,
        nonce: u64,
        password: String,
        account: i32,
        idx: i32,
        network: &'a str,
        delegate: String,
        vendor_field: Option<String>,
        manual_fee: Option<u64>,
    ) -> PyResult<String> {
        match self.sdk.vote(
            data,
            nonce,
            password,
            account,
            idx,
            network,
            delegate,
            vendor_field,
            manual_fee,
        ) {
            Ok(response) => Ok(response),
            Err(err) => Err(map_error(err)),
        }
    }

    fn unvote<'a>(
        &self,
        data: String,
        nonce: u64,
        password: String,
        account: i32,
        idx: i32,
        network: &'a str,
        delegate: String,
        vendor_field: Option<String>,
        manual_fee: Option<u64>,
    ) -> PyResult<String> {
        let delegate = SecpPublicKey::from_str(delegate.as_str()).unwrap();
        match self.sdk.unvote(
            data,
            nonce,
            password,
            account,
            idx,
            network,
            &delegate,
            vendor_field,
            manual_fee,
        ) {
            Ok(response) => Ok(response),
            Err(err) => Err(map_error(err)),
        }
    }
    fn register_delegate<'a>(
        &self,
        data: String,
        nonce: u64,
        password: String,
        account: i32,
        idx: i32,
        network: &'a str,
        delegate: String,
        vendor_field: Option<String>,
        manual_fee: Option<u64>,
    ) -> PyResult<String> {
        match self.sdk.register_delegate(
            data,
            nonce,
            password,
            account,
            idx,
            network,
            &delegate,
            vendor_field,
            manual_fee,
        ) {
            Ok(response) => Ok(response),
            Err(err) => Err(map_error(err)),
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
