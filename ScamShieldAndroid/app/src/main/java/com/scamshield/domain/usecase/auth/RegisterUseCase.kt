package com.scamshield.domain.usecase.auth

import com.scamshield.domain.model.User
import com.scamshield.domain.repository.IAuthRepository
import javax.inject.Inject

class RegisterUseCase @Inject constructor(
    private val authRepository: IAuthRepository
) {
    suspend operator fun invoke(email: String, password: String, phoneNumber: String?): User {
        val result = authRepository.register(email, password, phoneNumber)
        return result.getOrThrow()
    }
}
