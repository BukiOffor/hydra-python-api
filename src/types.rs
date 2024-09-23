use iop_sdk::ciphersuite::secp256k1::hyd::{self, Mainnet, Testnet};
use iop_sdk::ciphersuite::secp256k1::Secp256k1;
use iop_sdk::hydra::TransactionData;
use iop_sdk::vault::Network as HydNetwork;
use pyo3::create_exception;
use pyo3::prelude::*;
use serde::{Deserialize, Serialize};
use std::str::FromStr;

/// Possible Errors exposed by the package
#[allow(dead_code)]
#[derive(Debug)]
pub enum IopError {
    CouldNotSignTransaction,
    CouldNotSerializeHydVault,
    CouldNotDeserializeHydVault,
    CouldNotMatchNetwork,
    CouldNotCreateHydVault,
    CouldNotInitializeHydVault,
    CouldNotDeserializeMorpheusVault,
    CouldNotSerializeMorpheusVault,
    CouldNotGenerateNewAccountFromVault,
    CouldNotParseSignedStatement,
    CouldNotSerializeData,
    CouldNotSignDidStatement,
    CouldNotCreateMorpheusVault,
    CouldNotUnlockVaultWithPassword,
    CouldNotGetMorpheusVault,
    CouldNotGetMorpheusPublicKey,
    CouldNotGetHydVault,
    CouldNotGetHydPublicKey,
    CouldNotValidateDidStatement,
}

impl std::error::Error for IopError {}

impl std::fmt::Display for IopError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "Error : {}", self.message())
    }
}

impl IopError {
    pub fn message(&self) -> &'static str {
        match self {
            IopError::CouldNotSignTransaction => "could not sign transaction",
            IopError::CouldNotSerializeHydVault => "could not serialize hyd vault",
            IopError::CouldNotDeserializeHydVault => "could not deserialize hyd vault",
            Self::CouldNotMatchNetwork => {
                "could not match network, args must be [ mainnet, devnet, testnet ] "
            }
            IopError::CouldNotCreateHydVault => "could not create hyd vault",
            IopError::CouldNotInitializeHydVault => "could not initialize hyd vault",
            IopError::CouldNotDeserializeMorpheusVault => "could not deserialize morpheus vault",
            IopError::CouldNotSerializeMorpheusVault => "could not serialize morpheus vault",
            IopError::CouldNotGenerateNewAccountFromVault => {
                "could not generate new account from vault"
            }
            IopError::CouldNotParseSignedStatement => "could not parse signed statement",
            IopError::CouldNotSerializeData => "could not serialize data",
            IopError::CouldNotSignDidStatement => "could not sign did statement",
            Self::CouldNotCreateMorpheusVault => "could not create morpheus vault",
            Self::CouldNotUnlockVaultWithPassword => "could not unlock vault with password",
            IopError::CouldNotGetMorpheusVault => "could not get morpheus vault",
            IopError::CouldNotGetMorpheusPublicKey => "could not get public key, is idx correct ?",
            IopError::CouldNotGetHydVault => "could not parse parameter, is account correct ?",
            IopError::CouldNotGetHydPublicKey => "could not get public key, is idx correct ?",
            IopError::CouldNotValidateDidStatement => "could not validate did statement",
        }
    }
}

pub struct Network {
    pub network: Box<dyn HydNetwork<Suite = Secp256k1>>,
}

impl FromStr for Network {
    type Err = IopError;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s.to_lowercase().as_str() {
            "testnet" => Ok(Self {
                network: Box::new(Testnet),
            }),
            "mainnet" => Ok(Self {
                network: Box::new(Mainnet),
            }),
            "devnet" => Ok(Self {
                network: Box::new(hyd::Devnet),
            }),
            _ => Err(IopError::CouldNotMatchNetwork),
        }
    }
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
    pub transactions: Vec<TransactionData>,
}

#[pyclass]
pub struct PyIopErrorPayload {
    message: String,
}

#[pymethods]
impl PyIopErrorPayload {
    #[new]
    fn new(message: String) -> Self {
        PyIopErrorPayload { message }
    }

    #[getter]
    fn get_message(&self) -> PyResult<String> {
        Ok(self.message.clone())
    }
}

// Create the Python exception class
create_exception!(iop_python, PyIopError, pyo3::exceptions::PyException);

/// map iop error to a python error object
pub fn map_error(err: IopError) -> PyErr {
    let error_message = format!("{}", err);
    let error_payload = PyIopErrorPayload::new(error_message);
    PyErr::new::<PyIopError, _>(error_payload)
}
