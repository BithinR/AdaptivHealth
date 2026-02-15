/*
Text styles used across the app.

Design System Reference:
- Primary Font: Inter (body text, labels)
- Monospace Font: JetBrains Mono (numeric values like HR, SpO2, BP)

We keep all fonts and sizes here so screens look consistent.
*/

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AdaptivTypography {
  // Private constructor
  AdaptivTypography._();

  // Base text style using Inter (modern, clean, medical-grade)
  static TextStyle _baseStyle(
    double fontSize,
    FontWeight fontWeight,
    Color color,
    double lineHeight,
  ) {
    return GoogleFonts.inter(
      fontSize: fontSize,
      fontWeight: fontWeight,
      color: color,
      height: lineHeight,
      letterSpacing: fontSize < 14 ? 0.3 : 0,
    );
  }

  // Monospace style for numeric values using JetBrains Mono
  static TextStyle _monoStyle(
    double fontSize,
    FontWeight fontWeight,
    Color color,
    double lineHeight,
  ) {
    return GoogleFonts.jetBrainsMono(
      fontSize: fontSize,
      fontWeight: fontWeight,
      color: color,
      height: lineHeight,
    );
  }

  // Screen-level title (H1)
  static final TextStyle screenTitle = _baseStyle(
    28,
    FontWeight.w600,
    const Color(0xFF212121),
    1.3,
  );

  // Section headers within a screen (H2)
  static final TextStyle sectionTitle = _baseStyle(
    20,
    FontWeight.w600,
    const Color(0xFF424242),
    1.4,
  );

  // Card headers (H3)
  static final TextStyle cardTitle = _baseStyle(
    16,
    FontWeight.w600,
    const Color(0xFF212121),
    1.4,
  );

  // Regular body text (Body Large)
  static final TextStyle body = _baseStyle(
    16,
    FontWeight.w400,
    const Color(0xFF424242),
    1.5,
  );

  // Smaller body text (Body Small)
  static final TextStyle bodySmall = _baseStyle(
    14,
    FontWeight.w400,
    const Color(0xFF666666),
    1.5,
  );

  // Small metadata (Caption)
  static final TextStyle caption = _baseStyle(
    12,
    FontWeight.w400,
    const Color(0xFF999999),
    1.4,
  );

  // The big heart rate number (Value Display - Monospace)
  static final TextStyle heroNumber = _monoStyle(
    32,
    FontWeight.w700,
    const Color(0xFF212121),
    1.0,
  );

  // Compact metric value (for vital cards)
  static final TextStyle metricValue = _monoStyle(
    28,
    FontWeight.w700,
    const Color(0xFF212121),
    1.0,
  );

  // Small metric value (for secondary displays)
  static final TextStyle metricValueSmall = _monoStyle(
    20,
    FontWeight.w600,
    const Color(0xFF212121),
    1.0,
  );

  // Unit label next to numbers (units like BPM, %)
  static final TextStyle heroUnit = _baseStyle(
    12,
    FontWeight.w400,
    const Color(0xFF666666),
    1.0,
  );

  // Button text
  static final TextStyle button = _baseStyle(
    14,
    FontWeight.w600,
    const Color(0xFFFFFFFF),
    1.4,
  );

  // Overline / badge text
  static final TextStyle overline = _baseStyle(
    11,
    FontWeight.w500,
    const Color(0xFF666666),
    1.4,
  );

  // Label text (for form labels, card labels)
  static final TextStyle label = _baseStyle(
    12,
    FontWeight.w500,
    const Color(0xFF666666),
    1.4,
  );

  // Subtitle 1 (for section headers)
  static final TextStyle subtitle1 = _baseStyle(
    18,
    FontWeight.w600,
    const Color(0xFF212121),
    1.4,
  );

  // Subtitle 2 (smaller subtitle)
  static final TextStyle subtitle2 = _baseStyle(
    16,
    FontWeight.w500,
    const Color(0xFF424242),
    1.4,
  );
}
