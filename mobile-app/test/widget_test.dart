// Basic Flutter widget test for AdaptivHealth.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:adaptiv_health/main.dart';

void main() {
  testWidgets('App renders login screen by default', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const AdaptivHealthApp());

    // Verify that the app title is displayed.
    expect(find.text('Adaptiv Health'), findsOneWidget);

    // Verify that the sign in button is displayed.
    expect(find.text('Sign In'), findsOneWidget);
  });
}
