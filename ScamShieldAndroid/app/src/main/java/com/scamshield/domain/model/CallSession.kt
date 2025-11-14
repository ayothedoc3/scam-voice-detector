package com.scamshield.domain.model

import java.time.LocalDateTime

data class CallSession(
    val id: Long = 0,
    val callSid: String,
    val streamSid: String? = null,
    val status: CallStatus,
    val startedAt: LocalDateTime,
    val endedAt: LocalDateTime? = null,
    val totalDuration: Float = 0f,
    val maxRiskScore: Float = 0f,
    val finalVerdict: RiskLevel? = null,
    val phoneNumber: String? = null
)

enum class CallStatus {
    INITIALIZING,
    ACTIVE,
    COMPLETED,
    FAILED
}
