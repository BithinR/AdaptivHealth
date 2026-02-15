/*
Activity Detail Screen - Shows detailed information about a specific activity.

Displays comprehensive information including:
- Activity summary (duration, calories, distance)
- Heart rate chart during activity
- Zone distribution
- Route map (if GPS data available)
- Performance insights
*/

import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../theme/colors.dart';
import '../theme/typography.dart';
import '../widgets/widgets.dart';

class ActivityDetailScreen extends StatelessWidget {
  final Map<String, dynamic> activity;

  const ActivityDetailScreen({
    super.key,
    required this.activity,
  });

  String get _activityType => activity['activity_type'] ?? 'Workout';
  String get _title => activity['title'] ?? _activityType;
  int get _duration => activity['duration_minutes'] ?? 0;
  int get _avgHR => activity['avg_heart_rate'] ?? 0;
  int get _maxHR => activity['max_heart_rate'] ?? 0;
  int get _minHR => activity['min_heart_rate'] ?? 0;
  int get _calories => activity['calories_burned'] ?? 0;
  double get _distance => (activity['distance_km'] ?? 0).toDouble();
  String get _timestamp => activity['start_time'] ?? '';

  String _formatDateTime(String isoString) {
    if (isoString.isEmpty) return 'Unknown';
    try {
      final date = DateTime.parse(isoString);
      return DateFormat('EEEE, MMMM d, yyyy • h:mm a').format(date);
    } catch (e) {
      return 'Unknown';
    }
  }

  String _formatDuration(int minutes) {
    if (minutes < 60) return '$minutes min';
    final hours = minutes ~/ 60;
    final mins = minutes % 60;
    if (mins == 0) return '${hours}h';
    return '${hours}h ${mins}m';
  }

  IconData _getActivityIcon() {
    switch (_activityType.toLowerCase()) {
      case 'walking':
        return Icons.directions_walk;
      case 'running':
        return Icons.directions_run;
      case 'cycling':
        return Icons.directions_bike;
      case 'swimming':
        return Icons.pool;
      case 'yoga':
      case 'stretching':
        return Icons.self_improvement;
      case 'strength':
        return Icons.fitness_center;
      case 'hiit':
        return Icons.whatshot;
      default:
        return Icons.fitness_center;
    }
  }

  Color _getActivityColor() {
    switch (_activityType.toLowerCase()) {
      case 'walking':
        return AdaptivColors.stable;
      case 'running':
        return AdaptivColors.primary;
      case 'cycling':
        return const Color(0xFF00BCD4);
      case 'swimming':
        return const Color(0xFF2196F3);
      case 'yoga':
      case 'stretching':
        return const Color(0xFF9C27B0);
      case 'strength':
        return const Color(0xFFFF5722);
      case 'hiit':
        return AdaptivColors.critical;
      default:
        return AdaptivColors.primary;
    }
  }

