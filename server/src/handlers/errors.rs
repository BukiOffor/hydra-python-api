#![cfg_attr(debug_assertions, allow(dead_code, unused_imports))]
use actix_web::{
    http::{header::ContentType, StatusCode},
    HttpResponse, ResponseError,
};

use derive_more::Display;
#[derive(Debug, Display)]
pub enum GateWayError {
    TokenIdNotFound,
    InsufficientFunds,
    InvalidPrice,
    ParseParams,
    NonceAlreadyUsed,
    WrongContract,
    TransactionSimulationError
}

impl ResponseError for GateWayError {
    fn error_response(&self) -> HttpResponse<actix_web::body::BoxBody> {
        HttpResponse::build(self.status_code())
            .insert_header(ContentType::json())
            .body(self.to_string())
    }

    fn status_code(&self) -> StatusCode {
        match self {
            GateWayError::InsufficientFunds => StatusCode::FAILED_DEPENDENCY,
            GateWayError::InvalidPrice => StatusCode::NOT_ACCEPTABLE,
            GateWayError::TokenIdNotFound => StatusCode::NOT_FOUND,
            GateWayError::NonceAlreadyUsed => StatusCode::FORBIDDEN,
            GateWayError::ParseParams => StatusCode::UNPROCESSABLE_ENTITY,
            GateWayError::TransactionSimulationError => StatusCode::BAD_REQUEST,
            GateWayError::WrongContract => StatusCode::BAD_GATEWAY
        }
    }
}
