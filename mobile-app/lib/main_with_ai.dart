/*
Updated main.dart with AI integration.

This version includes:
- TokenStorage for secure token management
- ApiClient with auto-attached Bearer tokens
- AiStore for AI risk assessment and recommendations
- Provider for state management
*/

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:google_fonts/google_fonts.dart';

import 'core/api_client.dart';
import 'core/token_storage.dart';
import 'features/ai/ai_api.dart';
import 'features/ai/ai_store.dart';
import 'screens/ai_home_screen.dart';
import 'screens/login_screen.dart';
import 'theme/theme.dart';

void main() {
  // Initialize core services
  final tokenStorage = TokenStorage();
  
  // IMPORTANT: Change this to your backend IP/domain
  final apiClient = ApiClient(
    tokenStorage: tokenStorage,
    baseUrl: 'http://YOUR_IP:8000/api/v1', // <-- UPDATE THIS
  );

  final aiApi = AiApi(apiClient.dio);

  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AiStore(aiApi)),
        // Add more providers here as needed
      ],
      child: AdaptivHealthApp(
        apiClient: apiClient,
        tokenStorage: tokenStorage,
      ),
    ),
  );
}

class AdaptivHealthApp extends StatefulWidget {
  final ApiClient apiClient;
  final TokenStorage tokenStorage;

  const AdaptivHealthApp({
    super.key,
    required this.apiClient,
    required this.tokenStorage,
  });

  @override
  State<AdaptivHealthApp> createState() => _AdaptivHealthAppState();
}

class _AdaptivHealthAppState extends State<AdaptivHealthApp> {
  bool? _isLoggedIn;

  @override
  void initState() {
    super.initState();
    _checkLoginStatus();
  }

  Future<void> _checkLoginStatus() async {
    final token = await widget.tokenStorage.getToken();
    setState(() {
      _isLoggedIn = token != null && token.isNotEmpty;
    });
  }

  void _handleLoginSuccess() {
    setState(() {
      _isLoggedIn = true;
    });
  }

  void _handleLogout() async {
    await widget.tokenStorage.clearToken();
    setState(() {
      _isLoggedIn = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Adaptiv Health',
      theme: buildAdaptivHealthTheme(),
      
      home: _isLoggedIn == null
          ? const SplashScreen()
          : _isLoggedIn!
              ? const AiHomeScreen()
              : LoginScreen(
                  apiClient: widget.apiClient,
                  onLoginSuccess: _handleLoginSuccess,
                ),
      debugShowCheckedModeBanner: false,
    );
  }
}

class SplashScreen extends StatelessWidget {
  const SplashScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(
        child: CircularProgressIndicator(),
      ),
    );
  }
}
