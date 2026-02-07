import 'package:flutter/foundation.dart';
import 'ai_api.dart';

class AiStore extends ChangeNotifier {
  final AiApi api;
  AiStore(this.api);

  bool loading = false;
  String? error;

  Map<String, dynamic>? latestVitals;
  Map<String, dynamic>? latestRisk;
  Map<String, dynamic>? latestRecommendation;

  Future<void> loadHome() async {
    loading = true;
    error = null;
    notifyListeners();

    try {
      // In parallel-ish: call sequentially for simplicity
      latestVitals = await api.getLatestVitals();
      latestRisk = await api.getMyLatestRisk();
      latestRecommendation = await api.getMyLatestRecommendation();
    } catch (e) {
      error = _prettyError(e);
    } finally {
      loading = false;
      notifyListeners();
    }
  }

  Future<void> computeAiAndRefresh() async {
    loading = true;
    error = null;
    notifyListeners();

    try {
      await api.computeMyRiskAssessment();
      latestRisk = await api.getMyLatestRisk();
      latestRecommendation = await api.getMyLatestRecommendation();
    } catch (e) {
      error = _prettyError(e);
    } finally {
      loading = false;
      notifyListeners();
    }
  }

  String _prettyError(Object e) {
    final msg = e.toString();
    // You can improve this later; keep it readable for now
    if (msg.contains('404')) return 'No data yet. Submit vitals first.';
    if (msg.contains('401')) return 'Session expired. Please login again.';
    return 'Something went wrong. $msg';
  }
}
