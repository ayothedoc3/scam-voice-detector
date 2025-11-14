package com.scamshield.data.local.entities

import androidx.room.Entity
import androidx.room.PrimaryKey
import androidx.room.TypeConverters
import com.scamshield.data.local.Converters
import com.scamshield.domain.model.CallSession
import com.scamshield.domain.model.CallStatus
import com.scamshield.domain.model.RiskLevel
import java.time.LocalDateTime

@Entity(tableName = "call_sessions")
@TypeConverters(Converters::class)
data class CallSessionEntity(
    @PrimaryKey(autoGenerate = true)
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
) {
    fun toDomain(): CallSession {
        return CallSession(
            id = id,
            callSid = callSid,
            streamSid = streamSid,
            status = status,
            startedAt = startedAt,
            endedAt = endedAt,
            totalDuration = totalDuration,
            maxRiskScore = maxRiskScore,
            finalVerdict = finalVerdict,
            phoneNumber = phoneNumber
        )
    }

    companion object {
        fun fromDomain(callSession: CallSession): CallSessionEntity {
            return CallSessionEntity(
                id = callSession.id,
                callSid = callSession.callSid,
                streamSid = callSession.streamSid,
                status = callSession.status,
                startedAt = callSession.startedAt,
                endedAt = callSession.endedAt,
                totalDuration = callSession.totalDuration,
                maxRiskScore = callSession.maxRiskScore,
                finalVerdict = callSession.finalVerdict,
                phoneNumber = callSession.phoneNumber
            )
        }
    }
}
