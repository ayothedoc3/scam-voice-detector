package com.scamshield.domain.model

data class User(
    val id: Long,
    val email: String,
    val phoneNumber: String?,
    val createdAt: String
)
