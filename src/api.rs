use iop_sdk::hydra::txtype::{
    hyd_core::Transaction, Aip29Transaction, CommonTransactionFields, OptionalTransactionFields,
};
use iop_sdk::morpheus::crypto::{sign::PrivateKeySigner, Signed};
use iop_sdk::morpheus::data::{Did, WitnessStatement};
use iop_sdk::multicipher::MPublicKey;
use iop_sdk::vault::hydra::HydraSigner;
use iop_sdk::vault::morpheus::Private;
use iop_sdk::{
    ciphersuite::secp256k1::{SecpKeyId, SecpPrivateKey, SecpPublicKey},
    vault::{hydra, morpheus, Bip39, Vault},
};
use iop_sdk::{
    json_digest::Nonce264,
    morpheus::{crypto::SyncMorpheusSigner, data::DidDocument},
    vault::{hydra::Plugin, PublicKey},
};
use std::str::FromStr;

use crate::types::{IopError, Network, Transactions};

pub struct IopSdk;

impl IopSdk {
    pub fn new() -> Self {
        IopSdk
    }

    /// Generates the wallet address when passed a vault and some account details.
    ///
    /// # Example
    ///
    /// ```
    /// let sdk = IopSdk::new();
    /// let phrase = sdk.generate_phrase();
    /// let vault = sdk.get_hyd_vault(phrase, "password","mainnet",0);
    /// let address = sdk.get_wallet_address(vault,0,0,"mainnet").unwrap();
    /// assert_eq!(address.len(), 34);
    /// ```

