package com.scamshield.domain.repository

import com.scamshield.domain.model.User

interface IAuthRepository {
    suspend fun register(email: String, password: String, phoneNumber: String?): Result<User>
    suspend fun login(email: String, password: String): Result<User>
    suspend fun logout()
    suspend fun saveToken(token: String)
    suspend fun getToken(): String?
    suspend fun isLoggedIn(): Boolean
}
