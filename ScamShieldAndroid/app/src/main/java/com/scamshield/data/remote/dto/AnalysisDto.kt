package com.scamshield.data.remote.dto

import com.google.gson.annotations.SerializedName

data class AnalysisHistoryResponse(
    @SerializedName("results")
    val results: List<AnalysisResultDto>
)

data class AnalysisResultDto(
    @SerializedName("id")
    val id: Long,
    @SerializedName("call_session_id")
    val callSessionId: Long,
    @SerializedName("chunk_index")
    val chunkIndex: Int,
    @SerializedName("timestamp")
    val timestamp: String,
    @SerializedName("risk_score")
    val riskScore: Float,
    @SerializedName("risk_level")
    val riskLevel: String,
    @SerializedName("is_deepfake")
    val isDeepfake: Boolean,
    @SerializedName("confidence")
    val confidence: Float,
    @SerializedName("transcript")
    val transcript: String?,
    @SerializedName("voice_characteristics")
    val voiceCharacteristics: VoiceCharacteristicsDto?
)

data class VoiceCharacteristicsDto(
    @SerializedName("pitch_mean")
    val pitchMean: Float,
    @SerializedName("pitch_std")
    val pitchStd: Float,
    @SerializedName("spectral_centroid")
    val spectralCentroid: Float,
    @SerializedName("synthetic_score")
    val syntheticScore: Float
)