    pub fn get_wallet_address<'a>(
        &self,
        data: String,
        account: i32,
        idx: i32,
        network: &'a str,
    ) -> Result<String, IopError> {
        let vault: Vault = match serde_json::from_str(&data) {
            Ok(vault) => vault,
            Err(_) => return Err(IopError::CouldNotInitializeHydVault),
        };
        let network = network.parse::<Network>().unwrap().network;
        let params = hydra::Parameters::new(&*network, account);
        let wallet = match hydra::Plugin::get(&vault, &params) {
            Ok(wallet) => wallet,
            Err(_) => return Err(IopError::CouldNotGetHydVault),
        };
        let wallet_address = match wallet.public().unwrap().key_mut(idx) {
            Ok(address) => address.to_p2pkh_addr(),
            Err(_) => return Err(IopError::CouldNotGetHydPublicKey),
        };
        Ok(wallet_address)
    }

    pub fn generate_transaction<'a>(
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
    ) -> Result<String, IopError> {
        let mut transactions = Vec::new();
        let signer = self.deserialize_hydra(data, password, account, idx, network)?;
        let network = network.parse::<Network>().unwrap().network;
        let recipient_id = SecpKeyId::from_p2pkh_addr(receiver.as_str(), &*network).unwrap();
        let nonce = nonce + 1;
        let optional = OptionalTransactionFields {
            amount,
            manual_fee,
            vendor_field,
        };
        let common_fields = CommonTransactionFields {
            network: &*network,
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

    /// Initializes a Hydra vault and returns account information as a JSON string. This information includes an encrypted seed and derived public key
    ///
    /// # Example
    ///
    /// ```
    /// let sdk = IopSdk::new();
    /// let phrase = sdk.generate_phrase();
    /// let account = 0;
    /// let vault = sdk.get_hyd_vault(phrase,"password","mainnet", account);
    /// ```

    pub fn get_hyd_vault(
        &self,
        phrase: String,
        password: String,
        network: String,
        account: i32,
    ) -> Result<String, IopError> {
        let mut vault = match Vault::create(None, phrase, "", &password) {
            Ok(vault) => vault,
            Err(_err) => return Err(IopError::CouldNotCreateHydVault),
        };
        let network = match network.parse::<Network>() {
            Ok(network) => network.network,
            Err(_err) => return Err(IopError::CouldNotMatchNetwork),
        };
        let params = hydra::Parameters::new(&*network, account);
        hydra::Plugin::init(&mut vault, &password, &params)
            .expect("plugin could not be initialised");
        let admin = serde_json::to_string_pretty(&vault).unwrap();
        Ok(admin)
    }

    /// Initializes a Morpheus vault and returns admin information as a JSON string.
    ///
    /// # Example
    ///
    /// ```
    /// let sdk = IopSdk::new();
    /// let phrase = sdk.generate_phrase();
    /// let vault = sdk.get_morpheus_vault(phrase,"password");
    /// ```

    pub fn get_morpheus_vault(&self, phrase: String, password: String) -> Result<String, IopError> {
        let vault = Vault::create(None, phrase, "", &password);
        match vault {
            Ok(mut vault) => {
                morpheus::Plugin::init(&mut vault, &password).unwrap();
                let admin = serde_json::to_string_pretty(&vault).unwrap();
                Ok(admin)
            }

            Err(_err) => Err(IopError::CouldNotCreateMorpheusVault),
        }
    }

    pub fn get_new_acc_on_vault(
        &self,
        data: String,
        unlock_password: String,
        account: i32,
        network: String,
    ) -> Result<String, IopError> {
        let mut vault: Vault = match serde_json::from_str(&data) {
            Ok(vault) => vault,
            Err(_err) => return Err(IopError::CouldNotDeserializeHydVault),
        };
        let network = Network::from_str(&network)?.network;
        let params = hydra::Parameters::new(&*network, account);
        match Plugin::create(&mut vault, unlock_password, &params) {
            Ok(()) => (),
            Err(_err) => return Err(IopError::CouldNotGenerateNewAccountFromVault),
        }
        let admin = serde_json::to_string_pretty(&vault).unwrap();
        Ok(admin)
    }

    fn deserialize_hydra<'a>(
        &self,
        data: String,
        unlock_password: String,
        account: i32,
        idx: i32,
        network: &'a str,
    ) -> Result<(SecpPrivateKey, SecpPublicKey, SecpKeyId), IopError> {
        let vault: Vault = match serde_json::from_str(&data) {
            Ok(vault) => vault,
            Err(_err) => return Err(IopError::CouldNotDeserializeHydVault),
        };
        let network = Network::from_str(network)?.network;
        let params = hydra::Parameters::new(&*network, account);
        let wallet = match hydra::Plugin::get(&vault, &params) {
            Ok(wallet) => wallet,
            Err(_err) => return Err(IopError::CouldNotInitializeHydVault),
        };
        let wallet_private = match wallet.private(&unlock_password) {
            Ok(mut wallet_private) => match wallet_private.key_mut(idx) {
                Ok(wallet_private) => wallet_private.to_private_key(),
                Err(_err) => return Err(IopError::CouldNotMatchNetwork),
            },
            Err(_err) => return Err(IopError::CouldNotUnlockVaultWithPassword),
        };
        let wallet_public = wallet.public().unwrap().key(idx).unwrap().to_public_key();
        let wallet_key_id = wallet.public().unwrap().key(idx).unwrap().to_key_id();
        Ok((wallet_private, wallet_public, wallet_key_id))
    }

    fn deserialize_morpheus(
        &self,
        data: String,
        unlock_password: String,
        idx: i32,
    ) -> Result<(Private, MPublicKey), IopError> {
        let vault: Vault = match serde_json::from_str(&data) {
            Ok(vault) => vault,
            Err(_err) => return Err(IopError::CouldNotDeserializeMorpheusVault),
        };
        let morpheus_plugin = match morpheus::Plugin::get(&vault) {
            Ok(m) => m,
            Err(_) => return Err(IopError::CouldNotGetMorpheusVault),
        };
        let pk = match morpheus_plugin.private(unlock_password) {
            Ok(pk) => pk,
            Err(_) => return Err(IopError::CouldNotUnlockVaultWithPassword),
        };
        let kpub = match morpheus_plugin
            .public()
            .unwrap()
            .personas()
            .unwrap()
            .key(idx)
        {
            Ok(kpub) => kpub,
            Err(_) => return Err(IopError::CouldNotGetMorpheusPublicKey),
        };
        Ok((pk, kpub))
    }

    pub fn verify_signed_statement(&self, data: &str) -> Result<bool, IopError> {
        let statement: Signed<WitnessStatement> = match serde_json::from_str(&data) {
            Ok(s) => s,
            Err(_err) => return Err(IopError::CouldNotParseSignedStatement),
        };
        let verified = statement.validate();
        Ok(verified)
    }

    pub fn sign_did_statement(
        &self,
        vault: String,
        password: String,
        data: &[u8],
        idx: i32,
    ) -> Result<(String, String), IopError> {
        let (pk, kpub) = self.deserialize_morpheus(vault, password, idx)?;
        let private_key = pk.key_by_pk(&kpub).unwrap().private_key();
        let signer = PrivateKeySigner::new(private_key);
        let response = match signer.sign(data) {
            Ok(res) => res,
            Err(_) => return Err(IopError::CouldNotSignDidStatement),
        };
        let kpub = response.0;
        let signed_data = response.1;
        Ok((signed_data.to_string(), kpub.to_string()))
    }
    /// Generates a random nonce and returns it as a string.
    ///
    /// # Example
    ///
    /// ```
    /// let sdk: IopSdk = IopSdk::new();
    /// let nonce: String = sdk.generate_nonce().unwrap();
    ///
    /// assert_eq!(nonce.len(), 45_usize);
    /// ```
    pub fn generate_nonce(&self) -> Result<String, ()> {
        let nonce = Nonce264::generate().0;
        Ok(nonce)
    }

    /// Generates a random mnemonic phrase and returns it as a string.
    ///
    /// # Example
    ///
    /// ```
    /// let sdk: IopSdk = IopSdk::new();
    /// let phrase: String = sdk.generate_phrase().unwrap();
    ///
    /// ```
    pub fn generate_phrase(&self) -> Result<String, ()> {
        let bip = Bip39::new();
        let phrase = bip.generate().as_phrase().to_owned();
        Ok(phrase)
    }

    pub fn generate_did_by_morpheus(
        &self,
        data: String,
        password: String,
        idx: i32,
    ) -> Result<String, IopError> {
        let (pk, kpub) = self.deserialize_morpheus(data, password, idx)?;
        let persona = pk.key_by_pk(&kpub).unwrap();
        let did = Did::from(persona.neuter().public_key().key_id());
        Ok(did.to_string())
    }
    pub fn get_witness_statement(&self, data: &str) -> Result<WitnessStatement, IopError> {
        let value = match serde_json::from_str(data) {
            Ok(s) => s,
            Err(_err) => return Err(IopError::CouldNotParseSignedStatement),
        };
        let digest = json_digest::canonical_json(&value).unwrap();
        let statement: WitnessStatement = serde_json::from_str(&digest).unwrap();
        Ok(statement)
    }

    pub fn sign_witness_statement(
        &self,
        vault: String,
        password: String,
        data: &str,
        idx: i32,
    ) -> Result<String, IopError> {
        let (pk, kpub) = self.deserialize_morpheus(vault, password, idx)?;
        let private_key = pk.key_by_pk(&kpub).unwrap().private_key();
        let signer = PrivateKeySigner::new(private_key);
        let statement = self.get_witness_statement(data)?;
        let response = signer.sign_witness_statement(statement).unwrap();
        let data = serde_json::to_string(&response).unwrap();
        Ok(data)
    }

    pub fn validate_statement_with_did(&self, data: &str, doc: &str) -> Result<String, IopError> {
        let did_doc: DidDocument = serde_json::from_str(doc).unwrap();
        let statement: Signed<WitnessStatement> = serde_json::from_str(data).unwrap();
        let response = match statement.validate_with_did_doc(&did_doc, None, None) {
            Ok(res) => res,
            Err(_) => return Err(IopError::CouldNotValidateDidStatement),
        };
        let data = serde_json::to_string(&response).unwrap();
        Ok(data)
    }
}

#[cfg(test)]
#[test]
fn generate_nonce() {
    let sdk = IopSdk::new();
    match sdk.generate_nonce() {
        Ok(nonce) => assert_eq!(nonce.len(), 45_usize),
        Err(_) => (),
    }
}
