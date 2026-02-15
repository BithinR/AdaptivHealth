/*
TargetZoneIndicator - Heart rate zone visualization widget.

Displays a 5-zone HR bar with current position indicator.
Shows Resting, Light, Moderate, Hard, and Maximum zones
with color coding matching the design system.

Usage:
```dart
TargetZoneIndicator(
  currentBPM: 125,
  targetZone: HRZone.moderate,
  maxHR: 190,
  showLabels: true,
)
```
*/

import 'package:flutter/material.dart';
import '../theme/colors.dart';
import '../theme/typography.dart';
import 'recommendation_card.dart' show HRZone;

class TargetZoneIndicator extends StatelessWidget {
  /// Current heart rate in BPM
  final int currentBPM;
  
  /// Target zone for current workout (optional)
  final HRZone? targetZone;
  
  /// Maximum heart rate for the user (default 220 - age)
  final int maxHR;
  
  /// Minimum heart rate (resting)
  final int minHR;
  
  /// Whether to show zone labels
  final bool showLabels;
  
  /// Whether to show current BPM value
  final bool showCurrentValue;
  
  /// Orientation of the indicator
  final Axis orientation;

  const TargetZoneIndicator({
    super.key,
    required this.currentBPM,
    this.targetZone,
    this.maxHR = 190,
    this.minHR = 50,
    this.showLabels = true,
    this.showCurrentValue = true,
    this.orientation = Axis.horizontal,
  });

  /// Get the HR zone for a given BPM
  HRZone _getZoneForBPM(int bpm) {
    final range = maxHR - minHR;
    final normalizedBpm = bpm - minHR;
    final percentage = normalizedBpm / range;
    
    if (percentage < 0.14) return HRZone.resting;
    if (percentage < 0.36) return HRZone.light;
    if (percentage < 0.64) return HRZone.moderate;
    if (percentage < 0.86) return HRZone.hard;
    return HRZone.maximum;
  }

  double _getPositionPercentage() {
    final clampedBPM = currentBPM.clamp(minHR, maxHR);
    return (clampedBPM - minHR) / (maxHR - minHR);
  }

  Color _getZoneColor(HRZone zone) {
    switch (zone) {
      case HRZone.resting:
        return AdaptivColors.hrResting;
      case HRZone.light:
        return AdaptivColors.hrLight;
      case HRZone.moderate:
        return AdaptivColors.hrModerate;
      case HRZone.hard:
        return AdaptivColors.hrHard;
      case HRZone.maximum:
        return AdaptivColors.hrMaximum;
    }
  }

  String _getZoneLabel(HRZone zone) {
    switch (zone) {
      case HRZone.resting:
        return 'Rest';
      case HRZone.light:
        return 'Light';
      case HRZone.moderate:
        return 'Mod';
      case HRZone.hard:
        return 'Hard';
      case HRZone.maximum:
        return 'Max';
    }
  }

  @override
  Widget build(BuildContext context) {
    if (orientation == Axis.vertical) {
      return _buildVertical(context);
    }
    return _buildHorizontal(context);
  }

