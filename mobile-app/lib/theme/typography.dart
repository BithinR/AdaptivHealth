/*
Text styles used across the app.

We keep all fonts and sizes here so screens look consistent.
*/

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AdaptivTypography {
  // Private constructor
  AdaptivTypography._();

  // Base text styles using DM Sans
  static TextStyle _baseStyle(
    double fontSize,
    FontWeight fontWeight,
    Color color,
    double lineHeight,
  ) {
    return GoogleFonts.dmSans(
      fontSize: fontSize,
      fontWeight: fontWeight,
      color: color,
      height: lineHeight,
      letterSpacing: fontSize < 14 ? 0.3 : 0,
    );
  }

  // Screen-level title
  static final TextStyle screenTitle = _baseStyle(
    24,
    FontWeight.w700,
    const Color(0xFF111827),
    1.3,
  );

  // Section headers within a screen
  static final TextStyle sectionTitle = _baseStyle(
    18,
    FontWeight.w600,
    const Color(0xFF111827),
    1.4,
  );

  // Card headers
  static final TextStyle cardTitle = _baseStyle(
    16,
    FontWeight.w600,
    const Color(0xFF111827),
    1.4,
  );

  // Regular body text
  static final TextStyle body = _baseStyle(
    14,
    FontWeight.w400,
    const Color(0xFF374151),
    1.5,
  );

  // Small metadata
  static final TextStyle caption = _baseStyle(
    12,
    FontWeight.w400,
    const Color(0xFF6B7280),
    1.4,
  );

  // The big heart rate number (HERO display)
  static final TextStyle heroNumber = _baseStyle(
    56,
    FontWeight.w700,
    const Color(0xFF111827),
    1.0,
  );

  // Unit label next to hero number
  static final TextStyle heroUnit = _baseStyle(
    18,
    FontWeight.w400,
    const Color(0xFF6B7280),
    1.0,
  );

  // Button text
  static final TextStyle button = _baseStyle(
    14,
    FontWeight.w600,
    const Color(0xFF111827),
    1.4,
  );

  // Overline / badge text
  static final TextStyle overline = _baseStyle(
    11,
    FontWeight.w500,
    const Color(0xFF6B7280),
    1.4,
  );
}
