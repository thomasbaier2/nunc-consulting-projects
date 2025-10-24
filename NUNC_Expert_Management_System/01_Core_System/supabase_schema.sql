-- NUNC Expert Management System - Boutique Architecture Schema
-- Erstellt das komplette Supabase Schema für persönliche Kandidaten-Verwaltung

-- =============================================================================
-- PROFILES TABLE - Haupttabelle für Kandidaten (max. 100)
-- =============================================================================
CREATE TABLE IF NOT EXISTS profiles (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Grunddaten
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(50),
    location VARCHAR(255),
    
    -- Boutique-spezifische Felder
    boutique_status VARCHAR(20) DEFAULT 'candidate' CHECK (boutique_status IN ('candidate', 'active', 'trusted', 'archived')),
    trust_level INTEGER DEFAULT 1 CHECK (trust_level BETWEEN 1 AND 5), -- 1=new, 5=trusted
    personal_notes TEXT, -- Persönliche Notizen über den Kandidaten
    relationship_quality VARCHAR(20) DEFAULT 'new' CHECK (relationship_quality IN ('new', 'good', 'excellent', 'partnership')),
    
    -- Verfügbarkeit
    availability_status VARCHAR(20) DEFAULT 'unknown' CHECK (availability_status IN ('unknown', 'available', 'busy', 'unavailable')),
    next_available_date DATE,
    preferred_hours_per_week INTEGER,
    remote_preference VARCHAR(20) DEFAULT 'flexible' CHECK (remote_preference IN ('remote', 'onsite', 'hybrid', 'flexible')),
    
    -- Skills und Erfahrung
    technical_skills TEXT[], -- Array von technischen Skills
    soft_skills TEXT[], -- Array von Soft Skills
    certifications TEXT[], -- Array von Zertifizierungen
    languages TEXT[], -- Array von Sprachen
    
    -- Projekt-Erfahrung (für Cross-connections)
    company_experience JSONB, -- {"BMW": "2 years", "SAP": "1 year"}
    project_experience JSONB, -- {"ERP": "3 years", "Cloud": "2 years"}
    industry_experience TEXT[], -- ["Automotive", "Finance", "Healthcare"]
    
    -- AI-basierte Bewertung
    reliability_score DECIMAL(3,2) DEFAULT 0.0 CHECK (reliability_score BETWEEN 0.0 AND 1.0),
    experience_score DECIMAL(3,2) DEFAULT 0.0 CHECK (experience_score BETWEEN 0.0 AND 1.0),
    quality_score DECIMAL(3,2) DEFAULT 0.0 CHECK (quality_score BETWEEN 0.0 AND 1.0),
    
    -- Metadaten
    source VARCHAR(50) DEFAULT 'manual' CHECK (source IN ('manual', 'linkedin', 'freelancermap', 'salesforce', 'cv_upload')),
    external_id VARCHAR(255), -- ID aus externem System
    last_contact_date DATE,
    total_contact_count INTEGER DEFAULT 0,
    
    -- Volltext-Suche (wird per Trigger aktualisiert)
    search_vector tsvector
);

