package com.scamshield.data.remote.api

import com.scamshield.data.remote.dto.AnalysisHistoryResponse
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.Path

interface AnalysisApi {

    @GET("/api/v1/analysis/history/{callSessionId}")
    suspend fun getAnalysisHistory(
        @Header("Authorization") token: String,
        @Path("callSessionId") callSessionId: Long
    ): AnalysisHistoryResponse

    @GET("/api/v1/analysis/sessions")
    suspend fun getCallSessions(
        @Header("Authorization") token: String
    ): List<Any> // Replace with proper response type
}
