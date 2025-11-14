package com.scamshield.domain.repository

import com.scamshield.domain.model.AnalysisResult
import com.scamshield.domain.model.CallSession
import kotlinx.coroutines.flow.Flow

interface IAnalysisRepository {
    suspend fun getCallSessions(): Flow<List<CallSession>>
    suspend fun getCallSessionById(id: Long): CallSession?
    suspend fun getAnalysisResultsForCall(callSessionId: Long): Flow<List<AnalysisResult>>
    suspend fun saveCallSession(callSession: CallSession): Long
    suspend fun saveAnalysisResult(analysisResult: AnalysisResult)
}
