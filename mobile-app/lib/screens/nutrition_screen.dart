import 'package:flutter/material.dart';
import '../theme/colors.dart';
import '../theme/typography.dart';

class NutritionScreen extends StatelessWidget {
  const NutritionScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AdaptivColors.bg100,
      appBar: AppBar(
        backgroundColor: AdaptivColors.white,
        elevation: 0,
        title: Text('Nutrition', style: AdaptivTypography.screenTitle),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _buildDailyGoals(),
          const SizedBox(height: 24),
          _buildMealCards(),
          const SizedBox(height: 24),
          _buildProgressTracking(),
          const SizedBox(height: 24),
          _buildNutritionistIntegration(),
        ],
      ),
    );
  }

  Widget _buildDailyGoals() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Daily Nutrition Goals', style: AdaptivTypography.sectionTitle),
            const SizedBox(height: 8),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                _buildGoalItem('Calories', '1800 kcal'),
                _buildGoalItem('Protein', '90g'),
                _buildGoalItem('Carbs', '200g'),
                _buildGoalItem('Fat', '60g'),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildGoalItem(String label, String value) {
    return Column(
      children: [
        Text(value, style: AdaptivTypography.metricValue),
        Text(label, style: AdaptivTypography.caption),
      ],
    );
  }

  Widget _buildMealCards() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Meals', style: AdaptivTypography.sectionTitle),
        const SizedBox(height: 8),
        Card(
          child: ListTile(
            leading: const Icon(Icons.breakfast_dining),
            title: const Text('Breakfast'),
            subtitle: const Text('Oatmeal, Berries, Almonds'),
            trailing: const Text('350 kcal'),
          ),
        ),
        Card(
          child: ListTile(
            leading: const Icon(Icons.lunch_dining),
            title: const Text('Lunch'),
            subtitle: const Text('Grilled Chicken, Quinoa, Broccoli'),
            trailing: const Text('500 kcal'),
          ),
        ),
        Card(
          child: ListTile(
            leading: const Icon(Icons.dinner_dining),
            title: const Text('Dinner'),
            subtitle: const Text('Salmon, Brown Rice, Asparagus'),
            trailing: const Text('600 kcal'),
          ),
        ),
        Card(
          child: ListTile(
            leading: const Icon(Icons.emoji_food_beverage),
            title: const Text('Snacks'),
            subtitle: const Text('Greek Yogurt, Apple'),
            trailing: const Text('200 kcal'),
          ),
        ),
      ],
    );
  }

  Widget _buildProgressTracking() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Progress Tracking', style: AdaptivTypography.sectionTitle),
            const SizedBox(height: 12),
            LinearProgressIndicator(
              value: 0.75,
              backgroundColor: AdaptivColors.bg200,
              valueColor: AlwaysStoppedAnimation(AdaptivColors.primary),
              minHeight: 10,
            ),
            const SizedBox(height: 8),
            Text('1350 / 1800 kcal consumed', style: AdaptivTypography.caption),
          ],
        ),
      ),
    );
  }

  Widget _buildNutritionistIntegration() {
    return Card(
      child: ListTile(
        leading: const Icon(Icons.support_agent, color: AdaptivColors.primary),
        title: const Text('Chat with Nutritionist'),
        subtitle: const Text('Ask questions or get meal advice'),
        trailing: ElevatedButton(
          onPressed: () {},
          child: const Text('Start Chat'),
        ),
      ),
    );
  }
}
