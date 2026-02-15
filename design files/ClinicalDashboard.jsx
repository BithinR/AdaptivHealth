import React, { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Heart, AlertTriangle, CheckCircle, AlertCircle, Search, Filter, Clock, TrendingUp } from 'lucide-react';

// commentline: Define color constants that match Adaptiv Health design system
const COLORS = {
  primary: '#0DB9A6',
  primaryHover: '#0A9B8A',
  primaryDark: '#076659',
  success: '#10B981',
  warning: '#F59E0B',
  danger: '#EF4444',
  critical: '#7F1D1D',
  bgPrimary: '#F8FAFB',
  bgSecondary: '#FFFFFF',
  textPrimary: '#1A1F2A',
  textSecondary: '#8C96A0',
  border: '#E6EAED',
};

// commentline: Mock patient data for demonstration (replace with real API data)
const mockPatientData = [
  { id: 1, name: 'Robert Anderson', age: 68, status: 'critical', healthScore: 45, lastReading: '8 min ago', hrTrend: [72, 75, 78, 82, 88, 92, 95, 98] },
  { id: 2, name: 'Sarah Mitchell', age: 54, status: 'warning', healthScore: 72, lastReading: '18 min ago', hrTrend: [68, 70, 72, 75, 78, 80, 82, 85] },
  { id: 3, name: 'James Thompson', age: 61, status: 'stable', healthScore: 85, lastReading: '13 min ago', hrTrend: [65, 66, 67, 68, 69, 70, 71, 72] },
  { id: 4, name: 'Maria Garcia', age: 59, status: 'stable', healthScore: 88, lastReading: '11 min ago', hrTrend: [62, 63, 64, 65, 66, 67, 68, 69] },
  { id: 5, name: 'David Lee', age: 72, status: 'warning', healthScore: 65, lastReading: '23 min ago', hrTrend: [75, 76, 78, 80, 82, 84, 86, 88] },
];

// commentline: Mock alert data for dashboard
const mockAlerts = [
  { id: 1, patient: 'Robert Anderson', severity: 'critical', title: 'Low SpO2', message: 'SpO2 dropped to 89%', time: '14 min ago' },
  { id: 2, patient: 'Sarah Mitchell', severity: 'warning', title: 'Elevated BP', message: 'Blood pressure 142/86', time: '34 min ago' },
  { id: 3, patient: 'James Thompson', severity: 'active', title: 'Irregular HR', message: 'Heart rate variability detected', time: '9 min ago' },
];

// commentline: Mock trend data for system analytics
const mockTrendData = [
  { day: 'Sun', avgHR: 72, alerts: 1, critical: 0 },
  { day: 'Mon', avgHR: 74, alerts: 4, critical: 1 },
  { day: 'Tue', avgHR: 71, alerts: 1, critical: 0 },
  { day: 'Wed', avgHR: 75, alerts: 4, critical: 2 },
  { day: 'Thu', avgHR: 73, alerts: 2, critical: 0 },
  { day: 'Fri', avgHR: 76, alerts: 4, critical: 1 },
  { day: 'Sat', avgHR: 70, alerts: 3, critical: 1 },
];

// commentline: Status badge component - displays color-coded patient status
const StatusBadge = ({ status }) => {
  const statusStyles = {
    critical: { bg: '#FEE2E2', text: '#7F1D1D', label: 'Critical' },
    warning: { bg: '#FEF3C7', text: '#92400E', label: 'Warning' },
    active: { bg: '#DBEAFE', text: '#1E40AF', label: 'Active' },
    stable: { bg: '#DCFCE7', text: '#166534', label: 'Stable' },
  };

  const style = statusStyles[status] || statusStyles.stable;

  return (
    <span
      style={{
        display: 'inline-block',
        backgroundColor: style.bg,
        color: style.text,
        padding: '4px 12px',
        borderRadius: '20px',
        fontSize: '12px',
        fontWeight: '600',
      }}
    >
      {style.label}
    </span>
  );
};

