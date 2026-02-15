import 'package:flutter/material.dart';
import '../theme/colors.dart';
import '../theme/typography.dart';

class DoctorMessagingScreen extends StatelessWidget {
  const DoctorMessagingScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AdaptivColors.bg100,
      appBar: AppBar(
        backgroundColor: AdaptivColors.white,
        elevation: 0,
        title: Text('Doctor Messaging', style: AdaptivTypography.screenTitle),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _buildCareTeamList(),
          const SizedBox(height: 24),
          _buildConversationThreads(),
          const SizedBox(height: 24),
          _buildMessageComposer(),
        ],
      ),
    );
  }

  Widget _buildCareTeamList() {
    return Card(
      child: ListTile(
        leading: const Icon(Icons.medical_services, color: AdaptivColors.primary),
        title: const Text('Care Team'),
        subtitle: const Text('Dr. Smith, Nurse Lee, Dr. Patel'),
      ),
    );
  }

  Widget _buildConversationThreads() {
    return Card(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: Text('Conversations', style: AdaptivTypography.sectionTitle),
          ),
          ListTile(
            leading: const CircleAvatar(child: Icon(Icons.person)),
            title: const Text('Dr. Smith'),
            subtitle: const Text('How are you feeling today?'),
            trailing: const Text('2m ago'),
          ),
          ListTile(
            leading: const CircleAvatar(child: Icon(Icons.person)),
            title: const Text('Nurse Lee'),
            subtitle: const Text('Please update your vitals.'),
            trailing: const Text('1h ago'),
          ),
        ],
      ),
    );
  }

  Widget _buildMessageComposer() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Compose Message', style: AdaptivTypography.sectionTitle),
            const SizedBox(height: 8),
            TextField(
              decoration: const InputDecoration(
                hintText: 'Type your message...',
                border: OutlineInputBorder(),
              ),
              maxLines: 3,
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                ElevatedButton(
                  onPressed: () {},
                  child: const Text('Send'),
                ),
                const SizedBox(width: 8),
                IconButton(
                  icon: const Icon(Icons.attach_file),
                  onPressed: () {},
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
