-- Barrett Demo Seed
-- Idempotent: uses ON CONFLICT to avoid duplicates.
-- UTC canonical.

-- Company
insert into companies (id, name, slug)
values ('a0000000-0000-0000-0000-000000000001', 'Barrett Roofing Demo', 'barrett-demo')
on conflict (slug) do nothing;

-- Job
insert into jobs (id, company_id, job_number, name)
values (
  'b0000000-0000-0000-0000-000000000001',
  'a0000000-0000-0000-0000-000000000001',
  'JOB-BARRETT-DEMO-001',
  'Barrett RamProof GC Demo Project'
)
on conflict do nothing;

-- Submittal
insert into submittals (id, job_id, submittal_number, description)
values (
  'c0000000-0000-0000-0000-000000000001',
  'b0000000-0000-0000-0000-000000000001',
  'SUB-BARRETT-DEMO-001',
  'Barrett RamProof GC shop drawing package'
)
on conflict do nothing;

-- Manufacturer: Barrett
insert into manufacturers (id, name, slug, category)
values ('d0000000-0000-0000-0000-000000000001', 'Barrett Roofing', 'barrett', 'roofing_waterproofing')
on conflict (slug) do nothing;

-- Manufacturer: ISOVER (scaffold)
insert into manufacturers (id, name, slug, category)
values ('d0000000-0000-0000-0000-000000000002', 'ISOVER Fireproofing', 'isover', 'fireproofing')
on conflict (slug) do nothing;

-- Manufacturer: GCP (scaffold)
insert into manufacturers (id, name, slug, category)
values ('d0000000-0000-0000-0000-000000000003', 'GCP Applied Technologies', 'gcp', 'waterproofing_air_barrier')
on conflict (slug) do nothing;

-- System Family: RamProof GC
insert into system_families (id, manufacturer_id, name, slug, system_type, csi_section, description)
values (
  'e0000000-0000-0000-0000-000000000001',
  'd0000000-0000-0000-0000-000000000001',
  'RamProof GC Waterproofing System',
  'ramproof_gc',
  'waterproofing',
  '07 11 13',
  'Single-component fluid-applied elastomeric rubberized asphalt waterproofing membrane.'
)
on conflict (manufacturer_id, slug) do nothing;

-- System Family: SBS Modified Bitumen
insert into system_families (id, manufacturer_id, name, slug, system_type, csi_section, description)
values (
  'e0000000-0000-0000-0000-000000000002',
  'd0000000-0000-0000-0000-000000000001',
  'SBS Modified Bitumen Roofing',
  'sbs_modified_bitumen',
  'roofing',
  '07 52 16',
  'Multi-ply SBS modified bitumen roofing system with mineral cap sheet.'
)
on conflict (manufacturer_id, slug) do nothing;

-- System: RamProof GC v1
insert into systems (id, family_id, name, version)
values (
  'f0000000-0000-0000-0000-000000000001',
  'e0000000-0000-0000-0000-000000000001',
  'RamProof GC Standard',
  '1.0'
)
on conflict do nothing;

-- System: SBS Standard
insert into systems (id, family_id, name, version)
values (
  'f0000000-0000-0000-0000-000000000002',
  'e0000000-0000-0000-0000-000000000002',
  'Barrett SBS Standard',
  '1.0'
)
on conflict do nothing;

-- RamProof GC Components (7 required)
insert into system_components (system_id, name, role, material_type, ownership_class, required, sort_order)
values
  ('f0000000-0000-0000-0000-000000000001', 'RamProof GC Membrane', 'membrane', 'fluid_applied_rubberized_asphalt', 'SYSTEM_OWNED', true, 1),
  ('f0000000-0000-0000-0000-000000000001', 'RamProof GC Primer', 'primer', 'asphalt_primer', 'SYSTEM_OWNED', true, 2),
  ('f0000000-0000-0000-0000-000000000001', 'Mesh Reinforcement', 'reinforcement', 'polyester_mesh', 'SYSTEM_OWNED', true, 3),
  ('f0000000-0000-0000-0000-000000000001', 'Ram Mastic', 'sealant', 'mastic_sealant', 'SYSTEM_OWNED', true, 4),
  ('f0000000-0000-0000-0000-000000000001', 'Drainage Mat', 'drainage', 'drainage_composite', 'SYSTEM_OWNED', true, 5),
  ('f0000000-0000-0000-0000-000000000001', 'Protection Course', 'protection', 'protection_board', 'SYSTEM_OWNED', true, 6),
  ('f0000000-0000-0000-0000-000000000001', 'Filter Fabric', 'filter', 'polyester_filter_fabric', 'SYSTEM_OWNED', false, 7)
on conflict do nothing;

-- RamProof GC System Details (condition → detail mapping)
insert into system_details (system_id, condition_type, detail_id, detail_name, description)
values
  ('f0000000-0000-0000-0000-000000000001', 'parapet', 'RP-RA-01', 'RamProof GC Parapet', 'Standard parapet termination with membrane turnup and metal coping'),
  ('f0000000-0000-0000-0000-000000000001', 'drain', 'RP-RD-01', 'RamProof GC Roof Drain', 'Roof drain with membrane collar and clamping ring'),
  ('f0000000-0000-0000-0000-000000000001', 'penetration', 'RP-RP-01', 'RamProof GC Pipe Penetration', 'Pipe penetration with membrane boot and sealant'),
  ('f0000000-0000-0000-0000-000000000001', 'corner', 'RP-RC-01', 'RamProof GC Corner Detail', 'Inside/outside corner with reinforced membrane'),
  ('f0000000-0000-0000-0000-000000000001', 'expansion_joint', 'RP-RE-01', 'RamProof GC Expansion Joint', 'Expansion joint with flexible membrane and bellows')
on conflict (system_id, condition_type) do nothing;

-- SBS System Details
insert into system_details (system_id, condition_type, detail_id, detail_name, description)
values
  ('f0000000-0000-0000-0000-000000000002', 'parapet', 'SBS-PA-01', 'SBS Parapet Termination', 'Standard SBS parapet termination with flashing, cant strip, termination bar, metal coping'),
  ('f0000000-0000-0000-0000-000000000002', 'drain', 'SBS-DR-01', 'SBS Roof Drain', 'Roof drain with flashing collar and clamping ring'),
  ('f0000000-0000-0000-0000-000000000002', 'penetration', 'SBS-PP-01', 'SBS Pipe Penetration', 'Pipe penetration through SBS membrane'),
  ('f0000000-0000-0000-0000-000000000002', 'corner', 'SBS-CR-01', 'SBS Corner Detail', 'Modified bitumen corner reinforcement'),
  ('f0000000-0000-0000-0000-000000000002', 'expansion_joint', 'SBS-EJ-01', 'SBS Expansion Joint', 'SBS expansion joint with flexible flashing')
on conflict (system_id, condition_type) do nothing;
