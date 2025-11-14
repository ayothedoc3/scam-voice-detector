package com.scamshield.domain.model

import java.time.LocalDateTime

data class AnalysisResult(
    val id: Long = 0,
    val callSessionId: Long,
    val chunkIndex: Int,
    val timestamp: LocalDateTime,
    val riskScore: Float,
    val riskLevel: RiskLevel,
    val isDeepfake: Boolean,
    val confidence: Float,
    val transcript: String? = null,
    val voiceCharacteristics: VoiceCharacteristics? = null
)

data class VoiceCharacteristics(
    val pitchMean: Float,
    val pitchStd: Float,
    val spectralCentroid: Float,
    val syntheticScore: Float
)