// commentline: Header component - shows system overview and critical alerts banner
const Header = () => {
  const criticalCount = mockAlerts.filter(a => a.severity === 'critical').length;

  return (
    <div style={{ padding: '24px 32px', borderBottom: `1px solid ${COLORS.border}`, backgroundColor: COLORS.bgSecondary }}>
      <div style={{ maxWidth: '1400px', margin: '0 auto' }}>
        {/* commentline: Brand and title section */}
        <div style={{ marginBottom: '24px' }}>
          <h1 style={{ fontSize: '28px', fontWeight: '700', color: COLORS.textPrimary, margin: '0 0 8px 0', fontFamily: 'Poppins, system-ui' }}>
            Adaptiv Health
          </h1>
          <p style={{ fontSize: '14px', color: COLORS.textSecondary, margin: '0', fontFamily: 'Inter, system-ui' }}>
            Care Dashboard
          </p>
        </div>

        {/* commentline: Critical alert banner - draws immediate attention */}
        {criticalCount > 0 && (
          <div
            style={{
              backgroundColor: '#FEE2E2',
              border: '1px solid #FCA5A5',
              borderLeft: '4px solid #DC2626',
              borderRadius: '8px',
              padding: '12px 16px',
              marginBottom: '16px',
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              animation: 'pulse 2s infinite',
            }}
          >
            <AlertTriangle size={20} style={{ color: '#DC2626', flexShrink: 0 }} />
            <span style={{ color: '#7F1D1D', fontSize: '14px', fontWeight: '600' }}>
              {criticalCount} critical alert{criticalCount > 1 ? 's' : ''} require immediate attention
            </span>
          </div>
        )}
      </div>
    </div>
  );
};

// commentline: Overview metrics section - shows key system statistics
const OverviewMetrics = () => {
  const metrics = [
    { label: 'Total Patients', value: '8', icon: Heart, color: COLORS.primary },
    { label: 'Patients Stable', value: '5', icon: CheckCircle, color: COLORS.success },
    { label: 'Require Attention', value: '3', icon: AlertCircle, color: COLORS.warning },
    { label: 'Critical Alerts', value: '2', icon: AlertTriangle, color: COLORS.danger },
  ];

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginBottom: '32px' }}>
      {/* commentline: Render each metric as a card with icon and value */}
      {metrics.map((metric, idx) => {
        const Icon = metric.icon;
        return (
          <div
            key={idx}
            style={{
              backgroundColor: COLORS.bgSecondary,
              border: `1px solid ${COLORS.border}`,
              borderRadius: '12px',
              padding: '20px',
              boxShadow: '0 1px 3px rgba(0, 0, 0, 0.08)',
              transition: 'all 300ms ease',
              cursor: 'pointer',
              _hover: { boxShadow: '0 4px 12px rgba(0, 0, 0, 0.12)' },
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.12)';
              e.currentTarget.style.borderColor = metric.color;
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.08)';
              e.currentTarget.style.borderColor = COLORS.border;
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '12px' }}>
              <Icon size={20} style={{ color: metric.color }} />
              <span style={{ fontSize: '12px', color: COLORS.textSecondary, fontFamily: 'Inter, system-ui' }}>
                {metric.label}
              </span>
            </div>
            <div style={{ fontSize: '36px', fontWeight: '700', color: metric.color, fontFamily: 'IBM Plex Mono, monospace' }}>
              {metric.value}
            </div>
          </div>
        );
      })}
    </div>
  );
};

