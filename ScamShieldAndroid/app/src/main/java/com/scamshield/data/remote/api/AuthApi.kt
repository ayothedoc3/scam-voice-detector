package com.scamshield.data.remote.api

import com.scamshield.data.remote.dto.AuthResponse
import com.scamshield.data.remote.dto.LoginRequest
import com.scamshield.data.remote.dto.RegisterRequest
import retrofit2.http.Body
import retrofit2.http.POST

interface AuthApi {

    @POST("/api/v1/auth/register")
    suspend fun register(@Body request: RegisterRequest): AuthResponse

    @POST("/api/v1/auth/login")
    suspend fun login(@Body request: LoginRequest): AuthResponse
}
