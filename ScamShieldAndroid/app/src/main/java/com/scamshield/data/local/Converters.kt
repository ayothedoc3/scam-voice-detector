package com.scamshield.data.local

import androidx.room.TypeConverter
import com.scamshield.domain.model.CallStatus
import com.scamshield.domain.model.RiskLevel
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

class Converters {
    private val formatter = DateTimeFormatter.ISO_LOCAL_DATE_TIME

    @TypeConverter
    fun fromLocalDateTime(value: LocalDateTime?): String? {
        return value?.format(formatter)
    }

    @TypeConverter
    fun toLocalDateTime(value: String?): LocalDateTime? {
        return value?.let { LocalDateTime.parse(it, formatter) }
    }

    @TypeConverter
    fun fromCallStatus(value: CallStatus): String {
        return value.name
    }

    @TypeConverter
    fun toCallStatus(value: String): CallStatus {
        return CallStatus.valueOf(value)
    }

    @TypeConverter
    fun fromRiskLevel(value: RiskLevel?): String? {
        return value?.name
    }

    @TypeConverter
    fun toRiskLevel(value: String?): RiskLevel? {
        return value?.let { RiskLevel.valueOf(it) }
    }
}
