/*
Patients list page.

Shows all patients being monitored. Displays their latest vital signs
and risk level. Clinicians can search for a patient or filter by risk level.
Click on a patient to see detailed information.
*/

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Search } from 'lucide-react';
import { colors } from '../theme/colors';
import { typography } from '../theme/typography';
import StatusBadge, { riskToStatus } from '../components/common/StatusBadge';

interface Patient {
  id: number;
  name: string;
  age: number;
  gender: string;
  riskLevel: 'low' | 'moderate' | 'high';
  lastReading: string;
  heartRate: number;
  device: string;
}

// Mock patient data
const MOCK_PATIENTS: Patient[] = [
  {
    id: 1,
    name: 'Robert Anderson',
    age: 68,
    gender: 'Male',
    riskLevel: 'high',
    lastReading: '8 min ago',
    heartRate: 112,
    device: 'Fitbit Charge 6',
  },
  {
    id: 2,
    name: 'Sarah Mitchell',
    age: 55,
    gender: 'Female',
    riskLevel: 'moderate',
    lastReading: '34 min ago',
    heartRate: 94,
    device: 'Apple Watch',
  },
  {
    id: 3,
    name: 'James Thompson',
    age: 72,
    gender: 'Male',
    riskLevel: 'low',
    lastReading: '1 hour ago',
    heartRate: 68,
    device: 'Withings Watch',
  },
  {
    id: 4,
    name: 'Emily Rodriguez',
    age: 61,
    gender: 'Female',
    riskLevel: 'moderate',
    lastReading: '2 hours ago',
    heartRate: 88,
    device: 'Fitbit Versa 4',
  },
  {
    id: 5,
    name: 'Michael Chen',
    age: 59,
    gender: 'Male',
    riskLevel: 'low',
    lastReading: '3 hours ago',
    heartRate: 72,
    device: 'Garmin Epix',
  },
];