  Widget _buildHorizontal(BuildContext context) {
    final currentZone = _getZoneForBPM(currentBPM);
    final positionPercent = _getPositionPercentage();

    return Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Current value badge (positioned above indicator)
        if (showCurrentValue)
          Padding(
            padding: const EdgeInsets.only(bottom: 8),
            child: Row(
              children: [
                Icon(
                  Icons.favorite,
                  size: 16,
                  color: _getZoneColor(currentZone),
                ),
                const SizedBox(width: 4),
                Text(
                  currentBPM.toString(),
                  style: AdaptivTypography.metricValueSmall.copyWith(
                    color: _getZoneColor(currentZone),
                  ),
                ),
                const SizedBox(width: 2),
                Text(
                  'BPM',
                  style: AdaptivTypography.label.copyWith(
                    color: AdaptivColors.text500,
                  ),
                ),
                const Spacer(),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                  decoration: BoxDecoration(
                    color: _getZoneColor(currentZone).withOpacity(0.1),
                    borderRadius: BorderRadius.circular(4),
                  ),
                  child: Text(
                    _getZoneLabel(currentZone),
                    style: AdaptivTypography.overline.copyWith(
                      color: _getZoneColor(currentZone),
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
              ],
            ),
          ),
        
        // Zone bar
        SizedBox(
          height: 24,
          child: LayoutBuilder(
            builder: (context, constraints) {
              final width = constraints.maxWidth;
              final indicatorX = positionPercent * width;
              
              return Stack(
                clipBehavior: Clip.none,
                children: [
                  // Zone segments
                  Row(
                    children: [
                      _ZoneSegment(
                        zone: HRZone.resting,
                        color: _getZoneColor(HRZone.resting),
                        isTarget: targetZone == HRZone.resting,
                        flex: 14,
                        isFirst: true,
                      ),
                      _ZoneSegment(
                        zone: HRZone.light,
                        color: _getZoneColor(HRZone.light),
                        isTarget: targetZone == HRZone.light,
                        flex: 22,
                      ),
                      _ZoneSegment(
                        zone: HRZone.moderate,
                        color: _getZoneColor(HRZone.moderate),
                        isTarget: targetZone == HRZone.moderate,
                        flex: 28,
                      ),
                      _ZoneSegment(
                        zone: HRZone.hard,
                        color: _getZoneColor(HRZone.hard),
                        isTarget: targetZone == HRZone.hard,
                        flex: 22,
                      ),
                      _ZoneSegment(
                        zone: HRZone.maximum,
                        color: _getZoneColor(HRZone.maximum),
                        isTarget: targetZone == HRZone.maximum,
                        flex: 14,
                        isLast: true,
                      ),
                    ],
                  ),
                  
                  // Position indicator
                  Positioned(
                    left: indicatorX - 8,
                    top: -4,
                    child: Container(
                      width: 16,
                      height: 32,
                      decoration: BoxDecoration(
                        color: AdaptivColors.white,
                        borderRadius: BorderRadius.circular(4),
                        border: Border.all(
                          color: _getZoneColor(currentZone),
                          width: 2,
                        ),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.black.withOpacity(0.15),
                            blurRadius: 4,
                            offset: const Offset(0, 2),
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              );
            },
          ),
        ),

        // Zone labels
        if (showLabels)
          Padding(
            padding: const EdgeInsets.only(top: 8),
            child: Row(
              children: [
                _ZoneLabel(label: _getZoneLabel(HRZone.resting), flex: 14),
                _ZoneLabel(label: _getZoneLabel(HRZone.light), flex: 22),
                _ZoneLabel(label: _getZoneLabel(HRZone.moderate), flex: 28),
                _ZoneLabel(label: _getZoneLabel(HRZone.hard), flex: 22),
                _ZoneLabel(label: _getZoneLabel(HRZone.maximum), flex: 14),
              ],
            ),
          ),
      ],
    );
  }

  Widget _buildVertical(BuildContext context) {
    final currentZone = _getZoneForBPM(currentBPM);
    final positionPercent = _getPositionPercentage();

    return Row(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Zone bar (vertical)
        SizedBox(
          width: 24,
          height: 200,
          child: LayoutBuilder(
            builder: (context, constraints) {
              final height = constraints.maxHeight;
              // Invert position for vertical (bottom = low, top = high)
              final indicatorY = (1 - positionPercent) * height;
              
              return Stack(
                clipBehavior: Clip.none,
                children: [
                  // Zone segments (reversed for vertical)
                  Column(
                    children: [
                      _VerticalZoneSegment(
                        color: _getZoneColor(HRZone.maximum),
                        isTarget: targetZone == HRZone.maximum,
                        flex: 14,
                        isFirst: true,
                      ),
                      _VerticalZoneSegment(
                        color: _getZoneColor(HRZone.hard),
                        isTarget: targetZone == HRZone.hard,
                        flex: 22,
                      ),
                      _VerticalZoneSegment(
                        color: _getZoneColor(HRZone.moderate),
                        isTarget: targetZone == HRZone.moderate,
                        flex: 28,
                      ),
                      _VerticalZoneSegment(
                        color: _getZoneColor(HRZone.light),
                        isTarget: targetZone == HRZone.light,
                        flex: 22,
                      ),
                      _VerticalZoneSegment(
                        color: _getZoneColor(HRZone.resting),
                        isTarget: targetZone == HRZone.resting,
                        flex: 14,
                        isLast: true,
                      ),
                    ],
                  ),
                  
                  // Position indicator
                  Positioned(
                    left: -4,
                    top: indicatorY - 8,
                    child: Container(
                      width: 32,
                      height: 16,
                      decoration: BoxDecoration(
                        color: AdaptivColors.white,
                        borderRadius: BorderRadius.circular(4),
                        border: Border.all(
                          color: _getZoneColor(currentZone),
                          width: 2,
                        ),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.black.withOpacity(0.15),
                            blurRadius: 4,
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              );
            },
          ),
        ),
        
        // Labels column
        if (showLabels)
          Padding(
            padding: const EdgeInsets.only(left: 8),
            child: SizedBox(
              height: 200,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: HRZone.values.reversed.map((zone) {
                  return Text(
                    _getZoneLabel(zone),
                    style: AdaptivTypography.overline.copyWith(
                      color: _getZoneColor(zone),
                    ),
                  );
                }).toList(),
              ),
            ),
          ),
      ],
    );
  }
}

class _ZoneSegment extends StatelessWidget {
  final HRZone zone;
  final Color color;
  final bool isTarget;
  final int flex;
  final bool isFirst;
  final bool isLast;

  const _ZoneSegment({
    required this.zone,
    required this.color,
    required this.isTarget,
    required this.flex,
    this.isFirst = false,
    this.isLast = false,
  });

  @override
  Widget build(BuildContext context) {
    return Expanded(
      flex: flex,
      child: Container(
        height: double.infinity,
        decoration: BoxDecoration(
          color: color.withOpacity(isTarget ? 1.0 : 0.6),
          borderRadius: BorderRadius.horizontal(
            left: isFirst ? const Radius.circular(4) : Radius.zero,
            right: isLast ? const Radius.circular(4) : Radius.zero,
          ),
          border: isTarget
              ? Border.all(color: color, width: 2)
              : null,
        ),
      ),
    );
  }
}

class _VerticalZoneSegment extends StatelessWidget {
  final Color color;
  final bool isTarget;
  final int flex;
  final bool isFirst;
  final bool isLast;

  const _VerticalZoneSegment({
    required this.color,
    required this.isTarget,
    required this.flex,
    this.isFirst = false,
    this.isLast = false,
  });

  @override
  Widget build(BuildContext context) {
    return Expanded(
      flex: flex,
      child: Container(
        width: double.infinity,
        decoration: BoxDecoration(
          color: color.withOpacity(isTarget ? 1.0 : 0.6),
          borderRadius: BorderRadius.vertical(
            top: isFirst ? const Radius.circular(4) : Radius.zero,
            bottom: isLast ? const Radius.circular(4) : Radius.zero,
          ),
        ),
      ),
    );
  }
}

class _ZoneLabel extends StatelessWidget {
  final String label;
  final int flex;

  const _ZoneLabel({
    required this.label,
    required this.flex,
  });

  @override
  Widget build(BuildContext context) {
    return Expanded(
      flex: flex,
      child: Text(
        label,
        textAlign: TextAlign.center,
        style: AdaptivTypography.overline.copyWith(
          color: AdaptivColors.text500,
        ),
      ),
    );
  }
}

/// Compact version for inline display
class CompactZoneIndicator extends StatelessWidget {
  final int currentBPM;
  final int maxHR;
  final int minHR;

  const CompactZoneIndicator({
    super.key,
    required this.currentBPM,
    this.maxHR = 190,
    this.minHR = 50,
  });

  @override
  Widget build(BuildContext context) {
    final range = maxHR - minHR;
    final percentage = ((currentBPM - minHR) / range).clamp(0.0, 1.0);
    final zone = AdaptivColors.getHRZoneLabel(currentBPM);
    final color = AdaptivColors.getHRZoneColor(currentBPM);

    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        // Mini bar
        Container(
          width: 40,
          height: 8,
          decoration: BoxDecoration(
            color: AdaptivColors.bg200,
            borderRadius: BorderRadius.circular(4),
          ),
          child: Align(
            alignment: Alignment.centerLeft,
            child: FractionallySizedBox(
              widthFactor: percentage,
              child: Container(
                decoration: BoxDecoration(
                  color: color,
                  borderRadius: BorderRadius.circular(4),
                ),
              ),
            ),
          ),
        ),
        const SizedBox(width: 6),
        Text(
          zone,
          style: AdaptivTypography.overline.copyWith(
            color: color,
            fontWeight: FontWeight.w600,
          ),
        ),
      ],
    );
  }
}
