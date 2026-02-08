-- =============================================================================
-- ADAPTIV HEALTH - RBAC & Consent Management Migration
-- =============================================================================
-- Migration for: copilot/implement-user-roles-access branch
-- Date: February 8, 2026
-- Description: Adds role-based access control, consent management, and 
--              security enhancements to users table
-- =============================================================================

-- Add role and status columns
ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(20) DEFAULT 'patient';
ALTER TABLE users ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;
ALTER TABLE users ADD COLUMN IF NOT EXISTS is_verified BOOLEAN DEFAULT FALSE;

-- Add medical data columns (encrypted storage)
ALTER TABLE users ADD COLUMN IF NOT EXISTS medical_history_encrypted TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS emergency_contact_name VARCHAR(255);
ALTER TABLE users ADD COLUMN IF NOT EXISTS emergency_contact_phone VARCHAR(20);

-- Add consent/sharing state machine columns
ALTER TABLE users ADD COLUMN IF NOT EXISTS share_state VARCHAR(30) DEFAULT 'SHARING_ON';
ALTER TABLE users ADD COLUMN IF NOT EXISTS share_requested_at TIMESTAMP;
ALTER TABLE users ADD COLUMN IF NOT EXISTS share_requested_by INTEGER;
ALTER TABLE users ADD COLUMN IF NOT EXISTS share_reviewed_at TIMESTAMP;
ALTER TABLE users ADD COLUMN IF NOT EXISTS share_reviewed_by INTEGER;
ALTER TABLE users ADD COLUMN IF NOT EXISTS share_decision VARCHAR(20);
ALTER TABLE users ADD COLUMN IF NOT EXISTS share_reason VARCHAR(500);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_user_email_active ON users(email, is_active);
CREATE INDEX IF NOT EXISTS idx_user_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_user_share_state ON users(share_state);

-- Set defaults for existing users
UPDATE users SET role = 'patient' WHERE role IS NULL;
UPDATE users SET is_active = TRUE WHERE is_active IS NULL;
UPDATE users SET is_verified = FALSE WHERE is_verified IS NULL;
UPDATE users SET share_state = 'SHARING_ON' WHERE share_state IS NULL;

-- Verify migration
SELECT 
    COUNT(*) as total_users,
    SUM(CASE WHEN role IS NULL THEN 1 ELSE 0 END) as null_roles,
    SUM(CASE WHEN share_state IS NULL THEN 1 ELSE 0 END) as null_share_state
FROM users;

-- Show role distribution
SELECT role, COUNT(*) as count
FROM users
GROUP BY role
ORDER BY count DESC;
