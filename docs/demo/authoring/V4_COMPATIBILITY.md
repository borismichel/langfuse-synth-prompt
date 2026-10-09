# Langfuse v4 compatibility audit — 2026-10-09

The reported `GET /api/public/traces` request came from two operator-only
credential probes, not the kit, companion or Depot runtime. The failed-key probe
was recorded at 06:58:53 UTC; replacement credential readback at 07:03:26 UTC.
Future operator inventory probes use observations v2. The user clarified that
one-off verification requests were acceptable, while legacy runtime calls were not.

Source inspection of the released kit, installed core v4.1.1 reader and Depot
application found no active legacy trace endpoint request. The remaining literal
references in dependency conformance rules and a Depot historical comment are
not requests.

- History verification and companion observation reads use
  `/api/public/v2/observations`, including trace/session filtering and cursor paging.
- Core trace/session helpers assemble observations rather than calling a legacy
  trace/session endpoint. Depot totals use observation-based v4 reads.
- Scores use `/api/public/v3/scores`, the current scores endpoint for Langfuse v4.
  Its API version number does not imply use of the Langfuse v3 platform.
- Native `/traces/<id>` browser links remain valid UI links, not legacy API calls.
- Prompt references stay on generations. User-feedback scores target the saved
  request observation; input judges and reply judges retain distinct subjects.

The pinned Langfuse Python SDK is 4.17.0. This audit is source/path evidence plus
the exact v0.1.0 admission result, not a claim to have exercised every third-party
SDK method. [Current API documentation](https://langfuse.com/docs/api-and-data-platform/features/public-api)
confirms observations v2 and scores v3 for the v4 platform.
