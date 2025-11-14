package com.scamshield.presentation.protection

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.scamshield.presentation.components.LiveTranscript
import com.scamshield.presentation.components.RiskMeter
import com.scamshield.presentation.components.TranscriptEntry

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProtectionScreen(
    viewModel: ProtectionViewModel = hiltViewModel()
) {
    val state by viewModel.state.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Call Protection") }
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            when {
                !state.isActive -> {
                    StartProtectionCard(
                        onStartClick = viewModel::startProtection,
                        isLoading = state.isLoading
                    )
                }
                state.isWaitingForMerge -> {
                    CallMergingInstructions(
                        bridgeNumber = state.bridgeNumber ?: "",
                        onMergedClick = viewModel::onCallsMerged
                    )
                }
                else -> {
                    ActiveProtectionView(
                        riskScore = state.currentRiskScore,
                        riskLevel = state.currentRiskLevel,
                        transcript = state.transcript,
                        onStopClick = viewModel::stopProtection
                    )
                }
            }
        }
    }

    // Show alert dialog when high risk detected
    if (state.showHighRiskAlert) {
        AlertDialog(
            onDismissRequest = { viewModel.dismissAlert() },
            title = { Text("⚠️ SCAM DETECTED") },
            text = {
                Text(
                    "AI-generated voice detected with ${state.currentRiskScore.toInt()}% confidence.\n\n" +
                            "Consider hanging up immediately."
                )
            },
            confirmButton = {
                Button(
                    onClick = viewModel::stopProtection,
                    colors = ButtonDefaults.buttonColors(
                        containerColor = MaterialTheme.colorScheme.error
                    )
                ) {
                    Text("Hang Up")
                }
            },
            dismissButton = {
                TextButton(onClick = { viewModel.dismissAlert() }) {
                    Text("Continue Monitoring")
                }
            }
        )
    }
}

@Composable
fun StartProtectionCard(
    onStartClick: () -> Unit,
    isLoading: Boolean
) {
    Card(
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier
                .padding(24.dp)
                .fillMaxWidth(),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Text(
                text = "Start Call Protection",
                style = MaterialTheme.typography.headlineSmall
            )

            Text(
                text = "Click below to activate call protection",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )

            Button(
                onClick = onStartClick,
                enabled = !isLoading,
                modifier = Modifier.fillMaxWidth()
            ) {
                if (isLoading) {
                    CircularProgressIndicator(
                        modifier = Modifier.size(24.dp),
                        color = MaterialTheme.colorScheme.onPrimary
                    )
                } else {
                    Text("Start Protection")
                }
            }
        }
    }
}

@Composable
fun CallMergingInstructions(
    bridgeNumber: String,
    onMergedClick: () -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier
                .padding(24.dp)
                .fillMaxWidth(),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Text(
                text = "Merge Calls",
                style = MaterialTheme.typography.headlineSmall
            )

            Text(
                text = "Protection Number:",
                style = MaterialTheme.typography.labelLarge
            )

            Text(
                text = bridgeNumber,
                style = MaterialTheme.typography.headlineMedium,
                color = MaterialTheme.colorScheme.primary
            )

            Divider()

            Text(
                text = "Instructions:",
                style = MaterialTheme.typography.labelLarge
            )

            InstructionStep(1, "Answer our protection call")
            InstructionStep(2, "Tap 'Add Call' on your phone")
            InstructionStep(3, "Call the suspicious number")
            InstructionStep(4, "Tap 'Merge Calls'")
            InstructionStep(5, "We'll analyze in real-time")

            Button(
                onClick = onMergedClick,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("I've Merged the Calls")
            }
        }
    }
}

@Composable
fun InstructionStep(number: Int, text: String) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Surface(
            shape = MaterialTheme.shapes.small,
            color = MaterialTheme.colorScheme.primaryContainer
        ) {
            Text(
                text = number.toString(),
                modifier = Modifier.padding(horizontal = 12.dp, vertical = 4.dp),
                style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.onPrimaryContainer
            )
        }
        Text(
            text = text,
            style = MaterialTheme.typography.bodyMedium
        )
    }
}

@Composable
fun ActiveProtectionView(
    riskScore: Float,
    riskLevel: String,
    transcript: List<TranscriptEntry>,
    onStopClick: () -> Unit
) {
    Column(
        modifier = Modifier.fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Card {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp)
            ) {
                Text(
                    text = "🔴 Protection Active",
                    style = MaterialTheme.typography.titleLarge,
                    color = MaterialTheme.colorScheme.error
                )
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = "Monitoring call for AI voice patterns",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }

        RiskMeter(
            score = riskScore,
            level = riskLevel
        )

        LiveTranscript(
            transcript = transcript,
            modifier = Modifier.weight(1f)
        )

        Button(
            onClick = onStopClick,
            modifier = Modifier.fillMaxWidth(),
            colors = ButtonDefaults.buttonColors(
                containerColor = MaterialTheme.colorScheme.error
            )
        ) {
            Text("Stop Protection")
        }
    }
}
