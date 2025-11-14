package com.scamshield.data.remote.api

import com.scamshield.data.remote.dto.CallStatusResponse
import com.scamshield.data.remote.dto.StartProtectionRequest
import com.scamshield.data.remote.dto.StartProtectionResponse
import com.scamshield.data.remote.dto.StopProtectionRequest
import retrofit2.http.*

interface ProtectionApi {

    @POST("/api/v1/protection/start")
    suspend fun startProtection(
        @Header("Authorization") token: String,
        @Body request: StartProtectionRequest
    ): StartProtectionResponse

    @POST("/api/v1/protection/stop")
    suspend fun stopProtection(
        @Header("Authorization") token: String,
        @Body request: StopProtectionRequest
    )

    @GET("/api/v1/protection/status/{callSid}")
    suspend fun getCallStatus(
        @Header("Authorization") token: String,
        @Path("callSid") callSid: String
    ): CallStatusResponse
}
