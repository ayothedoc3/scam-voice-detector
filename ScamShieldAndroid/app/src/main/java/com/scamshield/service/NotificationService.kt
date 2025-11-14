package com.scamshield.service

import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage
import timber.log.Timber

class NotificationService : FirebaseMessagingService() {

    override fun onMessageReceived(remoteMessage: RemoteMessage) {
        super.onMessageReceived(remoteMessage)
        Timber.d("FCM message received: ${remoteMessage.data}")

        // Handle notification payload
        remoteMessage.notification?.let {
            Timber.d("Message Notification Body: ${it.body}")
            // TODO: Show notification
        }

        // Handle data payload
        remoteMessage.data.isNotEmpty().let {
            Timber.d("Message data payload: ${remoteMessage.data}")
            // TODO: Handle data
        }
    }

    override fun onNewToken(token: String) {
        super.onNewToken(token)
        Timber.d("FCM token refreshed: $token")
        // TODO: Send token to server
    }
}
