package com.scamshield.di

import com.scamshield.data.repository.AnalysisRepository
import com.scamshield.data.repository.AuthRepository
import com.scamshield.data.repository.ProtectionRepository
import com.scamshield.domain.repository.IAnalysisRepository
import com.scamshield.domain.repository.IAuthRepository
import com.scamshield.domain.repository.IProtectionRepository
import dagger.Binds
import dagger.Module
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {

    @Binds
    @Singleton
    abstract fun bindAuthRepository(
        authRepository: AuthRepository
    ): IAuthRepository

    @Binds
    @Singleton
    abstract fun bindProtectionRepository(
        protectionRepository: ProtectionRepository
    ): IProtectionRepository

    @Binds
    @Singleton
    abstract fun bindAnalysisRepository(
        analysisRepository: AnalysisRepository
    ): IAnalysisRepository
}