// commentline: Patient list table component - sortable, searchable patient data
const PatientList = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('lastReading');

  // commentline: Filter patients by search term
  const filteredPatients = mockPatientData.filter(p =>
    p.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // commentline: Sort patients by selected criteria
  const sortedPatients = [...filteredPatients].sort((a, b) => {
    if (sortBy === 'healthScore') return b.healthScore - a.healthScore;
    if (sortBy === 'name') return a.name.localeCompare(b.name);
    return 0;
  });

  return (
    <div style={{ marginBottom: '32px' }}>
      <h2 style={{ fontSize: '22px', fontWeight: '600', color: COLORS.textPrimary, margin: '0 0 16px 0', fontFamily: 'Poppins, system-ui' }}>
        Patient Management
      </h2>

      {/* commentline: Search and filter controls */}
      <div style={{ display: 'flex', gap: '12px', marginBottom: '16px' }}>
        <div style={{ flex: 1, position: 'relative' }}>
          <Search size={16} style={{ position: 'absolute', left: '12px', top: '14px', color: COLORS.textSecondary }} />
          <input
            type="text"
            placeholder="Search patients by name..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{
              width: '100%',
              paddingLeft: '40px',
              paddingRight: '12px',
              padding: '12px 12px 12px 40px',
              border: `1px solid ${COLORS.border}`,
              borderRadius: '8px',
              fontSize: '14px',
              fontFamily: 'Inter, system-ui',
              outline: 'none',
              transition: 'border-color 200ms ease',
            }}
            onFocus={(e) => (e.target.style.borderColor = COLORS.primary)}
            onBlur={(e) => (e.target.style.borderColor = COLORS.border)}
          />
        </div>

        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          style={{
            padding: '12px 16px',
            border: `1px solid ${COLORS.border}`,
            borderRadius: '8px',
            fontSize: '14px',
            fontFamily: 'Inter, system-ui',
            backgroundColor: COLORS.bgSecondary,
            color: COLORS.textPrimary,
            cursor: 'pointer',
            outline: 'none',
          }}
        >
          <option value="lastReading">Sort by: Last Reading</option>
          <option value="healthScore">Sort by: Health Score</option>
          <option value="name">Sort by: Name</option>
        </select>
      </div>

      {/* commentline: Patient table with responsive layout */}
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ backgroundColor: COLORS.bgPrimary, borderBottom: `1px solid ${COLORS.border}` }}>
              <th style={{ padding: '12px', textAlign: 'left', fontSize: '12px', fontWeight: '600', color: COLORS.textSecondary, fontFamily: 'Inter, system-ui' }}>
                Patient Name
              </th>
              <th style={{ padding: '12px', textAlign: 'center', fontSize: '12px', fontWeight: '600', color: COLORS.textSecondary, fontFamily: 'Inter, system-ui' }}>
                Age
              </th>
              <th style={{ padding: '12px', textAlign: 'center', fontSize: '12px', fontWeight: '600', color: COLORS.textSecondary, fontFamily: 'Inter, system-ui' }}>
                Health Score
              </th>
              <th style={{ padding: '12px', textAlign: 'center', fontSize: '12px', fontWeight: '600', color: COLORS.textSecondary, fontFamily: 'Inter, system-ui' }}>
                Status
              </th>
              <th style={{ padding: '12px', textAlign: 'center', fontSize: '12px', fontWeight: '600', color: COLORS.textSecondary, fontFamily: 'Inter, system-ui' }}>
                Last Reading
              </th>
              <th style={{ padding: '12px', textAlign: 'center', fontSize: '12px', fontWeight: '600', color: COLORS.textSecondary, fontFamily: 'Inter, system-ui' }}>
                Action
              </th>
            </tr>
          </thead>
          <tbody>
            {/* commentline: Render patient row for each patient in sorted list */}
            {sortedPatients.map((patient) => (
              <tr
                key={patient.id}
                style={{
                  borderBottom: `1px solid ${COLORS.border}`,
                  transition: 'background-color 200ms ease',
                  cursor: 'pointer',
                }}
                onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = COLORS.bgPrimary)}
                onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = 'transparent')}
              >
                <td style={{ padding: '12px', fontSize: '14px', color: COLORS.textPrimary, fontFamily: 'Inter, system-ui' }}>
                  {patient.name}
                </td>
                <td style={{ padding: '12px', textAlign: 'center', fontSize: '14px', color: COLORS.textPrimary, fontFamily: 'Inter, system-ui' }}>
                  {patient.age}
                </td>
                <td style={{ padding: '12px', textAlign: 'center', fontFamily: 'IBM Plex Mono, monospace' }}>
                  <span
                    style={{
                      display: 'inline-block',
                      fontSize: '14px',
                      fontWeight: '700',
                      color: patient.healthScore >= 80 ? COLORS.success : patient.healthScore >= 60 ? COLORS.warning : COLORS.danger,
                    }}
                  >
                    {patient.healthScore}/100
                  </span>
                </td>
                <td style={{ padding: '12px', textAlign: 'center' }}>
                  <StatusBadge status={patient.status} />
                </td>
                <td style={{ padding: '12px', textAlign: 'center', fontSize: '12px', color: COLORS.textSecondary, fontFamily: 'Inter, system-ui' }}>
                  {patient.lastReading}
                </td>
                <td style={{ padding: '12px', textAlign: 'center' }}>
                  <button
                    style={{
                      padding: '6px 16px',
                      backgroundColor: 'transparent',
                      color: COLORS.primary,
                      border: `1px solid ${COLORS.primary}`,
                      borderRadius: '6px',
                      fontSize: '12px',
                      fontWeight: '600',
                      cursor: 'pointer',
                      transition: 'all 200ms ease',
                      fontFamily: 'Inter, system-ui',
                    }}
                    onMouseEnter={(e) => {
                      e.target.style.backgroundColor = COLORS.primary;
                      e.target.style.color = '#FFFFFF';
                    }}
                    onMouseLeave={(e) => {
                      e.target.style.backgroundColor = 'transparent';
                      e.target.style.color = COLORS.primary;
                    }}
                  >
                    View
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

