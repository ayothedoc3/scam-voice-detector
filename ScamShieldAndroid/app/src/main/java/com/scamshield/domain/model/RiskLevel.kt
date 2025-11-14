package com.scamshield.domain.model

import androidx.compose.ui.graphics.Color

enum class RiskLevel {
    LOW,
    MEDIUM,
    HIGH,
    CRITICAL;

    fun getColor(): Color {
        return when (this) {
            LOW -> Color(0xFF4CAF50)
            MEDIUM -> Color(0xFFFFC107)
            HIGH -> Color(0xFFFF9800)
            CRITICAL -> Color(0xFFF44336)
        }
    }

    companion object {
        fun fromString(value: String): RiskLevel {
            return when (value.uppercase()) {
                "LOW" -> LOW
                "MEDIUM" -> MEDIUM
                "HIGH" -> HIGH
                "CRITICAL" -> CRITICAL
                else -> LOW
            }
        }
    }
}
