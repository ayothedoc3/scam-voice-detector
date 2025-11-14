package com.scamshield.data.remote.websocket

import com.google.gson.Gson
import com.scamshield.BuildConfig
import kotlinx.coroutines.channels.awaitClose
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.callbackFlow
import okhttp3.*
import timber.log.Timber
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class AnalysisWebSocket @Inject constructor(
    private val okHttpClient: OkHttpClient,
    private val gson: Gson
) {

    private var webSocket: WebSocket? = null

    fun connectToAnalysisStream(callSid: String, token: String): Flow<AnalysisUpdate> = callbackFlow {
        val request = Request.Builder()
            .url("${BuildConfig.WS_BASE_URL}/socket.io/?EIO=4&transport=websocket")
            .addHeader("Authorization", "Bearer $token")
            .build()

        val listener = object : WebSocketListener() {
            override fun onOpen(webSocket: WebSocket, response: Response) {
                Timber.d("WebSocket connected")
                // Join call room
                val joinMessage = """42["join_call",{"call_sid":"$callSid"}]"""
                webSocket.send(joinMessage)
            }

            override fun onMessage(webSocket: WebSocket, text: String) {
                Timber.d("WebSocket message: $text")

                // Parse Socket.IO message format
                if (text.startsWith("42")) {
                    val jsonContent = text.substring(2)
                    try {
                        // Parse the array format: ["event_name", {data}]
                        val arrayPattern = """\["([^"]+)",(.+)\]""".toRegex()
                        val matchResult = arrayPattern.find(jsonContent)

                        if (matchResult != null) {
                            val eventName = matchResult.groupValues[1]
                            val dataJson = matchResult.groupValues[2]

                            when (eventName) {
                                "analysis_update", "real_time_analysis" -> {
                                    val update = gson.fromJson(dataJson, AnalysisUpdate::class.java)
                                    trySend(update)
                                }
                            }
                        }
                    } catch (e: Exception) {
                        Timber.e(e, "Failed to parse message")
                    }
                }
            }

            override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
                Timber.e(t, "WebSocket error")
                close(t)
            }

            override fun onClosing(webSocket: WebSocket, code: Int, reason: String) {
                Timber.d("WebSocket closing: $reason")
                webSocket.close(1000, null)
                close()
            }
        }

        webSocket = okHttpClient.newWebSocket(request, listener)

        awaitClose {
            webSocket?.close(1000, "Client closed")
            webSocket = null
        }
    }

    fun disconnect() {
        webSocket?.close(1000, "User disconnected")
        webSocket = null
    }
}

data class AnalysisUpdate(
    val timestamp: String,
    val chunkIndex: Int,
    val riskScore: Float,
    val riskLevel: String,
    val deepfake: DeepfakeData?,
    val transcript: TranscriptData?,
    val voice: VoiceData?
)

data class DeepfakeData(
    val isDeepfake: Boolean,
    val confidence: Float
)

data class TranscriptData(
    val text: String,
    val confidence: Float
)

data class VoiceData(
    val syntheticScore: Float,
    val pitchMean: Float,
    val pitchStd: Float
)
