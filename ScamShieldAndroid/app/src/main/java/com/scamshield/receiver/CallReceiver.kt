package com.scamshield.receiver

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.telephony.TelephonyManager
import timber.log.Timber

class CallReceiver : BroadcastReceiver() {

    override fun onReceive(context: Context?, intent: Intent?) {
        if (context == null || intent == null) return

        when (intent.action) {
            TelephonyManager.ACTION_PHONE_STATE_CHANGED -> {
                val state = intent.getStringExtra(TelephonyManager.EXTRA_STATE)
                val phoneNumber = intent.getStringExtra(TelephonyManager.EXTRA_INCOMING_NUMBER)

                Timber.d("Phone state changed: $state, number: $phoneNumber")

                when (state) {
                    TelephonyManager.EXTRA_STATE_RINGING -> {
                        // Incoming call
                        Timber.d("Incoming call from: $phoneNumber")
                        // TODO: Handle incoming call
                    }
                    TelephonyManager.EXTRA_STATE_OFFHOOK -> {
                        // Call answered
                        Timber.d("Call answered")
                        // TODO: Handle call answered
                    }
                    TelephonyManager.EXTRA_STATE_IDLE -> {
                        // Call ended
                        Timber.d("Call ended")
                        // TODO: Handle call ended
                    }
                }
            }

            Intent.ACTION_NEW_OUTGOING_CALL -> {
                val phoneNumber = intent.getStringExtra(Intent.EXTRA_PHONE_NUMBER)
                Timber.d("Outgoing call to: $phoneNumber")
                // TODO: Handle outgoing call
            }
        }
    }
}
