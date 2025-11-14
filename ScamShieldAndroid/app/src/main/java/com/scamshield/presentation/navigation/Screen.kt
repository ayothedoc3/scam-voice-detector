package com.scamshield.presentation.navigation

sealed class Screen(val route: String) {
    object Protection : Screen("protection")
    object Login : Screen("login")
    object Register : Screen("register")
    object Home : Screen("home")
    object History : Screen("history")
    object Settings : Screen("settings")
}
