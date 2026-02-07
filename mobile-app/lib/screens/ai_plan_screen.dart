import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../features/ai/ai_store.dart';

class AiPlanScreen extends StatelessWidget {
  const AiPlanScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final store = context.watch<AiStore>();
    final rec = store.latestRecommendation;

    return Scaffold(
      appBar: AppBar(title: const Text("Today's Plan")),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: rec == null
            ? Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Text("No plan yet. Compute AI first."),
                  const SizedBox(height: 12),
                  ElevatedButton(
                    onPressed: store.computeAiAndRefresh,
                    child: const Text("Compute AI Now"),
                  ),
                ],
              )
            : Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Text(rec['title']?.toString() ?? 'Recommendation',
                        style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 8),
                    Text("Activity: ${rec['suggested_activity']}"),
                    Text("Intensity: ${rec['intensity_level']}"),
                    Text("Duration: ${rec['duration_minutes']} min"),
                    const SizedBox(height: 8),
                    if (rec['target_heart_rate_max'] != null)
                      Text("Max HR: ${rec['target_heart_rate_max']}"),
                    const SizedBox(height: 8),
                    if (rec['description'] != null) Text(rec['description']),
                    const SizedBox(height: 8),
                    if (rec['warnings'] != null)
                      Text("Warning: ${rec['warnings']}", style: const TextStyle(fontWeight: FontWeight.w600)),
                  ]),
                ),
              ),
      ),
    );
  }
}
