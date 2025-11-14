package com.scamshield.util

import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import androidx.core.app.NotificationCompat
import com.scamshield.MainActivity
import com.scamshield.R
import com.scamshield.ScamShieldApplication

object NotificationHelper {

    fun createProtectionNotification(
        context: Context,
        riskScore: Float,
        riskLevel: String
    ): android.app.Notification {
        val intent = Intent(context, MainActivity::class.java)
        val pendingIntent = PendingIntent.getActivity(
            context,
            0,
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        return NotificationCompat.Builder(context, ScamShieldApplication.CHANNEL_PROTECTION)
            .setContentTitle("Call Protection Active")
            .setContentText("Risk Level: $riskLevel (${riskScore.toInt()}%)")
            .setSmallIcon(R.drawable.ic_launcher_foreground)
            .setContentIntent(pendingIntent)
            .setOngoing(true)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .build()
    }

    fun createScamAlertNotification(
        context: Context,
        riskScore: Float
    ): android.app.Notification {
        val intent = Intent(context, MainActivity::class.java)
        val pendingIntent = PendingIntent.getActivity(
            context,
            0,
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        return NotificationCompat.Builder(context, ScamShieldApplication.CHANNEL_ALERTS)
            .setContentTitle("⚠️ SCAM DETECTED")
            .setContentText("AI-generated voice detected with ${riskScore.toInt()}% confidence!")
            .setSmallIcon(R.drawable.ic_launcher_foreground)
            .setContentIntent(pendingIntent)
            .setPriority(NotificationCompat.PRIORITY_MAX)
            .setCategory(NotificationCompat.CATEGORY_ALARM)
            .setAutoCancel(true)
            .build()
    }

    fun showNotification(context: Context, id: Int, notification: android.app.Notification) {
        val notificationManager = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        notificationManager.notify(id, notification)
    }

    fun cancelNotification(context: Context, id: Int) {
        val notificationManager = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        notificationManager.cancel(id)
    }
}
