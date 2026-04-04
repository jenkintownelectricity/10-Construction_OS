-- Pipeline Execution Fields
-- Construction OS — Supabase Migration 002
-- Adds worker claim fields and downstream pipeline state tracking to ingest_jobs.

-- Worker claim fields
alter table ingest_jobs add column if not exists claimed_at_utc timestamptz;
alter table ingest_jobs add column if not exists worker_id text;

-- Extraction state
alter table ingest_jobs add column if not exists file_type text;
alter table ingest_jobs add column if not exists extraction_status text;
alter table ingest_jobs add column if not exists entity_count integer;

-- Ownership classification state
alter table ingest_jobs add column if not exists ownership_status text;
alter table ingest_jobs add column if not exists system_owned_count integer;
alter table ingest_jobs add column if not exists context_only_count integer;
alter table ingest_jobs add column if not exists annotation_count integer;

-- Condition detection state
alter table ingest_jobs add column if not exists condition_type text;
alter table ingest_jobs add column if not exists condition_support_state text;
alter table ingest_jobs add column if not exists condition_confidence numeric(4,3);

-- Assembly resolution state
alter table ingest_jobs add column if not exists assembly_candidate_status text;
alter table ingest_jobs add column if not exists resolution_status text;
alter table ingest_jobs add column if not exists resolved_detail_id text;
alter table ingest_jobs add column if not exists source_mode text;

-- Constraint decision state
alter table ingest_jobs add column if not exists constraint_action text;
alter table ingest_jobs add column if not exists constraint_severity text;
alter table ingest_jobs add column if not exists halt_reason text;
alter table ingest_jobs add column if not exists partial_reason text;

-- Guaranteed detail state
alter table ingest_jobs add column if not exists guarantee_state text;
alter table ingest_jobs add column if not exists guarantee_confidence numeric(4,3);

-- Receipt reference
alter table ingest_jobs add column if not exists receipt_reference text;

-- Update processing_status enum to include new states
-- (Postgres enums require ALTER TYPE ADD VALUE)
do $$ begin
  alter type processing_status add value if not exists 'claimed';
  alter type processing_status add value if not exists 'processing';
  alter type processing_status add value if not exists 'partial';
  alter type processing_status add value if not exists 'halted';
exception when others then null;
end $$;

-- Index for worker claims
create index if not exists idx_ingest_jobs_claimed on ingest_jobs(processing_status, claimed_at_utc)
  where processing_status in ('uploaded', 'queued');