const PatientsPage: React.FC = () => {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [filterRisk, setFilterRisk] = useState<'all' | 'low' | 'moderate' | 'high'>('all');

  const filteredPatients = MOCK_PATIENTS.filter((patient) => {
    const matchesSearch =
      patient.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      patient.id.toString().includes(searchTerm);
    const matchesFilter = filterRisk === 'all' || patient.riskLevel === filterRisk;
    return matchesSearch && matchesFilter;
  });

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
            onClick={() => navigate('/dashboard')}
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
            Back to Dashboard
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main style={{ maxWidth: '1440px', margin: '0 auto', padding: '32px' }}>
        <h1 style={typography.pageTitle}>Patient Management</h1>
        <p style={{ ...typography.body, color: colors.neutral['500'], marginBottom: '32px' }}>
          Monitor and manage all patients in your care team
        </p>

        {/* Filters Section */}
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
          {/* Search Bar */}
          <div style={{ marginBottom: '20px' }}>
            <label style={{ ...typography.body, fontWeight: 600, display: 'block', marginBottom: '8px' }}>
              Search Patients
            </label>
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                padding: '12px 16px',
                borderRadius: '8px',
                border: `1px solid ${colors.neutral['300']}`,
                backgroundColor: colors.neutral.white,
              }}
            >
              <Search size={20} color={colors.neutral['500']} />
              <input
                type="text"
                placeholder="Search by name or ID..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                style={{
                  flex: 1,
                  border: 'none',
                  outline: 'none',
                  fontSize: '14px',
                  fontFamily: 'inherit',
                }}
              />
            </div>
          </div>

          {/* Risk Filter */}
          <div>
            <label style={{ ...typography.body, fontWeight: 600, display: 'block', marginBottom: '8px' }}>
              Filter by Risk Level
            </label>
            <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
              {['all', 'low', 'moderate', 'high'].map((level) => (
                <button
                  key={level}
                  onClick={() => setFilterRisk(level as any)}
                  style={{
                    padding: '8px 16px',
                    borderRadius: '6px',
                    border: 'none',
                    backgroundColor:
                      filterRisk === level ? colors.primary.default : colors.neutral['100'],
                    color: filterRisk === level ? colors.neutral.white : colors.neutral['700'],
                    cursor: 'pointer',
                    fontWeight: 500,
                    textTransform: 'capitalize',
                    transition: 'all 0.2s',
                  }}
                >
                  {level === 'all' ? 'All Patients' : level.charAt(0).toUpperCase() + level.slice(1)}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Patient List Table */}
        <div
          style={{
            backgroundColor: colors.neutral.white,
            border: `1px solid ${colors.neutral['300']}`,
            borderRadius: '12px',
            overflow: 'hidden',
            boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
          }}
        >
          {/* Table Header */}
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: '200px 100px 100px 120px 100px 150px 80px',
              gap: '16px',
              padding: '16px 24px',
              backgroundColor: colors.neutral['50'],
              borderBottom: `1px solid ${colors.neutral['300']}`,
              fontWeight: 600,
              color: colors.neutral['700'],
              fontSize: '12px',
              textTransform: 'uppercase',
              letterSpacing: '0.05em',
            }}
          >
            <div>Patient Name</div>
            <div>Age</div>
            <div>Gender</div>
            <div>Risk Level</div>
            <div>Heart Rate</div>
            <div>Last Reading</div>
            <div>Action</div>
          </div>

          {/* Table Rows */}
          {filteredPatients.length > 0 ? (
            filteredPatients.map((patient, idx) => (
              <div
                key={patient.id}
                style={{
                  display: 'grid',
                  gridTemplateColumns: '200px 100px 100px 120px 100px 150px 80px',
                  gap: '16px',
                  padding: '16px 24px',
                  borderBottom: idx < filteredPatients.length - 1 ? `1px solid ${colors.neutral['300']}` : 'none',
                  backgroundColor: idx % 2 === 0 ? colors.neutral.white : colors.neutral['50'],
                  alignItems: 'center',
                }}
              >
                <div>
                  <div style={{ ...typography.body, fontWeight: 600 }}>{patient.name}</div>
                </div>
                <div style={typography.body}>{patient.age}</div>
                <div style={typography.body}>{patient.gender}</div>
                <div>
                  <StatusBadge status={riskToStatus(patient.riskLevel)} size="sm" />
                </div>
                <div style={{ ...typography.body, fontWeight: 600 }}>
                  {patient.heartRate} <span style={{ ...typography.caption, fontWeight: 400 }}>BPM</span>
                </div>
                <div style={typography.caption}>{patient.lastReading}</div>
                <button
                  onClick={() => navigate(`/patients/${patient.id}`)}
                  style={{
                    padding: '6px 12px',
                    borderRadius: '6px',
                    border: 'none',
                    backgroundColor: colors.primary.default,
                    color: colors.neutral.white,
                    cursor: 'pointer',
                    fontWeight: 500,
                    fontSize: '12px',
                    transition: 'all 0.2s',
                  }}
                  onMouseEnter={(e) => {
                    (e.currentTarget as HTMLButtonElement).style.backgroundColor = colors.primary.dark;
                  }}
                  onMouseLeave={(e) => {
                    (e.currentTarget as HTMLButtonElement).style.backgroundColor = colors.primary.default;
                  }}
                >
                  View
                </button>
              </div>
            ))
          ) : (
            <div
              style={{
                padding: '40px 24px',
                textAlign: 'center',
                color: colors.neutral['500'],
              }}
            >
              <p style={typography.body}>No patients found matching your criteria.</p>
            </div>
          )}
        </div>

        {/* Summary */}
        <div style={{ marginTop: '32px', display: 'flex', justifyContent: 'space-between' }}>
          <p style={typography.caption}>
            Showing {filteredPatients.length} of {MOCK_PATIENTS.length} patients
          </p>
          <p style={typography.caption}>Total Active Patients: {MOCK_PATIENTS.length}</p>
        </div>
      </main>
    </div>
  );
};

export default PatientsPage;
