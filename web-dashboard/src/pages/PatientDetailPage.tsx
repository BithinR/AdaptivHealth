/*
Patient detail page.

Shows detailed information about one patient:
- Current vital signs and risk score
- Historical trends over time
- Recent alerts
- AI recommendations
*/

import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Heart, Wind, Activity, AlertTriangle } from 'lucide-react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { api } from '../services/api';
import {
  AlertResponse,
  ActivitySessionResponse,
  RecommendationResponse,
  RiskAssessmentResponse,
  User,
  VitalSignResponse,
  VitalSignsHistoryResponse,
} from '../types';
import { colors } from '../theme/colors';
import { typography } from '../theme/typography';
import StatusBadge, { riskToStatus } from '../components/common/StatusBadge';

const PatientDetailPage: React.FC = () => {
  const { patientId } = useParams<{ patientId: string }>();
  const navigate = useNavigate();
  const [patient, setPatient] = useState<User | null>(null);
  const [latestVitals, setLatestVitals] = useState<VitalSignResponse | null>(null);
  const [riskAssessment, setRiskAssessment] = useState<RiskAssessmentResponse | null>(null);
  const [recommendation, setRecommendation] = useState<RecommendationResponse | null>(null);
  const [alerts, setAlerts] = useState<AlertResponse[]>([]);
  const [activities, setActivities] = useState<ActivitySessionResponse[]>([]);
  const [vitalsHistory, setVitalsHistory] = useState<VitalSignsHistoryResponse | null>(null);
  const [timeRange, setTimeRange] = useState<'1week' | '2weeks' | '1month' | '3months'>('1week');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadPatientData();
  }, [patientId, timeRange]);

  const rangeToDays = (range: typeof timeRange) => {
    switch (range) {
      case '2weeks':
        return 14;
      case '1month':
        return 30;
      case '3months':
        return 90;
      case '1week':
      default:
        return 7;
    }
  };

  const loadPatientData = async () => {
    try {
      if (!patientId) {
        throw new Error('Missing patient id');
      }

      const userId = Number(patientId);
      if (Number.isNaN(userId)) {
        throw new Error('Invalid patient id');
      }

      const days = rangeToDays(timeRange);

      const [user, vitals, risk, rec, alertsResponse, activitiesResponse, history] =
        await Promise.all([
          api.getUserById(userId),
          api.getLatestVitalSignsForUser(userId),
          api.getLatestRiskAssessmentForUser(userId),
          api.getLatestRecommendationForUser(userId),
          api.getAlertsForUser(userId, 1, 5),
          api.getActivitiesForUser(userId, 5, 0),
          api.getVitalSignsHistoryForUser(userId, days, 1, 100),
        ]);

      setPatient(user);
      setLatestVitals(vitals);
      setRiskAssessment(risk);
      setRecommendation(rec);
      setAlerts(alertsResponse.alerts ?? []);
      setActivities(activitiesResponse.activities ?? []);
      setVitalsHistory(history);
    } catch (error) {
      console.error('Error loading patient data:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatTimeAgo = (isoDate?: string) => {
    if (!isoDate) return 'Just now';
    const date = new Date(isoDate);
    const diffMs = Date.now() - date.getTime();
    const diffMin = Math.max(1, Math.floor(diffMs / 60000));
    if (diffMin < 60) return `${diffMin} min ago`;
    const diffHr = Math.floor(diffMin / 60);
    return `${diffHr} hr${diffHr > 1 ? 's' : ''} ago`;
  };

  const getRiskFactors = () => {
    const raw = riskAssessment?.risk_factors_json;
    if (!raw) return [] as string[];
    try {
      const parsed = JSON.parse(raw);
      if (Array.isArray(parsed)) {
        return parsed.map((item) => String(item));
      }
      if (typeof parsed === 'object' && parsed !== null) {
        return Object.values(parsed).map((item) => String(item));
      }
      return [String(parsed)];
    } catch {
      return [raw];
    }
  };

  if (loading) {
    return (
      <div style={{ padding: '32px', textAlign: 'center' }}>
        <p>Loading patient data...</p>
      </div>
    );
  }

  if (!patient || !latestVitals) {
    return (
      <div style={{ padding: '32px' }}>
        <p>Patient data not found</p>
      </div>
    );
  }

  // Helper function to get vital status
  const getVitalStatus = (value: number, type: 'hr' | 'spo2' | 'bp'): 'stable' | 'warning' | 'critical' => {
    if (type === 'hr') {
      if (value > 130) return 'critical';
      if (value > 110) return 'warning';
      return 'stable';
    }
    if (type === 'spo2') {
      if (value < 90) return 'critical';
      if (value < 95) return 'warning';
      return 'stable';
    }
    if (type === 'bp') {
      if (value > 140) return 'critical';
      if (value > 130) return 'warning';
      return 'stable';
    }
    return 'stable';
  };

  const riskStatus = riskToStatus(riskAssessment?.risk_level || 'low');
  const riskFactors = getRiskFactors();
  const systolic = latestVitals?.blood_pressure?.systolic ?? 0;
  const diastolic = latestVitals?.blood_pressure?.diastolic ?? 0;

  return (
    <div style={{ minHeight: '100vh', backgroundColor: colors.neutral['50'] }}>
      {/* Header */}
      <header
        style={{
          backgroundColor: colors.neutral.white,
          borderBottom: `1px solid ${colors.neutral['300']}`,
          padding: '16px 32px',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <button
            onClick={() => navigate('/patients')}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              padding: '8px 12px',
              backgroundColor: 'transparent',
              border: 'none',
              cursor: 'pointer',
              color: colors.primary.default,
              fontWeight: 500,
            }}
          >
            <ArrowLeft size={20} />
            Back to Patients
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main style={{ maxWidth: '1440px', margin: '0 auto', padding: '32px' }}>
        {/* Patient Header */}
        <div
          style={{
            backgroundColor: colors.neutral.white,
            border: `1px solid ${colors.neutral['300']}`,
            borderRadius: '12px',
            padding: '24px',
            marginBottom: '32px',
            boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'flex-start', gap: '24px' }}>
            {/* Avatar */}
            <div
              style={{
                width: '64px',
                height: '64px',
                borderRadius: '50%',
                backgroundColor: colors.primary.light,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                flexShrink: 0,
                fontSize: '24px',
                fontWeight: 700,
                color: colors.primary.default,
              }}
            >
              {patient.full_name?.substring(0, 2).toUpperCase()}
            </div>

            {/* Patient Info */}
            <div style={{ flex: 1 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '8px' }}>
                <h1 style={{ ...typography.sectionTitle, margin: 0 }}>{patient.full_name}</h1>
                <StatusBadge status={riskStatus} />
              </div>
              <p style={{ ...typography.body, margin: '4px 0' }}>
                {patient.gender?.charAt(0).toUpperCase()}{patient.gender?.slice(1) || 'N/A'}, {patient.age} years old
              </p>
              <p style={{ ...typography.caption, margin: '4px 0' }}>
                Last reading: {formatTimeAgo(latestVitals.timestamp)}
              </p>
              <p style={{ ...typography.caption, margin: '4px 0' }}>
                Device: {latestVitals.source_device || 'Unknown device'}
              </p>
            </div>
          </div>
        </div>

        {/* Current Vitals Grid */}
        <h2 style={{ ...typography.sectionTitle, marginBottom: '16px' }}>Current Vitals</h2>
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: '16px',
            marginBottom: '32px',
          }}
        >
          {/* Heart Rate */}
          <div
            style={{
              backgroundColor: colors.neutral.white,
              border: `1px solid ${colors.neutral['300']}`,
              borderRadius: '12px',
              padding: '20px',
              boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
              <Heart size={20} color={colors.critical.badge} />
              <span style={typography.overline}>Heart Rate</span>
            </div>
            <div style={{ ...typography.bigNumber, marginBottom: '4px' }}>
              {latestVitals.heart_rate}
            </div>
            <div style={typography.bigNumberUnit}>BPM</div>
            <div
              style={{
                ...typography.caption,
                marginTop: '8px',
                color: getVitalStatus(latestVitals.heart_rate, 'hr') === 'critical'
                  ? colors.critical.text
                  : getVitalStatus(latestVitals.heart_rate, 'hr') === 'warning'
                  ? colors.warning.text
                  : colors.stable.text,
              }}
            >
              ↑ High
            </div>
          </div>

          {/* SpO2 */}
          <div
            style={{
              backgroundColor: colors.neutral.white,
              border: `1px solid ${colors.neutral['300']}`,
              borderRadius: '12px',
              padding: '20px',
              boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
              <Wind size={20} color={colors.critical.badge} />
              <span style={typography.overline}>SpO2</span>
            </div>
            <div style={{ ...typography.bigNumber, marginBottom: '4px' }}>
              {(latestVitals.spo2 ?? 0).toFixed(0)}%
            </div>
            <div
              style={{
                ...typography.caption,
                marginTop: '8px',
                color: (latestVitals.spo2 ?? 0) < 90 ? colors.critical.text : colors.warning.text,
              }}
            >
              ↓ Low
            </div>
          </div>

          {/* Blood Pressure */}
          <div
            style={{
              backgroundColor: colors.neutral.white,
              border: `1px solid ${colors.neutral['300']}`,
              borderRadius: '12px',
              padding: '20px',
              boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
              <Activity size={20} color={colors.critical.badge} />
              <span style={typography.overline}>Blood Pressure</span>
            </div>
            <div style={{ ...typography.bigNumber, marginBottom: '4px' }}>
              {systolic || '--'}/{diastolic || '--'}
            </div>
            <div
              style={{
                ...typography.caption,
                marginTop: '8px',
                color: getVitalStatus(systolic, 'bp') === 'critical'
                  ? colors.critical.text
                  : getVitalStatus(systolic, 'bp') === 'warning'
                  ? colors.warning.text
                  : colors.stable.text,
              }}
            >
              ↑ High
            </div>
          </div>

          {/* Risk Score */}
          <div
            style={{
              backgroundColor: colors.neutral.white,
              border: `1px solid ${colors.neutral['300']}`,
              borderRadius: '12px',
              padding: '20px',
              boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
              <AlertTriangle size={20} color={colors.critical.badge} />
              <span style={typography.overline}>Risk Level</span>
            </div>
            <div style={{ ...typography.bigNumber, marginBottom: '4px', color: colors.critical.badge }}>
              {riskAssessment?.risk_level?.toUpperCase()}
            </div>
            <div style={{ ...typography.body, color: colors.neutral['700'] }}>
              {(riskAssessment?.risk_score || 0).toFixed(2)}
            </div>
          </div>
        </div>

        {/* Time Range Tabs */}
        <div style={{ marginBottom: '32px', display: 'flex', gap: '8px' }}>
          {['1week', '2weeks', '1month', '3months'].map((range) => (
            <button
              key={range}
              onClick={() => setTimeRange(range as any)}
              style={{
                padding: '8px 16px',
                borderRadius: '6px',
                border: 'none',
                backgroundColor: timeRange === range ? colors.primary.default : colors.neutral['100'],
                color: timeRange === range ? colors.neutral.white : colors.neutral['700'],
                cursor: 'pointer',
                fontWeight: 500,
                transition: 'all 0.2s',
              }}
            >
              {range === '1week' && '1 Week'}
              {range === '2weeks' && '2 Weeks'}
              {range === '1month' && '1 Month'}
              {range === '3months' && '3 Months'}
            </button>
          ))}
        </div>

        {/* Heart Rate History Chart */}
        <div
          style={{
            backgroundColor: colors.neutral.white,
            border: `1px solid ${colors.neutral['300']}`,
            borderRadius: '12px',
            padding: '24px',
            marginBottom: '32px',
            boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
          }}
        >
          <h3 style={{ ...typography.sectionTitle, marginBottom: '16px' }}>Heart Rate History</h3>
          {vitalsHistory?.vitals?.length ? (
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={vitalsHistory.vitals.map((v) => ({
                time: new Date(v.timestamp).toLocaleTimeString('en-US', {
                  hour: 'numeric',
                  minute: '2-digit',
                  hour12: true,
                }),
                hr: v.heart_rate,
                spo2: v.spo2,
                systolic: v.blood_pressure?.systolic || null,
                timestamp: v.timestamp,
              }))}>
                <CartesianGrid strokeDasharray="3 3" stroke={colors.neutral['200']} />
                <XAxis
                  dataKey="time"
                  stroke={colors.neutral['500']}
                  style={{ fontSize: '12px' }}
                />
                <YAxis
                  stroke={colors.neutral['500']}
                  style={{ fontSize: '12px' }}
                  domain={[40, 180]}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: colors.neutral.white,
                    border: `1px solid ${colors.neutral['300']}`,
                    borderRadius: '6px',
                  }}
                  formatter={(value) => (value !== null ? value.toFixed(1) : 'N/A')}
                />
                <Legend wrapperStyle={{ paddingTop: '16px' }} />
                <Line
                  type="monotone"
                  dataKey="hr"
                  stroke={colors.semantic.critical}
                  name="Heart Rate (BPM)"
                  dot={false}
                  strokeWidth={2}
                />
                <Line
                  type="monotone"
                  dataKey="spo2"
                  stroke={colors.semantic.warning}
                  name="SpO2 (%)"
                  dot={false}
                  strokeWidth={2}
                />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div
              style={{
                height: '300px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                backgroundColor: colors.neutral['50'],
                borderRadius: '8px',
                color: colors.neutral['500'],
              }}
            >
              No vitals history available for chart
            </div>
          )}
        </div>

        {/* Two Column History Panels */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))',
            gap: '16px',
            marginBottom: '32px',
          }}
        >
          {/* Alert History */}
          <div
            style={{
              backgroundColor: colors.neutral.white,
              border: `1px solid ${colors.neutral['300']}`,
              borderRadius: '12px',
              padding: '24px',
              boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
            }}
          >
            <h3 style={{ ...typography.sectionTitle, marginBottom: '16px' }}>Alert History</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {alerts.length === 0 ? (
                <div style={{ padding: '12px', backgroundColor: colors.neutral['50'], borderRadius: '8px' }}>
                  <div style={{ ...typography.body, fontWeight: 600 }}>No alerts available</div>
                </div>
              ) : (
                alerts.map((alert) => {
                  const isCritical = alert.severity === 'critical' || alert.severity === 'emergency';
                  const bg = isCritical ? colors.critical.background : colors.warning.background;
                  const text = isCritical ? colors.critical.text : colors.warning.text;
                  return (
                    <div
                      key={alert.alert_id}
                      style={{ padding: '12px', backgroundColor: bg, borderRadius: '8px' }}
                    >
                      <div style={{ ...typography.body, color: text, fontWeight: 600 }}>
                        ● {alert.severity.toUpperCase()}: {alert.title || alert.alert_type.replaceAll('_', ' ')}
                      </div>
                      <div style={{ ...typography.caption, color: text, marginTop: '4px' }}>
                        {formatTimeAgo(alert.created_at)}
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </div>

          {/* Session History */}
          <div
            style={{
              backgroundColor: colors.neutral.white,
              border: `1px solid ${colors.neutral['300']}`,
              borderRadius: '12px',
              padding: '24px',
              boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
            }}
          >
            <h3 style={{ ...typography.sectionTitle, marginBottom: '16px' }}>Session History</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {activities.length === 0 ? (
                <div style={{ padding: '12px', backgroundColor: colors.neutral['50'], borderRadius: '8px' }}>
                  <div style={{ ...typography.body, fontWeight: 600 }}>No sessions yet</div>
                </div>
              ) : (
                activities.map((session) => (
                  <div
                    key={session.session_id}
                    style={{ padding: '12px', backgroundColor: colors.neutral['50'], borderRadius: '8px' }}
                  >
                    <div style={{ ...typography.body, fontWeight: 600 }}>
                      {new Date(session.start_time).toLocaleDateString()}: {session.duration_minutes ?? '--'}-min{' '}
                      {session.activity_type.replaceAll('_', ' ')}
                    </div>
                    <div style={{ ...typography.caption, color: colors.neutral['500'], marginTop: '4px' }}>
                      Avg HR: {session.avg_heart_rate ?? '--'} BPM • Recovery: {session.recovery_time_minutes ?? '--'} min
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        {/* AI Risk Assessment */}
        <div
          style={{
            backgroundColor: colors.critical.background,
            border: `1px solid ${colors.critical.border}`,
            borderRadius: '12px',
            padding: '24px',
            boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
            <AlertTriangle size={20} color={colors.critical.text} />
            <h3 style={{ ...typography.sectionTitle, color: colors.critical.text, margin: 0 }}>
              AI Risk Assessment
            </h3>
          </div>

          <div style={{ marginBottom: '16px' }}>
            <div style={{ ...typography.body, color: colors.critical.text, marginBottom: '8px' }}>
              <strong>
                Current Risk: {riskAssessment?.risk_level?.toUpperCase()} ({(riskAssessment?.risk_score || 0).toFixed(2)})
              </strong>
            </div>
          </div>

          <div style={{ marginBottom: '16px' }}>
            <div style={{ ...typography.body, color: colors.critical.text, fontWeight: 600, marginBottom: '8px' }}>
              Contributing Factors:
            </div>
            <ul style={{ margin: 0, paddingLeft: '20px' }}>
              {riskFactors.length === 0 ? (
                <li style={{ ...typography.body, color: colors.critical.text, marginBottom: '4px' }}>
                  No contributing factors available.
                </li>
              ) : (
                riskFactors.map((factor, idx) => (
                  <li key={idx} style={{ ...typography.body, color: colors.critical.text, marginBottom: '4px' }}>
                    {factor}
                  </li>
                ))
              )}
            </ul>
          </div>

          <div style={{ paddingTop: '16px', borderTop: `1px solid ${colors.critical.border}` }}>
            <div style={{ ...typography.body, color: colors.critical.text, fontWeight: 600 }}>
              Recommendation:
            </div>
            <div style={{ ...typography.body, color: colors.critical.text, marginTop: '8px' }}>
              {recommendation?.description || recommendation?.warnings || 'No recommendation available.'}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default PatientDetailPage;