// commentline: Analytics charts component - displays HR trends and alert patterns
const AnalyticsCharts = () => {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '24px' }}>
      {/* commentline: Heart rate trend chart - shows average HR over 7 days */}
      <div style={{ backgroundColor: COLORS.bgSecondary, border: `1px solid ${COLORS.border}`, borderRadius: '12px', padding: '20px' }}>
        <h3 style={{ fontSize: '16px', fontWeight: '600', color: COLORS.textPrimary, margin: '0 0 16px 0', fontFamily: 'Poppins, system-ui' }}>
          Average Heart Rate Trend (Population)
        </h3>
        <ResponsiveContainer width="100%" height={280}>
          <LineChart data={mockTrendData}>
            <CartesianGrid strokeDasharray="3 3" stroke={COLORS.border} />
            <XAxis dataKey="day" stroke={COLORS.textSecondary} />
            <YAxis stroke={COLORS.textSecondary} />
            <Tooltip
              contentStyle={{
                backgroundColor: COLORS.bgSecondary,
                border: `1px solid ${COLORS.border}`,
                borderRadius: '8px',
              }}
            />
            <Legend />
            <Line type="monotone" dataKey="avgHR" stroke={COLORS.primary} strokeWidth={2} dot={{ fill: COLORS.primary }} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* commentline: Alerts over time chart - shows alert frequency and severity */}
      <div style={{ backgroundColor: COLORS.bgSecondary, border: `1px solid ${COLORS.border}`, borderRadius: '12px', padding: '20px' }}>
        <h3 style={{ fontSize: '16px', fontWeight: '600', color: COLORS.textPrimary, margin: '0 0 16px 0', fontFamily: 'Poppins, system-ui' }}>
          Alerts Over Time (Last 7 Days)
        </h3>
        <ResponsiveContainer width="100%" height={280}>
          <BarChart data={mockTrendData}>
            <CartesianGrid strokeDasharray="3 3" stroke={COLORS.border} />
            <XAxis dataKey="day" stroke={COLORS.textSecondary} />
            <YAxis stroke={COLORS.textSecondary} />
            <Tooltip
              contentStyle={{
                backgroundColor: COLORS.bgSecondary,
                border: `1px solid ${COLORS.border}`,
                borderRadius: '8px',
              }}
            />
            <Legend />
            <Bar dataKey="alerts" fill={COLORS.warning} radius={[8, 8, 0, 0]} />
            <Bar dataKey="critical" fill={COLORS.danger} radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

