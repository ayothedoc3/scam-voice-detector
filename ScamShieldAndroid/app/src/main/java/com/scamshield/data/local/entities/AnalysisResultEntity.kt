package com.scamshield.data.local.entities

import androidx.room.Embedded
import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.PrimaryKey
import androidx.room.TypeConverters
import com.scamshield.data.local.Converters
import com.scamshield.domain.model.AnalysisResult
import com.scamshield.domain.model.RiskLevel
import com.scamshield.domain.model.VoiceCharacteristics
import java.time.LocalDateTime

@Entity(
    tableName = "analysis_results",
    foreignKeys = [
        ForeignKey(
            entity = CallSessionEntity::class,
            parentColumns = ["id"],
            childColumns = ["callSessionId"],
            onDelete = ForeignKey.CASCADE
        )
    ]
)
@TypeConverters(Converters::class)
data class AnalysisResultEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val callSessionId: Long,
    val chunkIndex: Int,
    val timestamp: LocalDateTime,
    val riskScore: Float,
    val riskLevel: RiskLevel,
    val isDeepfake: Boolean,
    val confidence: Float,
    val transcript: String? = null,
    @Embedded
    val voiceCharacteristics: VoiceCharacteristics? = null
) {
    fun toDomain(): AnalysisResult {
        return AnalysisResult(
            id = id,
            callSessionId = callSessionId,
            chunkIndex = chunkIndex,
            timestamp = timestamp,
            riskScore = riskScore,
            riskLevel = riskLevel,
            isDeepfake = isDeepfake,
            confidence = confidence,
            transcript = transcript,
            voiceCharacteristics = voiceCharacteristics
        )
    }

    companion object {
        fun fromDomain(analysisResult: AnalysisResult): AnalysisResultEntity {
            return AnalysisResultEntity(
                id = analysisResult.id,
                callSessionId = analysisResult.callSessionId,
                chunkIndex = analysisResult.chunkIndex,
                timestamp = analysisResult.timestamp,
                riskScore = analysisResult.riskScore,
                riskLevel = analysisResult.riskLevel,
                isDeepfake = analysisResult.isDeepfake,
                confidence = analysisResult.confidence,
                transcript = analysisResult.transcript,
                voiceCharacteristics = analysisResult.voiceCharacteristics
            )
        }
    }
}