-- =============================================================================
-- RELATIONSHIPS TABLE - Persönliche Beziehungen
-- =============================================================================
CREATE TABLE IF NOT EXISTS relationships (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    profile_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    
    -- Beziehungs-Status
    relationship_type VARCHAR(20) DEFAULT 'professional' CHECK (relationship_type IN ('professional', 'personal', 'partnership', 'mentor')),
    relationship_strength INTEGER DEFAULT 1 CHECK (relationship_strength BETWEEN 1 AND 5),
    
    -- Persönliche Notizen
    personal_notes TEXT, -- "Sehr zuverlässig, arbeitet gerne remote"
    personality_traits TEXT[], -- ["analytical", "creative", "detail-oriented"]
    communication_style VARCHAR(50), -- "direct", "diplomatic", "technical"
    motivation_factors TEXT[], -- ["challenge", "growth", "stability"]
    
    -- Karriere-Entwicklung
    career_goals TEXT,
    development_areas TEXT[],
    mentoring_relationship BOOLEAN DEFAULT FALSE,
    
    -- Vertrauen und Zuverlässigkeit
    trust_indicators JSONB, -- {"punctuality": 5, "communication": 4, "delivery": 5}
    reliability_notes TEXT,
    red_flags TEXT[], -- Array von Warnsignalen
    
    -- Kontakt-Präferenzen
    preferred_contact_method VARCHAR(20) DEFAULT 'email' CHECK (preferred_contact_method IN ('email', 'phone', 'linkedin', 'whatsapp')),
    contact_frequency VARCHAR(20) DEFAULT 'monthly' CHECK (contact_frequency IN ('weekly', 'monthly', 'quarterly', 'as_needed')),
    best_contact_time VARCHAR(50), -- "mornings", "afternoons", "evenings"
    
    -- Metadaten
    created_by VARCHAR(100) DEFAULT 'system',
    last_interaction_date DATE,
    interaction_count INTEGER DEFAULT 0
);

-- =============================================================================
-- CONTACT_HISTORY TABLE - Kontakt-Verlauf
-- =============================================================================
CREATE TABLE IF NOT EXISTS contact_history (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    profile_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    relationship_id UUID REFERENCES relationships(id) ON DELETE SET NULL,
    
    -- Kontakt-Details
    contact_type VARCHAR(20) NOT NULL CHECK (contact_type IN ('call', 'email', 'meeting', 'linkedin', 'project_discussion', 'check_in')),
    contact_method VARCHAR(20) NOT NULL CHECK (contact_method IN ('phone', 'email', 'video_call', 'in_person', 'linkedin', 'whatsapp')),
    
    -- Inhalt
    subject VARCHAR(255),
    notes TEXT NOT NULL,
    outcome VARCHAR(50), -- "positive", "neutral", "concerns", "follow_up_needed"
    
    -- Follow-up
    follow_up_required BOOLEAN DEFAULT FALSE,
    follow_up_date DATE,
    follow_up_notes TEXT,
    
    -- Metadaten
    duration_minutes INTEGER,
    initiated_by VARCHAR(50) DEFAULT 'recruiter',
    mood_rating INTEGER CHECK (mood_rating BETWEEN 1 AND 5), -- 1=sehr schlecht, 5=sehr gut
    satisfaction_rating INTEGER CHECK (satisfaction_rating BETWEEN 1 AND 5)
);

-- =============================================================================
-- PROJECTS TABLE - Projekt-Informationen
-- =============================================================================
CREATE TABLE IF NOT EXISTS projects (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Projekt-Grunddaten
    title VARCHAR(255) NOT NULL,
    description TEXT,
    client_company VARCHAR(255),
    industry VARCHAR(100),
    
    -- Anforderungen
    required_skills TEXT[] NOT NULL,
    preferred_skills TEXT[],
    soft_skills_required TEXT[],
    experience_level VARCHAR(20) DEFAULT 'mid' CHECK (experience_level IN ('junior', 'mid', 'senior', 'lead', 'expert')),
    
    -- Projekt-Details
    duration_months INTEGER,
    start_date DATE,
    end_date DATE,
    hours_per_week INTEGER,
    remote_allowed BOOLEAN DEFAULT TRUE,
    onsite_required BOOLEAN DEFAULT FALSE,
    
    -- Budget und Status
    budget_range VARCHAR(50), -- "50k-100k", "100k-200k", "200k+"
    project_status VARCHAR(20) DEFAULT 'planning' CHECK (project_status IN ('planning', 'active', 'completed', 'cancelled')),
    priority_level INTEGER DEFAULT 3 CHECK (priority_level BETWEEN 1 AND 5),
    
    -- Persönliche Anforderungen
    personality_fit_required TEXT[], -- ["analytical", "creative", "team_player"]
    communication_style_preferred VARCHAR(50),
    client_culture VARCHAR(100), -- "startup", "corporate", "consulting"
    
    -- Metadaten
    created_by VARCHAR(100) DEFAULT 'recruiter',
    last_updated_by VARCHAR(100),
    internal_notes TEXT
);

