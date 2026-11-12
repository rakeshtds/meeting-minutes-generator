# Lakehouse Platform Weekly Sync

**Date:** 2026-11-04

**Attendees:** Rakesh Sharma, Priya Nair, Tom Becker, Aisha Khan

## Agenda

- Migration progress for the remaining warehouse domains
- Cortex Analyst rollout plan
- Data quality gate thresholds

## Summary

The team reviewed migration progress: nine of twelve domains are now live on the lakehouse, with capital markets on track for the following sprint. Cortex Analyst will roll out to the governance team first, using the PRISM semantic view as the pilot surface. The group agreed to tighten the data quality gate so any failed critical test blocks promotion to the Standard zone.

## Decisions

- Cortex Analyst pilot starts with the governance team on the PRISM semantic view
- Failed critical data quality tests block promotion to the Standard zone
- Capital markets migration stays in the current sprint plan

## Action Items

| Task | Owner | Due |
| --- | --- | --- |
| Publish the golden-question set for Cortex Analyst validation | Priya Nair | 2026-11-11 |
| Add blocking quality gates to the promotion pipeline | Tom Becker | 2026-11-13 |
| Draft the domain cutover checklist for capital markets | Aisha Khan | 2026-11-10 |

## Open Questions

- Do we retire the legacy reporting extracts in Q1 or run them in parallel for one more quarter?
