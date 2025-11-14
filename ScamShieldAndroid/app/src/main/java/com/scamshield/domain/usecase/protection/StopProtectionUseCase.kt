package com.scamshield.domain.usecase.protection

import com.scamshield.domain.repository.IProtectionRepository
import javax.inject.Inject

class StopProtectionUseCase @Inject constructor(
    private val protectionRepository: IProtectionRepository
) {
    suspend operator fun invoke(callSid: String) {
        val result = protectionRepository.stopProtection(callSid)
        result.getOrThrow()
    }
}
