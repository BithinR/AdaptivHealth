// #commentline: Import necessary Flutter and theme packages
import 'package:flutter/material.dart';
import '../theme/colors.dart';
import '../theme/typography.dart';

// #commentline: WeekViewCalendar widget definition with parameters for callback and selected date
class WeekViewCalendar extends StatelessWidget {
  // #commentline: Callback when a day is selected
  final Function(DateTime) onDaySelected;
  // #commentline: Optional pre-selected date
  final DateTime? selectedDate;

  // #commentline: Constructor for WeekViewCalendar
  const WeekViewCalendar({
    super.key,
    required this.onDaySelected,
    this.selectedDate,
  });

  // #commentline: Build method to render the week view calendar
  @override
  Widget build(BuildContext context) {
    // #commentline: Get current date and calculate start of week (Monday)
    final now = DateTime.now();
    final startOfWeek = now.subtract(Duration(days: now.weekday - 1));
    // #commentline: Generate list of 7 days for the week
    final days = List.generate(7, (i) => DateTime(
      startOfWeek.year,
      startOfWeek.month,
      startOfWeek.day + i,
    ));

    // #commentline: Render horizontally scrollable row of days
    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      child: Row(
        children: days.map((date) {
          // #commentline: Check if this day is selected
          final isSelected = selectedDate != null &&
              date.year == selectedDate!.year &&
              date.month == selectedDate!.month &&
              date.day == selectedDate!.day;
          // #commentline: Check if this day is today
          final isToday = date.year == now.year &&
              date.month == now.month &&
              date.day == now.day;

          // #commentline: Day abbreviation (Mon, Tue, ...)
          final dayAbbr = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][date.weekday - 1];

          // #commentline: Widget for each day
          return GestureDetector(
            onTap: () => onDaySelected(date),
            child: Container(
              margin: const EdgeInsets.symmetric(horizontal: 6, vertical: 8),
              padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 14),
              decoration: BoxDecoration(
                color: isSelected ? AdaptivColors.primary : AdaptivColors.bg200,
                borderRadius: BorderRadius.circular(10),
                border: isToday
                    ? Border.all(
                        color: AdaptivColors.primary,
                        width: 2,
                      )
                    : null,
                boxShadow: isSelected
                    ? [
                        BoxShadow(
                          color: AdaptivColors.primary.withOpacity(0.15),
                          blurRadius: 6,
                          offset: const Offset(0, 2),
                        ),
                      ]
                    : [],
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  // #commentline: Display day abbreviation
                  Text(
                    dayAbbr,
                    style: AdaptivTypography.label.copyWith(
                      color: isSelected ? Colors.white : AdaptivColors.text600,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  const SizedBox(height: 4),
                  // #commentline: Display date number
                  Text(
                    date.day.toString(),
                    style: AdaptivTypography.metricValue.copyWith(
                      color: isSelected ? Colors.white : AdaptivColors.text900,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
            ),
          );
        }).toList(),
      ),
    );
  }
}