-- =============================================================================
-- PROJECT_MATCHES TABLE - Projekt-Zuordnungen
-- =============================================================================
CREATE TABLE IF NOT EXISTS project_matches (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    profile_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    
    -- Matching-Scores
    skill_match_score DECIMAL(3,2) NOT NULL CHECK (skill_match_score BETWEEN 0.0 AND 1.0),
    experience_match_score DECIMAL(3,2) NOT NULL CHECK (experience_match_score BETWEEN 0.0 AND 1.0),
    personality_match_score DECIMAL(3,2) CHECK (personality_match_score BETWEEN 0.0 AND 1.0),
    availability_match_score DECIMAL(3,2) CHECK (availability_match_score BETWEEN 0.0 AND 1.0),
    overall_match_score DECIMAL(3,2) NOT NULL CHECK (overall_match_score BETWEEN 0.0 AND 1.0),
    
    -- Persönliche Empfehlung
    personal_recommendation BOOLEAN DEFAULT FALSE,
    recommendation_reason TEXT,
    confidence_level INTEGER CHECK (confidence_level BETWEEN 1 AND 5),
    
    -- Status
    match_status VARCHAR(20) DEFAULT 'suggested' CHECK (match_status IN ('suggested', 'contacted', 'interested', 'not_interested', 'placed')),
    contact_date DATE,
    response_date DATE,
    response_notes TEXT,
    
    -- Metadaten
    created_by VARCHAR(100) DEFAULT 'system',
    last_updated_by VARCHAR(100)
);

-- =============================================================================
-- INDEXES für Performance
-- =============================================================================

-- Profiles Indexes
CREATE INDEX IF NOT EXISTS idx_profiles_boutique_status ON profiles(boutique_status);
CREATE INDEX IF NOT EXISTS idx_profiles_trust_level ON profiles(trust_level);
CREATE INDEX IF NOT EXISTS idx_profiles_availability ON profiles(availability_status);
CREATE INDEX IF NOT EXISTS idx_profiles_skills ON profiles USING GIN(technical_skills);
CREATE INDEX IF NOT EXISTS idx_profiles_company_exp ON profiles USING GIN(company_experience);
CREATE INDEX IF NOT EXISTS idx_profiles_search ON profiles USING GIN(search_vector);

-- Relationships Indexes
CREATE INDEX IF NOT EXISTS idx_relationships_profile_id ON relationships(profile_id);
CREATE INDEX IF NOT EXISTS idx_relationships_type ON relationships(relationship_type);
CREATE INDEX IF NOT EXISTS idx_relationships_strength ON relationships(relationship_strength);

-- Contact History Indexes
CREATE INDEX IF NOT EXISTS idx_contact_history_profile_id ON contact_history(profile_id);
CREATE INDEX IF NOT EXISTS idx_contact_history_date ON contact_history(created_at);
CREATE INDEX IF NOT EXISTS idx_contact_history_type ON contact_history(contact_type);

-- Projects Indexes
CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(project_status);
CREATE INDEX IF NOT EXISTS idx_projects_skills ON projects USING GIN(required_skills);
CREATE INDEX IF NOT EXISTS idx_projects_industry ON projects(industry);

-- Project Matches Indexes
CREATE INDEX IF NOT EXISTS idx_project_matches_project_id ON project_matches(project_id);
CREATE INDEX IF NOT EXISTS idx_project_matches_profile_id ON project_matches(profile_id);
CREATE INDEX IF NOT EXISTS idx_project_matches_score ON project_matches(overall_match_score DESC);

-- =============================================================================
-- TRIGGERS für automatische Updates
-- =============================================================================

