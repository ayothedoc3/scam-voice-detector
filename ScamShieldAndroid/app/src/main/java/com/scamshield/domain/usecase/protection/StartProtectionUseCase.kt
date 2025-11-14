package com.scamshield.domain.usecase.protection

import com.scamshield.data.remote.dto.StartProtectionResponse
import com.scamshield.domain.repository.IProtectionRepository
import javax.inject.Inject

class StartProtectionUseCase @Inject constructor(
    private val protectionRepository: IProtectionRepository
) {
    suspend operator fun invoke(phoneNumber: String): StartProtectionResponse {
        val result = protectionRepository.startProtection(phoneNumber)
        return result.getOrThrow()
    }
}
