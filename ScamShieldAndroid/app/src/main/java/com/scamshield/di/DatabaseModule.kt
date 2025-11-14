package com.scamshield.di

import android.content.Context
import androidx.room.Room
import com.scamshield.data.local.ScamShieldDatabase
import com.scamshield.data.local.dao.AnalysisResultDao
import com.scamshield.data.local.dao.CallSessionDao
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {

    @Provides
    @Singleton
    fun provideScamShieldDatabase(
        @ApplicationContext context: Context
    ): ScamShieldDatabase {
        return Room.databaseBuilder(
            context,
            ScamShieldDatabase::class.java,
            ScamShieldDatabase.DATABASE_NAME
        )
            .fallbackToDestructiveMigration()
            .build()
    }

    @Provides
    @Singleton
    fun provideCallSessionDao(database: ScamShieldDatabase): CallSessionDao {
        return database.callSessionDao()
    }

    @Provides
    @Singleton
    fun provideAnalysisResultDao(database: ScamShieldDatabase): AnalysisResultDao {
        return database.analysisResultDao()
    }
}
