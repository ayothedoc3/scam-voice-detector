package com.scamshield.data.local

import androidx.room.Database
import androidx.room.RoomDatabase
import androidx.room.TypeConverters
import com.scamshield.data.local.dao.AnalysisResultDao
import com.scamshield.data.local.dao.CallSessionDao
import com.scamshield.data.local.entities.AnalysisResultEntity
import com.scamshield.data.local.entities.CallSessionEntity

@Database(
    entities = [
        CallSessionEntity::class,
        AnalysisResultEntity::class
    ],
    version = 1,
    exportSchema = false
)
@TypeConverters(Converters::class)
abstract class ScamShieldDatabase : RoomDatabase() {
    abstract fun callSessionDao(): CallSessionDao
    abstract fun analysisResultDao(): AnalysisResultDao

    companion object {
        const val DATABASE_NAME = "scam_shield_db"
    }
}
