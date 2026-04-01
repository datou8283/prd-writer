---
name: Web Push Notifications PostHog events
description: PostHog event tracking spec for the Web Push Notifications feature (Telegram/Discord binding + notification type preferences)
type: project
---

Web Push Notifications (v1) 埋點規劃，共 8 個 events：

1. `notification_settings_viewed` — 進入 /notification/settings 頁，property: source (account_menu / direct_url / onboarding)
2. `notification_channel_bind_started` — 點擊 Bind 按鈕，property: channel (telegram / discord)
3. `notification_channel_code_copied` — 複製驗證碼，property: channel
4. `notification_channel_bot_link_clicked` — 點擊 bot deep link，property: channel
5. `notification_channel_bind_completed` — polling 確認綁定成功，property: channel
6. `notification_channel_bind_failed` — polling 逾時或驗證碼過期，properties: channel, failure_reason (timeout / code_expired / already_bound)
7. `notification_channel_toggled` — 啟用/停用已綁定管道，properties: channel, enabled (boolean)
8. `notification_type_toggled` — 切換通知類型，properties: notification_type (announcement / price_alert / deposits_withdrawals / order_updates), enabled (boolean)

**設計決策：**
- 不追蹤 Risk Alerts toggle（UI 上 disabled，用戶無法操作）
- 不追蹤 unbind 事件（Danny 判斷不需要）
- notification_type property 命名為 `notification_type` 而非 `type`，避免泛用名稱混淆
- bind flow 拆 started → completed/failed 方便漏斗分析

**Why:** 這是第一次用 write-posthog-events skill 產出的埋點，作為後續功能埋點的參考基準。
**How to apply:** 後續 Web Push Notifications 相關討論可參考此規劃。