// commentline: Alerts management section - displays and manages clinical alerts
const AlertsSection = () => {
  const [expandedAlert, setExpandedAlert] = useState(null);

  // commentline: Group alerts by severity for better organization
  const groupedAlerts = {
    critical: mockAlerts.filter(a => a.severity === 'critical'),
    warning: mockAlerts.filter(a => a.severity === 'warning'),
    active: mockAlerts.filter(a => a.severity === 'active'),
  };

  const AlertCard = ({ alert, severity }) => {
    const severityStyles = {
      critical: { bg: '#FEE2E2', border: '#FCA5A5', icon: AlertTriangle },
      warning: { bg: '#FEF3C7', border: '#FCD34D', icon: AlertCircle },
      active: { bg: '#DBEAFE', border: '#93C5FD', icon: Clock },
    };

    const style = severityStyles[severity];
    const IconComponent = style.icon;

    return (
      <div
        style={{
          backgroundColor: style.bg,
          border: `1px solid ${style.border}`,
          borderRadius: '8px',
          padding: '16px',
          marginBottom: '12px',
          cursor: 'pointer',
          transition: 'all 200ms ease',
        }}
        onClick={() => setExpandedAlert(expandedAlert === alert.id ? null : alert.id)}
        onMouseEnter={(e) => (e.currentTarget.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.1)')}
        onMouseLeave={(e) => (e.currentTarget.style.boxShadow = 'none')}
      >
        <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
          <IconComponent size={20} style={{ marginTop: '2px', flexShrink: 0 }} />
          <div style={{ flex: 1 }}>
            <h4 style={{ fontSize: '14px', fontWeight: '600', margin: '0 0 4px 0', color: COLORS.textPrimary, fontFamily: 'Poppins, system-ui' }}>
              {alert.title}
            </h4>
            <p style={{ fontSize: '13px', color: COLORS.textSecondary, margin: '0 0 4px 0', fontFamily: 'Inter, system-ui' }}>
              {alert.message}
            </p>
            <p style={{ fontSize: '12px', color: COLORS.textSecondary, margin: '0', fontFamily: 'Inter, system-ui' }}>
              Patient: {alert.patient} • {alert.time}
            </p>
          </div>
        </div>

        {/* commentline: Expandable action buttons for alert management */}
        {expandedAlert === alert.id && (
          <div style={{ marginTop: '12px', paddingTop: '12px', borderTop: `1px solid ${style.border}`, display: 'flex', gap: '8px' }}>
            <button
              style={{
                flex: 1,
                padding: '8px 12px',
                backgroundColor: COLORS.primary,
                color: '#FFFFFF',
                border: 'none',
                borderRadius: '6px',
                fontSize: '12px',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'background-color 200ms ease',
                fontFamily: 'Inter, system-ui',
              }}
              onMouseEnter={(e) => (e.target.style.backgroundColor = COLORS.primaryHover)}
              onMouseLeave={(e) => (e.target.style.backgroundColor = COLORS.primary)}
            >
              View Patient
            </button>
            <button
              style={{
                flex: 1,
                padding: '8px 12px',
                backgroundColor: COLORS.success,
                color: '#FFFFFF',
                border: 'none',
                borderRadius: '6px',
                fontSize: '12px',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'background-color 200ms ease',
                fontFamily: 'Inter, system-ui',
              }}
              onMouseEnter={(e) => (e.target.style.backgroundColor = '#059669')}
              onMouseLeave={(e) => (e.target.style.backgroundColor = COLORS.success)}
            >
              Acknowledge
            </button>
          </div>
        )}
      </div>
    );
  };

  return (
    <div style={{ marginBottom: '32px' }}>
      <h2 style={{ fontSize: '22px', fontWeight: '600', color: COLORS.textPrimary, margin: '0 0 16px 0', fontFamily: 'Poppins, system-ui' }}>
        Alerts & Warnings
      </h2>
      <p style={{ fontSize: '14px', color: COLORS.textSecondary, margin: '0 0 16px 0', fontFamily: 'Inter, system-ui' }}>
        Risk management and clinical escalation
      </p>

      {/* commentline: Render critical alerts section */}
      {groupedAlerts.critical.length > 0 && (
        <div style={{ marginBottom: '24px' }}>
          <h3 style={{ fontSize: '14px', fontWeight: '600', color: COLORS.danger, margin: '0 0 12px 0', fontFamily: 'Poppins, system-ui' }}>
            🚨 Critical Alerts ({groupedAlerts.critical.length})
          </h3>
          {groupedAlerts.critical.map(alert => (
            <AlertCard key={alert.id} alert={alert} severity="critical" />
          ))}
        </div>
      )}

      {/* commentline: Render warning alerts section */}
      {groupedAlerts.warning.length > 0 && (
        <div style={{ marginBottom: '24px' }}>
          <h3 style={{ fontSize: '14px', fontWeight: '600', color: COLORS.warning, margin: '0 0 12px 0', fontFamily: 'Poppins, system-ui' }}>
            ⚠️ Warning Alerts ({groupedAlerts.warning.length})
          </h3>
          {groupedAlerts.warning.map(alert => (
            <AlertCard key={alert.id} alert={alert} severity="warning" />
          ))}
        </div>
      )}

      {/* commentline: Render active alerts section */}
      {groupedAlerts.active.length > 0 && (
        <div>
          <h3 style={{ fontSize: '14px', fontWeight: '600', color: COLORS.textSecondary, margin: '0 0 12px 0', fontFamily: 'Poppins, system-ui' }}>
            ℹ️ Active Alerts ({groupedAlerts.active.length})
          </h3>
          {groupedAlerts.active.map(alert => (
            <AlertCard key={alert.id} alert={alert} severity="active" />
          ))}
        </div>
      )}
    </div>
  );
};

// commentline: Main dashboard component - orchestrates all sections
export default function ClinicianDashboard() {
  return (
    <div style={{ backgroundColor: COLORS.bgPrimary, minHeight: '100vh', fontFamily: 'Inter, system-ui' }}>
      <Header />

      <main style={{ padding: '32px', maxWidth: '1400px', margin: '0 auto' }}>
        <OverviewMetrics />
        <AlertsSection />
        <PatientList />
        <AnalyticsCharts />
      </main>

      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700&family=Inter:wght@400;500;600&display=swap');
        
        body {
          margin: 0;
          padding: 0;
          background-color: ${COLORS.bgPrimary};
        }

        @keyframes pulse {
          0%, 100% {
            opacity: 1;
          }
          50% {
            opacity: 0.8;
          }
        }

        button:active {
          transform: scale(0.98);
        }

        input::-webkit-outer-spin-button,
        input::-webkit-inner-spin-button {
          -webkit-appearance: none;
          margin: 0;
        }

        select option {
          background-color: ${COLORS.bgSecondary};
          color: ${COLORS.textPrimary};
        }
      `}</style>
    </div>
  );
}
