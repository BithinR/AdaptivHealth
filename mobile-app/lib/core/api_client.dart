import 'package:dio/dio.dart';
import 'token_storage.dart';

class ApiClient {
  final Dio dio;
  final TokenStorage tokenStorage;

  ApiClient({
    required this.tokenStorage,
    required String baseUrl,
  }) : dio = Dio(BaseOptions(
          baseUrl: baseUrl,
          connectTimeout: const Duration(seconds: 10),
          receiveTimeout: const Duration(seconds: 15),
        )) {
    dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) async {
          final token = await tokenStorage.getToken();
          if (token != null && token.isNotEmpty) {
            options.headers['Authorization'] = 'Bearer $token';
          }
          options.headers['Content-Type'] = 'application/json';
          return handler.next(options);
        },
      ),
    );
  }
}