-- Update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Update search_vector for profiles
CREATE OR REPLACE FUNCTION update_search_vector()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector := 
        setweight(to_tsvector('english', COALESCE(NEW.first_name, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.last_name, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.email, '')), 'B') ||
        setweight(to_tsvector('english', COALESCE(array_to_string(NEW.technical_skills, ' '), '')), 'C') ||
        setweight(to_tsvector('english', COALESCE(array_to_string(NEW.soft_skills, ' '), '')), 'C') ||
        setweight(to_tsvector('english', COALESCE(NEW.company_experience::text, '')), 'D');
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_relationships_updated_at BEFORE UPDATE ON relationships FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Search vector triggers
CREATE TRIGGER update_profiles_search_vector BEFORE INSERT OR UPDATE ON profiles FOR EACH ROW EXECUTE FUNCTION update_search_vector();

-- =============================================================================
-- ROW LEVEL SECURITY (RLS)
-- =============================================================================

-- Enable RLS on all tables
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE relationships ENABLE ROW LEVEL SECURITY;
ALTER TABLE contact_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE project_matches ENABLE ROW LEVEL SECURITY;

-- Create policies (adjust based on your auth setup)
-- For now, allow all operations (you can restrict later)
CREATE POLICY "Allow all operations on profiles" ON profiles FOR ALL USING (true);
CREATE POLICY "Allow all operations on relationships" ON relationships FOR ALL USING (true);
CREATE POLICY "Allow all operations on contact_history" ON contact_history FOR ALL USING (true);
CREATE POLICY "Allow all operations on projects" ON projects FOR ALL USING (true);
CREATE POLICY "Allow all operations on project_matches" ON project_matches FOR ALL USING (true);

-- =============================================================================
-- SAMPLE DATA (Optional - für Testing)
-- =============================================================================

-- Insert sample profile
INSERT INTO profiles (
    first_name, last_name, email, boutique_status, trust_level,
    technical_skills, soft_skills, company_experience,
    reliability_score, experience_score, quality_score
) VALUES (
    'Max', 'Mustermann', 'max.mustermann@example.com', 'active', 3,
    ARRAY['Python', 'React', 'AWS'], ARRAY['Teamwork', 'Communication'],
    '{"BMW": "2 years", "SAP": "1 year"}',
    0.85, 0.90, 0.88
) ON CONFLICT (email) DO NOTHING;

-- Insert sample relationship
INSERT INTO relationships (
    profile_id, relationship_type, relationship_strength,
    personal_notes, personality_traits, communication_style
) SELECT 
    p.id, 'professional', 4,
    'Sehr zuverlässig, arbeitet gerne remote',
    ARRAY['analytical', 'detail-oriented'], 'technical'
FROM profiles p WHERE p.email = 'max.mustermann@example.com';

-- Insert sample project
INSERT INTO projects (
    title, description, client_company, industry,
    required_skills, experience_level, duration_months
) VALUES (
    'React Frontend Development',
    'Entwicklung einer modernen React-Anwendung für BMW',
    'BMW', 'Automotive',
    ARRAY['React', 'TypeScript', 'CSS'], 'senior', 6
);

-- =============================================================================
-- COMMENTS für Dokumentation
-- =============================================================================

COMMENT ON TABLE profiles IS 'Haupttabelle für Kandidaten mit Boutique-Architektur (max. 100)';
COMMENT ON TABLE relationships IS 'Persönliche Beziehungen und Notizen zu Kandidaten';
COMMENT ON TABLE contact_history IS 'Vollständiger Kontakt-Verlauf für jeden Kandidaten';
COMMENT ON TABLE projects IS 'Projekt-Informationen mit Anforderungen';
COMMENT ON TABLE project_matches IS 'Intelligente Projekt-Zuordnungen mit Scores';

COMMENT ON COLUMN profiles.boutique_status IS 'Status im Boutique-System: candidate, active, trusted, archived';
COMMENT ON COLUMN profiles.trust_level IS 'Vertrauens-Level: 1=new, 5=trusted';
COMMENT ON COLUMN profiles.company_experience IS 'JSON mit Firmen-Erfahrung für Cross-connections';
COMMENT ON COLUMN relationships.personal_notes IS 'Persönliche Notizen über den Kandidaten';
COMMENT ON COLUMN project_matches.personal_recommendation IS 'Persönliche Empfehlung basierend auf Beziehung';
