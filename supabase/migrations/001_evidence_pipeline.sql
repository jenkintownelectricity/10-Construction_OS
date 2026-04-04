-- Evidence Intake Pipeline Schema
-- Construction OS — Supabase Migration 001
-- UTC is canonical. All timestamps stored as timestamptz.

-- Storage posture enum
create type storage_posture as enum (
  'temporary_processing',
  'queue_safeguarded',
  'vaulted'
);

-- Processing status enum
create type processing_status as enum (
  'uploaded',
  'queued',
  'extracting',
  'extracted',
  'failed',
  'expired'
);

-- Evidence kind enum
create type evidence_kind as enum (
  'dxf_detail',
  'pdf_submittal',
  'assembly_letter',
  'spec_section',
  'product_data',
  'field_photo',
  'test_report',
  'certification',
  'other'
);

-- Companies
create table if not exists companies (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  slug text unique not null,
  created_at timestamptz not null default now()
);

-- Jobs
create table if not exists jobs (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references companies(id),
  job_number text not null,
  name text not null,
  created_at timestamptz not null default now()
);

-- Submittals
create table if not exists submittals (
  id uuid primary key default gen_random_uuid(),
  job_id uuid not null references jobs(id),
  submittal_number text not null,
  description text,
  created_at timestamptz not null default now()
);

-- Manufacturers
create table if not exists manufacturers (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  slug text unique not null,
  category text,
  created_at timestamptz not null default now()
);

-- System Families
create table if not exists system_families (
  id uuid primary key default gen_random_uuid(),
  manufacturer_id uuid not null references manufacturers(id),
  name text not null,
  slug text not null,
  system_type text,
  csi_section text,
  description text,
  created_at timestamptz not null default now(),
  unique (manufacturer_id, slug)
);

-- Systems (specific assemblies within a family)
create table if not exists systems (
  id uuid primary key default gen_random_uuid(),
  family_id uuid not null references system_families(id),
  name text not null,
  version text default '1.0',
  created_at timestamptz not null default now()
);

-- System Components
create table if not exists system_components (
  id uuid primary key default gen_random_uuid(),
  system_id uuid not null references systems(id),
  name text not null,
  role text not null,
  material_type text,
  ownership_class text default 'SYSTEM_OWNED',
  required boolean default true,
  sort_order integer default 0,
  created_at timestamptz not null default now()
);

-- System Details (condition → detail mapping)
create table if not exists system_details (
  id uuid primary key default gen_random_uuid(),
  system_id uuid not null references systems(id),
  condition_type text not null,
  detail_id text not null,
  detail_name text not null,
  description text,
  created_at timestamptz not null default now(),
  unique (system_id, condition_type)
);

-- Ingest Jobs (core evidence pipeline table)
create table if not exists ingest_jobs (
  id uuid primary key default gen_random_uuid(),
  company_id uuid references companies(id),
  job_id uuid references jobs(id),
  submittal_id uuid references submittals(id),
  manufacturer_id uuid references manufacturers(id),
  system_family_id uuid references system_families(id),
  filename text not null,
  file_extension text,
  mime_type text,
  evidence_kind evidence_kind not null default 'other',
  processing_status processing_status not null default 'uploaded',
  storage_posture storage_posture not null default 'temporary_processing',
  storage_bucket text not null,
  storage_object_path text not null,
  file_size_bytes bigint,
  uploaded_at_utc timestamptz not null default now(),
  expires_at_utc timestamptz,
  extracted_at_utc timestamptz,
  extraction_summary jsonb,
  created_at timestamptz not null default now()
);

-- Evidence Records (extracted intelligence)
create table if not exists evidence_records (
  id uuid primary key default gen_random_uuid(),
  ingest_job_id uuid not null references ingest_jobs(id),
  evidence_type text not null,
  extracted_data jsonb not null default '{}',
  confidence numeric(4,3),
  created_at timestamptz not null default now()
);

-- Generated Reports
create table if not exists generated_reports (
  id uuid primary key default gen_random_uuid(),
  ingest_job_id uuid references ingest_jobs(id),
  report_type text not null,
  report_data jsonb not null default '{}',
  created_at timestamptz not null default now()
);

-- Evidence Summary View
create or replace view v_evidence_summary as
select
  ij.id as ingest_job_id,
  c.name as company_name,
  j.job_number,
  j.name as job_name,
  s.submittal_number,
  m.name as manufacturer_name,
  sf.name as system_family_name,
  ij.filename,
  ij.evidence_kind,
  ij.processing_status,
  ij.storage_posture,
  ij.uploaded_at_utc,
  ij.extracted_at_utc,
  count(er.id) as evidence_record_count
from ingest_jobs ij
left join companies c on ij.company_id = c.id
left join jobs j on ij.job_id = j.id
left join submittals s on ij.submittal_id = s.id
left join manufacturers m on ij.manufacturer_id = m.id
left join system_families sf on ij.system_family_id = sf.id
left join evidence_records er on er.ingest_job_id = ij.id
group by ij.id, c.name, j.job_number, j.name, s.submittal_number,
         m.name, sf.name, ij.filename, ij.evidence_kind,
         ij.processing_status, ij.storage_posture,
         ij.uploaded_at_utc, ij.extracted_at_utc;

-- RLS policies (buckets must be private)
alter table ingest_jobs enable row level security;
alter table evidence_records enable row level security;
alter table generated_reports enable row level security;

-- Index for common queries
create index if not exists idx_ingest_jobs_status on ingest_jobs(processing_status);
create index if not exists idx_ingest_jobs_manufacturer on ingest_jobs(manufacturer_id);
create index if not exists idx_ingest_jobs_uploaded on ingest_jobs(uploaded_at_utc desc);
create index if not exists idx_evidence_records_job on evidence_records(ingest_job_id);
