---
name: Completed features log
description: Summary of features that have gone through the PRD workflow. Reference to avoid duplicate research or conflicting design.
type: project
---

# Completed Features

Log of features that have completed (or partially completed) the PRD workflow.

## Web Push Notifications (v1)

- **Status**: PostHog tracking spec completed
- **Scope**: Telegram/Discord channel binding + notification type preferences
- **Key endpoints**: TBD (not yet documented in memory)
- **PostHog events**: 8 events (see `project_web_push_posthog.md` for full spec)
- **Design decisions**:
  - Risk Alerts toggle not tracked (UI disabled, user can't operate)
  - Unbind event not tracked (Danny's call)
  - Bind flow split: started -> completed/failed for funnel analysis
  - Property naming: `notification_type` not `type`

---

(Add new features here as they complete the workflow)
