package com.scamshield.presentation.protection

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.scamshield.data.local.PreferencesManager
import com.scamshield.data.remote.websocket.AnalysisWebSocket
import com.scamshield.domain.usecase.protection.StartProtectionUseCase
import com.scamshield.domain.usecase.protection.StopProtectionUseCase
import com.scamshield.presentation.components.TranscriptEntry
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import timber.log.Timber
import javax.inject.Inject

@HiltViewModel
class ProtectionViewModel @Inject constructor(
    private val startProtectionUseCase: StartProtectionUseCase,
    private val stopProtectionUseCase: StopProtectionUseCase,
    private val analysisWebSocket: AnalysisWebSocket,
    private val preferencesManager: PreferencesManager
) : ViewModel() {

    private val _state = MutableStateFlow(ProtectionState())
    val state: StateFlow<ProtectionState> = _state.asStateFlow()

    fun startProtection() {
        viewModelScope.launch {
            _state.update { it.copy(isLoading = true) }

            try {
                val result = startProtectionUseCase()

                _state.update {
                    it.copy(
                        isLoading = false,
                        isActive = true,
                        isWaitingForMerge = true,
                        callSid = result.callSid,
                        bridgeNumber = result.bridgeNumber
                    )
                }
            } catch (e: Exception) {
                Timber.e(e, "Failed to start protection")
                _state.update {
                    it.copy(
                        isLoading = false,
                        error = e.message
                    )
                }
            }
        }
    }

    fun onCallsMerged() {
        _state.update { it.copy(isWaitingForMerge = false) }

        // Start listening to analysis updates
        state.value.callSid?.let { callSid ->
            listenToAnalysisUpdates(callSid)
        }
    }

    private fun listenToAnalysisUpdates(callSid: String) {
        viewModelScope.launch {
            try {
                val token = preferencesManager.getAuthToken() ?: ""

                analysisWebSocket.connectToAnalysisStream(callSid, token)
                    .catch { e ->
                        Timber.e(e, "WebSocket error")
                    }
                    .collect { update ->
                        _state.update { state ->
                            val newTranscript = state.transcript + TranscriptEntry(
                                timestamp = update.timestamp,
                                text = update.transcript?.text ?: ""
                            )

                            state.copy(
                                currentRiskScore = update.riskScore,
                                currentRiskLevel = update.riskLevel,
                                transcript = newTranscript,
                                showHighRiskAlert = update.riskScore >= 70f && !state.showHighRiskAlert
                            )
                        }
                    }
            } catch (e: Exception) {
                Timber.e(e, "Failed to connect to WebSocket")
            }
        }
    }

    fun stopProtection() {
        viewModelScope.launch {
            state.value.callSid?.let { callSid ->
                try {
                    stopProtectionUseCase(callSid)
                    analysisWebSocket.disconnect()

                    _state.update {
                        ProtectionState() // Reset to initial state
                    }
                } catch (e: Exception) {
                    Timber.e(e, "Failed to stop protection")
                }
            }
        }
    }

    fun dismissAlert() {
        _state.update { it.copy(showHighRiskAlert = false) }
    }

    override fun onCleared() {
        super.onCleared()
        analysisWebSocket.disconnect()
    }
}

data class ProtectionState(
    val isLoading: Boolean = false,
    val isActive: Boolean = false,
    val isWaitingForMerge: Boolean = false,
    val callSid: String? = null,
    val bridgeNumber: String? = null,
    val currentRiskScore: Float = 0f,
    val currentRiskLevel: String = "LOW",
    val transcript: List<TranscriptEntry> = emptyList(),
    val showHighRiskAlert: Boolean = false,
    val error: String? = null
)
