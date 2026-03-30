# Reports Directory: GCP Shop Drawing Mirror

**Mirror ID:** `gcp_shopdrawing`
**Last Updated:** 2026-03-20

---

## Purpose

This directory contains generated reports for the `gcp_shopdrawing` mirror. Reports provide periodic summaries of mirror health, sync operations, parity measurements, drift events, and consumer activity. They are the primary communication mechanism between the mirror's automated systems and the platform team.

---

## Report Types

### 1. Sync Health Report

**Frequency:** Daily
**Contents:** Summary of all sync operations in the reporting period: cycles completed, records processed, records quarantined, errors encountered, average cycle duration, API call counts.

### 2. Parity Report

**Frequency:** Weekly
**Contents:** Parity measurements for all active slices over the reporting period. Trend analysis showing parity trajectory. Flagged slices approaching drift tolerance.

### 3. Drift Report

**Frequency:** On event (plus weekly summary)
**Contents:** Details of any drift events detected: type, magnitude, affected slices, root cause (if known), remediation status.

### 4. Consumer Activity Report

**Frequency:** Monthly
**Contents:** Which consumers are actively reading reflected data. Data access patterns. Unused reflections (candidates for deactivation). Consumer feedback summary.

### 5. Breakaway Readiness Report

**Frequency:** Quarterly
**Contents:** Results of the breakaway readiness checklist. Any readiness gaps identified. Dry run results if conducted in the reporting period.

### 6. Mirror Health Dashboard

**Frequency:** Continuous (real-time)
**Contents:** Current state of all slices, latest parity scores, sync agent status, trust boundary health, open incidents.

---

## Directory Structure

```
reports/
  daily/                   # Daily sync health reports
  weekly/                  # Weekly parity and drift summaries
  monthly/                 # Monthly consumer activity reports
  quarterly/               # Quarterly breakaway readiness and comprehensive reviews
  incident/                # Reports generated for specific incidents
  ad-hoc/                  # One-off reports for investigations or stakeholder requests
```

---

## Report Distribution

| Report | Audience | Channel |
|--------|----------|---------|
| Sync Health | Platform team | Automated alert channel |
| Parity | Platform team, mirror stakeholders | Email digest |
| Drift | Platform team (immediate), stakeholders (summary) | Alert + digest |
| Consumer Activity | Platform team, product owners | Monthly review |
| Breakaway Readiness | Platform team, architecture review | Quarterly review |

---

## Report Retention

| Report Type | Retention |
|-------------|-----------|
| Daily | 90 days |
| Weekly | 1 year |
| Monthly | 2 years |
| Quarterly | Indefinite |
| Incident | Indefinite |
