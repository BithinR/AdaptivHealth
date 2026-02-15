import 'package:flutter/material.dart';
import '../theme/colors.dart';
import '../theme/typography.dart';

class WeekView extends StatelessWidget {
  final DateTime selectedDate;
  final ValueChanged<DateTime> onDateSelected;

  const WeekView({
    super.key,
    required this.selectedDate,
    required this.onDateSelected,
  });

  @override
  Widget build(BuildContext context) {
    final now = DateTime.now();
    final startOfWeek = now.subtract(Duration(days: now.weekday - 1));
    final days = List.generate(7, (i) => startOfWeek.add(Duration(days: i)));

    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: days.map((date) {
        final isSelected = date.day == selectedDate.day && date.month == selectedDate.month && date.year == selectedDate.year;
        return GestureDetector(
          onTap: () => onDateSelected(date),
          child: Container(
            padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 12),
            decoration: BoxDecoration(
              color: isSelected ? AdaptivColors.primary : AdaptivColors.bg200,
              borderRadius: BorderRadius.circular(8),
            ),
            child: Column(
              children: [
                Text(
                  ['M', 'T', 'W', 'T', 'F', 'S', 'S'][date.weekday - 1],
                  style: AdaptivTypography.label.copyWith(
                    color: isSelected ? Colors.white : AdaptivColors.text600,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  date.day.toString(),
                  style: AdaptivTypography.metricValue.copyWith(
                    color: isSelected ? Colors.white : AdaptivColors.text900,
                  ),
                ),
              ],
            ),
          ),
        );
      }).toList(),
    );
  }
}
