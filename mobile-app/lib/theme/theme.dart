/*
App-wide theme.

This sets the default colors, fonts, and styles for all screens.
*/

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'colors.dart';
import 'typography.dart';

ThemeData buildAdaptivHealthTheme() {
  return ThemeData(
    useMaterial3: true,
    brightness: Brightness.light,
    
    // Color scheme
    colorScheme: const ColorScheme.light(
      primary: AdaptivColors.primary,
      secondary: AdaptivColors.primary,
      error: AdaptivColors.critical,
      surface: AdaptivColors.white,
      onPrimary: AdaptivColors.white,
      onSurface: AdaptivColors.text900,
    ),

    // Scaffold background
    scaffoldBackgroundColor: AdaptivColors.background50,

    // App bar theme
    appBarTheme: AppBarTheme(
      backgroundColor: AdaptivColors.white,
      elevation: 1,
      surfaceTintColor: Colors.transparent,
      iconTheme: const IconThemeData(
        color: AdaptivColors.text900,
      ),
      titleTextStyle: GoogleFonts.dmSans(
        fontSize: 20,
        fontWeight: FontWeight.w700,
        color: AdaptivColors.text900,
      ),
    ),

    // Card theme
    cardTheme: CardThemeData(
      color: AdaptivColors.white,
      elevation: 1,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: const BorderSide(
          color: Color(0xFFD1D5DB),
          width: 1,
        ),
      ),
    ),

    // Button theme
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: AdaptivColors.primary,
        foregroundColor: AdaptivColors.white,
        elevation: 0,
        padding: const EdgeInsets.symmetric(
          horizontal: 24,
          vertical: 12,
        ),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
        textStyle: GoogleFonts.dmSans(
          fontSize: 14,
          fontWeight: FontWeight.w600,
        ),
      ),
    ),

    // Text button theme
    textButtonTheme: TextButtonThemeData(
      style: TextButton.styleFrom(
        foregroundColor: AdaptivColors.primary,
        textStyle: GoogleFonts.dmSans(
          fontSize: 14,
          fontWeight: FontWeight.w600,
        ),
      ),
    ),

    // Input decoration theme
    inputDecorationTheme: InputDecorationTheme(
      filled: true,
      fillColor: AdaptivColors.white,
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(8),
        borderSide: const BorderSide(
          color: Color(0xFFD1D5DB),
        ),
      ),
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(8),
        borderSide: const BorderSide(
          color: Color(0xFFD1D5DB),
        ),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(8),
        borderSide: const BorderSide(
          color: AdaptivColors.primary,
          width: 2,
        ),
      ),
      contentPadding: const EdgeInsets.symmetric(
        horizontal: 16,
        vertical: 12,
      ),
      labelStyle: GoogleFonts.dmSans(
        color: AdaptivColors.text700,
        fontSize: 14,
        fontWeight: FontWeight.w500,
      ),
      hintStyle: GoogleFonts.dmSans(
        color: AdaptivColors.text500,
        fontSize: 14,
      ),
    ),

    // Bottom navigation theme
    bottomNavigationBarTheme: const BottomNavigationBarThemeData(
      backgroundColor: AdaptivColors.white,
      elevation: 8,
      selectedItemColor: AdaptivColors.primary,
      unselectedItemColor: AdaptivColors.text500,
      type: BottomNavigationBarType.fixed,
    ),

    // Font family
    fontFamily: 'Roboto',

    // Text themes
    textTheme: TextTheme(
      displayLarge: AdaptivTypography.heroNumber,
      displayMedium: AdaptivTypography.screenTitle,
      displaySmall: AdaptivTypography.sectionTitle,
      headlineSmall: AdaptivTypography.cardTitle,
      bodyLarge: AdaptivTypography.body,
      bodyMedium: AdaptivTypography.caption,
      labelSmall: AdaptivTypography.overline,
    ),
  );
}
