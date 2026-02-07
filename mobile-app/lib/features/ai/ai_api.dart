import 'package:dio/dio.dart';

class AiApi {
  final Dio dio;
  AiApi(this.dio);

  // 1) Compute risk assessment using latest vitals in DB + store it + create recommendation
  Future<Map<String, dynamic>> computeMyRiskAssessment() async {
    final res = await dio.post('/risk-assessments/compute');
    return Map<String, dynamic>.from(res.data);
  }

  // 2) Latest risk assessment
  Future<Map<String, dynamic>> getMyLatestRisk() async {
    final res = await dio.get('/risk-assessments/latest');
    return Map<String, dynamic>.from(res.data);
  }

  // 3) Latest recommendation
  Future<Map<String, dynamic>> getMyLatestRecommendation() async {
    final res = await dio.get('/recommendations/latest');
    return Map<String, dynamic>.from(res.data);
  }

  // Optional: latest vitals for the home screen (depends on your existing endpoint)
  Future<Map<String, dynamic>> getLatestVitals() async {
    final res = await dio.get('/vitals/latest');
    return Map<String, dynamic>.from(res.data);
  }
}
