package com.scamshield.data.local.dao

import androidx.room.*
import com.scamshield.data.local.entities.AnalysisResultEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface AnalysisResultDao {

    @Query("SELECT * FROM analysis_results WHERE callSessionId = :callSessionId ORDER BY timestamp ASC")
    fun getAnalysisResultsForCall(callSessionId: Long): Flow<List<AnalysisResultEntity>>

    @Query("SELECT * FROM analysis_results WHERE id = :id")
    suspend fun getAnalysisResultById(id: Long): AnalysisResultEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAnalysisResult(analysisResult: AnalysisResultEntity): Long

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAnalysisResults(analysisResults: List<AnalysisResultEntity>)

    @Delete
    suspend fun deleteAnalysisResult(analysisResult: AnalysisResultEntity)

    @Query("DELETE FROM analysis_results WHERE callSessionId = :callSessionId")
    suspend fun deleteAnalysisResultsForCall(callSessionId: Long)

    @Query("DELETE FROM analysis_results")
    suspend fun deleteAllAnalysisResults()
}
