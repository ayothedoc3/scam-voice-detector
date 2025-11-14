package com.scamshield.data.local.dao

import androidx.room.*
import com.scamshield.data.local.entities.CallSessionEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface CallSessionDao {

    @Query("SELECT * FROM call_sessions ORDER BY startedAt DESC")
    fun getAllCallSessions(): Flow<List<CallSessionEntity>>

    @Query("SELECT * FROM call_sessions WHERE id = :id")
    suspend fun getCallSessionById(id: Long): CallSessionEntity?

    @Query("SELECT * FROM call_sessions WHERE callSid = :callSid")
    suspend fun getCallSessionByCallSid(callSid: String): CallSessionEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertCallSession(callSession: CallSessionEntity): Long

    @Update
    suspend fun updateCallSession(callSession: CallSessionEntity)

    @Delete
    suspend fun deleteCallSession(callSession: CallSessionEntity)

    @Query("DELETE FROM call_sessions")
    suspend fun deleteAllCallSessions()

    @Query("SELECT * FROM call_sessions ORDER BY startedAt DESC LIMIT :limit")
    fun getRecentCallSessions(limit: Int = 20): Flow<List<CallSessionEntity>>
}
