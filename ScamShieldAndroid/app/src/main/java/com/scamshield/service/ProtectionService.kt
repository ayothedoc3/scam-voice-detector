package com.scamshield.service

import android.app.Service
import android.content.Intent
import android.os.IBinder
import androidx.core.app.ServiceCompat
import com.scamshield.util.Constants
import com.scamshield.util.NotificationHelper
import dagger.hilt.android.AndroidEntryPoint
import timber.log.Timber

@AndroidEntryPoint
class ProtectionService : Service() {

    private var isProtectionActive = false
    private var currentRiskScore = 0f
    private var currentRiskLevel = "LOW"

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        when (intent?.action) {
            Constants.ACTION_START_PROTECTION -> {
                startProtection()
            }
            Constants.ACTION_STOP_PROTECTION -> {
                stopProtection()
            }
        }
        return START_STICKY
    }

    private fun startProtection() {
        Timber.d("Starting protection service")
        isProtectionActive = true

        // Start foreground service with notification
        val notification = NotificationHelper.createProtectionNotification(
            this,
            currentRiskScore,
            currentRiskLevel
        )

        startForeground(Constants.NOTIFICATION_ID_PROTECTION, notification)
    }

    private fun stopProtection() {
        Timber.d("Stopping protection service")
        isProtectionActive = false

        // Stop foreground service
        ServiceCompat.stopForeground(this, ServiceCompat.STOP_FOREGROUND_REMOVE)
        stopSelf()
    }

    fun updateRiskLevel(score: Float, level: String) {
        currentRiskScore = score
        currentRiskLevel = level

        if (isProtectionActive) {
            val notification = NotificationHelper.createProtectionNotification(
                this,
                currentRiskScore,
                currentRiskLevel
            )
            NotificationHelper.showNotification(
                this,
                Constants.NOTIFICATION_ID_PROTECTION,
                notification
            )

            // Show alert if high risk
            if (score >= Constants.RISK_THRESHOLD_HIGH) {
                val alertNotification = NotificationHelper.createScamAlertNotification(
                    this,
                    score
                )
                NotificationHelper.showNotification(
                    this,
                    Constants.NOTIFICATION_ID_ALERT,
                    alertNotification
                )
            }
        }
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onDestroy() {
        super.onDestroy()
        Timber.d("Protection service destroyed")
    }
}
