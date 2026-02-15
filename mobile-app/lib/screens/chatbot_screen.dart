import 'package:flutter/material.dart';
import '../theme/colors.dart';
import '../theme/typography.dart';

class ChatbotScreen extends StatelessWidget {
  const ChatbotScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AdaptivColors.bg100,
      appBar: AppBar(
        backgroundColor: AdaptivColors.white,
        elevation: 0,
        title: Text('Health Coach Chatbot', style: AdaptivTypography.screenTitle),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _buildDailyBriefing(),
          const SizedBox(height: 24),
          _buildQuickQuestions(),
          const SizedBox(height: 24),
          _buildChatHistory(),
        ],
      ),
    );
  }

  Widget _buildDailyBriefing() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Daily Briefing', style: AdaptivTypography.sectionTitle),
            const SizedBox(height: 8),
            Text('Good morning! Here are your health tips for today:', style: AdaptivTypography.body),
            const SizedBox(height: 8),
            Text('• Stay hydrated\n• Take a 10-min walk\n• Remember to log your meals', style: AdaptivTypography.caption),
          ],
        ),
      ),
    );
  }

  Widget _buildQuickQuestions() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Quick Questions', style: AdaptivTypography.sectionTitle),
            const SizedBox(height: 8),
            Wrap(
              spacing: 8,
              children: [
                ElevatedButton(
                  onPressed: () {},
                  child: const Text('How to improve sleep?'),
                ),
                ElevatedButton(
                  onPressed: () {},
                  child: const Text('Healthy snacks?'),
                ),
                ElevatedButton(
                  onPressed: () {},
                  child: const Text('Stress relief tips'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildChatHistory() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Chat History', style: AdaptivTypography.sectionTitle),
            const SizedBox(height: 8),
            _buildMessage('Coach', 'Remember to drink water regularly!', true),
            _buildMessage('You', 'Thanks! Any tips for better sleep?', false),
            _buildMessage('Coach', 'Try to avoid screens 1 hour before bed.', true),
          ],
        ),
      ),
    );
  }

  Widget _buildMessage(String sender, String text, bool isCoach) {
    return Container(
      margin: const EdgeInsets.symmetric(vertical: 4),
      alignment: isCoach ? Alignment.centerLeft : Alignment.centerRight,
      child: Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: isCoach ? AdaptivColors.primaryUltralight : AdaptivColors.primary,
          borderRadius: BorderRadius.circular(12),
        ),
        child: Column(
          crossAxisAlignment:
              isCoach ? CrossAxisAlignment.start : CrossAxisAlignment.end,
          children: [
            Text(sender, style: AdaptivTypography.caption.copyWith(color: isCoach ? AdaptivColors.primary : Colors.white)),
            const SizedBox(height: 2),
            Text(text, style: AdaptivTypography.body.copyWith(color: isCoach ? AdaptivColors.text900 : Colors.white)),
          ],
        ),
      ),
    );
  }
}
