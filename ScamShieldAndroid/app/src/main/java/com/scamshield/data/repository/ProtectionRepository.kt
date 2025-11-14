package com.scamshield.data.repository

import com.scamshield.data.local.PreferencesManager
import com.scamshield.data.remote.api.ProtectionApi
import com.scamshield.data.remote.dto.CallStatusResponse
import com.scamshield.data.remote.dto.StartProtectionRequest
import com.scamshield.data.remote.dto.StartProtectionResponse
import com.scamshield.data.remote.dto.StopProtectionRequest
import com.scamshield.domain.repository.IProtectionRepository
import timber.log.Timber
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class ProtectionRepository @Inject constructor(
    private val protectionApi: ProtectionApi,
    private val preferencesManager: PreferencesManager
) : IProtectionRepository {

    override suspend fun startProtection(phoneNumber: String): Result<StartProtectionResponse> {
        return try {
            val token = preferencesManager.getAuthToken()
                ?: return Result.failure(Exception("Not authenticated"))

            val response = protectionApi.startProtection(
                token = "Bearer $token",
                request = StartProtectionRequest(userPhone = phoneNumber)
            )

            Result.success(response)
        } catch (e: Exception) {
            Timber.e(e, "Failed to start protection")
            Result.failure(e)
        }
    }

    override suspend fun stopProtection(callSid: String): Result<Unit> {
        return try {
            val token = preferencesManager.getAuthToken()
                ?: return Result.failure(Exception("Not authenticated"))

            protectionApi.stopProtection(
                token = "Bearer $token",
                request = StopProtectionRequest(callSid = callSid)
            )

            Result.success(Unit)
        } catch (e: Exception) {
            Timber.e(e, "Failed to stop protection")
            Result.failure(e)
        }
    }

    override suspend fun getCallStatus(callSid: String): Result<CallStatusResponse> {
        return try {
            val token = preferencesManager.getAuthToken()
                ?: return Result.failure(Exception("Not authenticated"))

            val response = protectionApi.getCallStatus(
                token = "Bearer $token",
                callSid = callSid
            )

            Result.success(response)
        } catch (e: Exception) {
            Timber.e(e, "Failed to get call status")
            Result.failure(e)
        }
    }
}
