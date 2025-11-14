package com.scamshield.util

object Constants {
    // Notification IDs
    const val NOTIFICATION_ID_PROTECTION = 1001
    const val NOTIFICATION_ID_ALERT = 1002

    // Intent Actions
    const val ACTION_START_PROTECTION = "com.scamshield.ACTION_START_PROTECTION"
    const val ACTION_STOP_PROTECTION = "com.scamshield.ACTION_STOP_PROTECTION"

    // Broadcast Actions
    const val BROADCAST_CALL_STATE_CHANGED = "com.scamshield.CALL_STATE_CHANGED"

    // Shared Preferences Keys
    const val PREF_AUTH_TOKEN = "auth_token"
    const val PREF_USER_EMAIL = "user_email"

    // API Endpoints
    const val API_VERSION = "v1"

    // WebSocket Events
    const val WS_EVENT_JOIN_CALL = "join_call"
    const val WS_EVENT_ANALYSIS_UPDATE = "analysis_update"
    const val WS_EVENT_REAL_TIME_ANALYSIS = "real_time_analysis"

    // Risk Thresholds
    const val RISK_THRESHOLD_HIGH = 70f
    const val RISK_THRESHOLD_MEDIUM = 50f
    const val RISK_THRESHOLD_LOW = 30f
}