  @override
  Widget build(BuildContext context) {
    final color = _getActivityColor();

    return Scaffold(
      backgroundColor: AdaptivColors.bg100,
      body: CustomScrollView(
        slivers: [
          // App bar with activity header
          SliverAppBar(
            expandedHeight: 200,
            pinned: true,
            backgroundColor: color,
            leading: IconButton(
              icon: const Icon(Icons.arrow_back, color: Colors.white),
              onPressed: () => Navigator.pop(context),
            ),
            actions: [
              IconButton(
                icon: const Icon(Icons.share, color: Colors.white),
                onPressed: () {
                  // Share activity
                },
              ),
              IconButton(
                icon: const Icon(Icons.more_vert, color: Colors.white),
                onPressed: () {
                  // More options
                },
              ),
            ],
            flexibleSpace: FlexibleSpaceBar(
              background: Container(
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                    colors: [color, color.withOpacity(0.7)],
                  ),
                ),
                child: SafeArea(
                  child: Padding(
                    padding: const EdgeInsets.fromLTRB(16, 60, 16, 16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      mainAxisAlignment: MainAxisAlignment.end,
                      children: [
                        Row(
                          children: [
                            Container(
                              padding: const EdgeInsets.all(12),
                              decoration: BoxDecoration(
                                color: Colors.white.withOpacity(0.2),
                                borderRadius: BorderRadius.circular(12),
                              ),
                              child: Icon(
                                _getActivityIcon(),
                                color: Colors.white,
                                size: 28,
                              ),
                            ),
                            const SizedBox(width: 16),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    _title,
                                    style: AdaptivTypography.screenTitle.copyWith(
                                      color: Colors.white,
                                    ),
                                  ),
                                  const SizedBox(height: 4),
                                  Text(
                                    _formatDateTime(_timestamp),
                                    style: AdaptivTypography.caption.copyWith(
                                      color: Colors.white.withOpacity(0.9),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),
          ),

          // Quick stats row
          SliverToBoxAdapter(
            child: _buildQuickStats(color),
          ),

          // Heart rate section
          SliverToBoxAdapter(
            child: _buildHeartRateSection(),
          ),

          // Zone distribution
          SliverToBoxAdapter(
            child: _buildZoneDistribution(),
          ),

          // Performance insights
          SliverToBoxAdapter(
            child: _buildInsights(color),
          ),

          // Bottom padding
          const SliverToBoxAdapter(
            child: SizedBox(height: 32),
          ),
        ],
      ),
    );
  }

  Widget _buildQuickStats(Color color) {
    return Container(
      margin: const EdgeInsets.all(16),
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AdaptivColors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          _buildStatItem(
            Icons.timer_outlined,
            _formatDuration(_duration),
            'Duration',
            color,
          ),
          _buildStatDivider(),
          _buildStatItem(
            Icons.local_fire_department,
            _calories.toString(),
            'Calories',
            AdaptivColors.warning,
          ),
          if (_distance > 0) ...[
            _buildStatDivider(),
            _buildStatItem(
              Icons.straighten,
              '${_distance.toStringAsFixed(1)} km',
              'Distance',
              AdaptivColors.stable,
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildStatItem(IconData icon, String value, String label, Color color) {
    return Column(
      children: [
        Icon(icon, color: color, size: 24),
        const SizedBox(height: 8),
        Text(
          value,
          style: AdaptivTypography.metricValue.copyWith(
            fontSize: 24,
          ),
        ),
        const SizedBox(height: 4),
        Text(
          label,
          style: AdaptivTypography.caption,
        ),
      ],
    );
  }

  Widget _buildStatDivider() {
    return Container(
      height: 50,
      width: 1,
      color: AdaptivColors.border300,
    );
  }

  Widget _buildHeartRateSection() {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AdaptivColors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AdaptivColors.border300),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: AdaptivColors.critical.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: const Icon(
                  Icons.favorite,
                  color: AdaptivColors.critical,
                  size: 20,
                ),
              ),
              const SizedBox(width: 12),
              Text(
                'Heart Rate',
                style: AdaptivTypography.subtitle1.copyWith(
                  fontWeight: FontWeight.w700,
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          // HR Stats row
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              _buildHRStat('Avg', _avgHR, AdaptivColors.primary),
              _buildHRStat('Max', _maxHR, AdaptivColors.critical),
              _buildHRStat('Min', _minHR, AdaptivColors.stable),
            ],
          ),
          const SizedBox(height: 16),
          // HR Chart placeholder
          Container(
            height: 120,
            decoration: BoxDecoration(
              color: AdaptivColors.bg100,
              borderRadius: BorderRadius.circular(12),
            ),
            child: Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    Icons.show_chart,
                    size: 32,
                    color: AdaptivColors.text500,
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'Heart rate chart',
                    style: AdaptivTypography.caption,
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildHRStat(String label, int value, Color color) {
    return Column(
      children: [
        Text(
          label,
          style: AdaptivTypography.caption,
        ),
        const SizedBox(height: 4),
        Text(
          value.toString(),
          style: AdaptivTypography.metricValue.copyWith(
            color: color,
            fontSize: 28,
          ),
        ),
        Text(
          'BPM',
          style: AdaptivTypography.overline.copyWith(
            color: AdaptivColors.text500,
          ),
        ),
      ],
    );
  }

  Widget _buildZoneDistribution() {
    // Demo zone data
    final zones = [
      {'zone': 'Maximum', 'percent': 5, 'color': AdaptivColors.hrMaximum},
      {'zone': 'Hard', 'percent': 25, 'color': AdaptivColors.hrHard},
      {'zone': 'Moderate', 'percent': 40, 'color': AdaptivColors.hrModerate},
      {'zone': 'Light', 'percent': 20, 'color': AdaptivColors.hrLight},
      {'zone': 'Resting', 'percent': 10, 'color': AdaptivColors.hrResting},
    ];

    return Container(
      margin: const EdgeInsets.all(16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AdaptivColors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AdaptivColors.border300),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'HR Zone Distribution',
            style: AdaptivTypography.subtitle1.copyWith(
              fontWeight: FontWeight.w700,
            ),
          ),
          const SizedBox(height: 16),
          // Zone bar
          ClipRRect(
            borderRadius: BorderRadius.circular(8),
            child: Row(
              children: zones.map((zone) {
                return Expanded(
                  flex: zone['percent'] as int,
                  child: Container(
                    height: 24,
                    color: zone['color'] as Color,
                  ),
                );
              }).toList(),
            ),
          ),
          const SizedBox(height: 16),
          // Zone legend
          ...zones.map((zone) => Padding(
            padding: const EdgeInsets.only(bottom: 8),
            child: Row(
              children: [
                Container(
                  width: 12,
                  height: 12,
                  decoration: BoxDecoration(
                    color: zone['color'] as Color,
                    borderRadius: BorderRadius.circular(3),
                  ),
                ),
                const SizedBox(width: 8),
                Text(
                  zone['zone'] as String,
                  style: AdaptivTypography.bodySmall,
                ),
                const Spacer(),
                Text(
                  '${zone['percent']}%',
                  style: AdaptivTypography.body.copyWith(
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ],
            ),
          )),
        ],
      ),
    );
  }

  Widget _buildInsights(Color color) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: color.withOpacity(0.3)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(Icons.lightbulb_outline, color: color, size: 20),
              const SizedBox(width: 8),
              Text(
                'AI Insights',
                style: AdaptivTypography.subtitle1.copyWith(
                  fontWeight: FontWeight.w700,
                  color: color,
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Text(
            _getInsightText(),
            style: AdaptivTypography.body.copyWith(
              color: AdaptivColors.text700,
            ),
          ),
        ],
      ),
    );
  }

  String _getInsightText() {
    if (_avgHR > 0 && _duration > 0) {
      if (_avgHR > 140) {
        return 'Great high-intensity session! Your heart rate averaged $_avgHR BPM, indicating a challenging workout. Consider a recovery session tomorrow.';
      } else if (_avgHR > 100) {
        return 'Good moderate workout! You spent most of the time in the fat-burning zone. This type of exercise is excellent for cardiovascular health.';
      } else {
        return 'Nice recovery session! Low-intensity activities like this help your body recover while still staying active.';
      }
    }
    return 'Keep tracking your activities to get personalized insights about your exercise patterns.';
  }
}
