package com.scamshield.data.repository

import com.scamshield.data.local.PreferencesManager
import com.scamshield.data.remote.api.AuthApi
import com.scamshield.data.remote.dto.LoginRequest
import com.scamshield.data.remote.dto.RegisterRequest
import com.scamshield.domain.model.User
import com.scamshield.domain.repository.IAuthRepository
import timber.log.Timber
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class AuthRepository @Inject constructor(
    private val authApi: AuthApi,
    private val preferencesManager: PreferencesManager
) : IAuthRepository {

    override suspend fun register(
        email: String,
        password: String,
        phoneNumber: String?
    ): Result<User> {
        return try {
            val response = authApi.register(
                RegisterRequest(
                    email = email,
                    password = password,
                    phoneNumber = phoneNumber
                )
            )

            // Save token
            preferencesManager.saveAuthToken(response.accessToken)
            preferencesManager.saveUserEmail(email)

            // Map to domain model
            val user = User(
                id = response.user.id,
                email = response.user.email,
                phoneNumber = response.user.phoneNumber,
                createdAt = response.user.createdAt
            )

            Result.success(user)
        } catch (e: Exception) {
            Timber.e(e, "Registration failed")
            Result.failure(e)
        }
    }

    override suspend fun login(email: String, password: String): Result<User> {
        return try {
            val response = authApi.login(
                LoginRequest(
                    email = email,
                    password = password
                )
            )

            // Save token
            preferencesManager.saveAuthToken(response.accessToken)
            preferencesManager.saveUserEmail(email)

            // Map to domain model
            val user = User(
                id = response.user.id,
                email = response.user.email,
                phoneNumber = response.user.phoneNumber,
                createdAt = response.user.createdAt
            )

            Result.success(user)
        } catch (e: Exception) {
            Timber.e(e, "Login failed")
            Result.failure(e)
        }
    }

    override suspend fun logout() {
        preferencesManager.clearAuthToken()
    }

    override suspend fun saveToken(token: String) {
        preferencesManager.saveAuthToken(token)
    }

    override suspend fun getToken(): String? {
        return preferencesManager.getAuthToken()
    }

    override suspend fun isLoggedIn(): Boolean {
        return preferencesManager.getAuthToken() != null
    }
}
