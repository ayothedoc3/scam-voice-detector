package com.scamshield.domain.repository

import com.scamshield.data.remote.dto.CallStatusResponse
import com.scamshield.data.remote.dto.StartProtectionResponse

interface IProtectionRepository {
    suspend fun startProtection(phoneNumber: String): Result<StartProtectionResponse>
    suspend fun stopProtection(callSid: String): Result<Unit>
    suspend fun getCallStatus(callSid: String): Result<CallStatusResponse>
}
