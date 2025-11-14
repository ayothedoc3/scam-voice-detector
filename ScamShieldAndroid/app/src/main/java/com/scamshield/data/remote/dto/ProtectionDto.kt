package com.scamshield.data.remote.dto

import com.google.gson.annotations.SerializedName

data class StartProtectionRequest(
    @SerializedName("user_phone")
    val userPhone: String
)

data class StartProtectionResponse(
    @SerializedName("session_id")
    val sessionId: Long,
    @SerializedName("call_sid")
    val callSid: String,
    @SerializedName("bridge_number")
    val bridgeNumber: String,
    @SerializedName("instructions")
    val instructions: String
)

data class StopProtectionRequest(
    @SerializedName("call_sid")
    val callSid: String
)

data class CallStatusResponse(
    @SerializedName("call_sid")
    val callSid: String,
    @SerializedName("status")
    val status: String,
    @SerializedName("current_risk_score")
    val currentRiskScore: Float,
    @SerializedName("duration")
    val duration: Float
)
