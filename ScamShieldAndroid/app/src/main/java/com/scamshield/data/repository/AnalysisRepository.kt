package com.scamshield.data.repository

import com.scamshield.data.local.dao.AnalysisResultDao
import com.scamshield.data.local.dao.CallSessionDao
import com.scamshield.data.local.entities.AnalysisResultEntity
import com.scamshield.data.local.entities.CallSessionEntity
import com.scamshield.domain.model.AnalysisResult
import com.scamshield.domain.model.CallSession
import com.scamshield.domain.repository.IAnalysisRepository
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class AnalysisRepository @Inject constructor(
    private val callSessionDao: CallSessionDao,
    private val analysisResultDao: AnalysisResultDao
) : IAnalysisRepository {

    override suspend fun getCallSessions(): Flow<List<CallSession>> {
        return callSessionDao.getAllCallSessions().map { entities ->
            entities.map { it.toDomain() }
        }
    }

    override suspend fun getCallSessionById(id: Long): CallSession? {
        return callSessionDao.getCallSessionById(id)?.toDomain()
    }

    override suspend fun getAnalysisResultsForCall(callSessionId: Long): Flow<List<AnalysisResult>> {
        return analysisResultDao.getAnalysisResultsForCall(callSessionId).map { entities ->
            entities.map { it.toDomain() }
        }
    }

    override suspend fun saveCallSession(callSession: CallSession): Long {
        return callSessionDao.insertCallSession(
            CallSessionEntity.fromDomain(callSession)
        )
    }

    override suspend fun saveAnalysisResult(analysisResult: AnalysisResult) {
        analysisResultDao.insertAnalysisResult(
            AnalysisResultEntity.fromDomain(analysisResult)
        )
    }
}
