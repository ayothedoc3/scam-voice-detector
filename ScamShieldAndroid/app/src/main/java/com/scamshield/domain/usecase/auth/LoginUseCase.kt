package com.scamshield.domain.usecase.auth

import com.scamshield.domain.model.User
import com.scamshield.domain.repository.IAuthRepository
import javax.inject.Inject

class LoginUseCase @Inject constructor(
    private val authRepository: IAuthRepository
) {
    suspend operator fun invoke(email: String, password: String): User {
        val result = authRepository.login(email, password)
        return result.getOrThrow()
    }
}
