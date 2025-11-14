package com.scamshield.presentation.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import com.scamshield.presentation.protection.ProtectionScreen

@Composable
fun NavGraph(
    navController: NavHostController,
    startDestination: String = Screen.Protection.route
) {
    NavHost(
        navController = navController,
        startDestination = startDestination
    ) {
        composable(Screen.Protection.route) {
            ProtectionScreen()
        }

        // Add other screens as needed
        // composable(Screen.Login.route) { LoginScreen() }
        // composable(Screen.Register.route) { RegisterScreen() }
        // composable(Screen.Home.route) { HomeScreen() }
        // composable(Screen.History.route) { HistoryScreen() }
        // composable(Screen.Settings.route) { SettingsScreen() }
    }
}
