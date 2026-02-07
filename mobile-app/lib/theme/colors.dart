/*
App color palette.

These colors are used everywhere so the app looks consistent.
Red means high risk, amber means caution, green means safe.
*/

import 'package:flutter/material.dart';

class AdaptivColors {
  // Private constructor
  AdaptivColors._();

  // Primary brand colors
  static const Color primary = Color(0xFF2563EB);      // Trust, professional
  static const Color primaryDark = Color(0xFF1E40AF);  // Hover states
  static const Color primaryLight = Color(0xFFDBEAFE); // Light backgrounds
  static const Color primaryUltralight = Color(0xFFEFF6FF); // Very light

  // Clinical status: Critical (High Risk)
  static const Color critical = Color(0xFFEF4444);
  static const Color criticalBg = Color(0xFFFEF2F2);
  static const Color criticalBorder = Color(0xFFFCA5A5);
  static const Color criticalText = Color(0xFF991B1B);
  static const Color criticalUltralight = Color(0xFFFEF2F2);
  static const Color criticalLight = Color(0xFFFCA5A5);

  // Clinical status: Warning (Moderate Risk)
  static const Color warning = Color(0xFFF59E0B);
  static const Color warningBg = Color(0xFFFFFBEB);
  static const Color warningBorder = Color(0xFFFCD34D);
  static const Color warningText = Color(0xFF92400E);

  // Clinical status: Stable (Low Risk)
  static const Color stable = Color(0xFF22C55E);
  static const Color stableBg = Color(0xFFF0FDF4);
  static const Color stableBorder = Color(0xFF86EFAC);
  static const Color stableText = Color(0xFF166534);

  // Neutral palette
  static const Color text900 = Color(0xFF111827);    // Primary text
  static const Color text700 = Color(0xFF374151);    // Secondary text
  static const Color text600 = Color(0xFF4B5563);    // Tertiary text alt
  static const Color text500 = Color(0xFF6B7280);    // Tertiary text
  static const Color text50 = Color(0xFFFAFAFA);     // Very light text
  static const Color neutral300 = Color(0xFFD1D5DB); // Neutral shade
  static const Color neutral400 = Color(0xFF9CA3AF); // Neutral shade
  static const Color border300 = Color(0xFFD1D5DB);  // Borders, dividers
  static const Color surface100 = Color(0xFFF3F4F6); // Card backgrounds
  static const Color background50 = Color(0xFFF9FAFB); // Page background
  static const Color white = Color(0xFFFFFFFF);      // White surfaces

  // Chart colors
  static const Color chartTeal = Color(0xFF14B8A6);
  static const Color chartBlue = Color(0xFF0EA5E9);
  static const Color chartSuccess = Color(0xFF10B981);

  // Helper methods for risk levels
  static Color getRiskColor(String riskLevel) {
    switch (riskLevel.toLowerCase()) {
      case 'high':
        return critical;
      case 'moderate':
        return warning;
      case 'low':
      default:
        return stable;
    }
  }

  static Color getRiskBgColor(String riskLevel) {
    switch (riskLevel.toLowerCase()) {
      case 'high':
        return criticalBg;
      case 'moderate':
        return warningBg;
      case 'low':
      default:
        return stableBg;
    }
  }

  static Color getRiskTextColor(String riskLevel) {
    switch (riskLevel.toLowerCase()) {
      case 'high':
        return criticalText;
      case 'moderate':
        return warningText;
      case 'low':
      default:
        return stableText;
    }
  }
}
