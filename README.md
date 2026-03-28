# PRD Writer

Claude Code skills — 讓 Claude 幫你寫競品分析、PRD、API 設計、埋點規劃。

## 這是什麼

這個 repo 裡面有 5 個 Claude Code skill，裝好之後你在 Claude Code 裡面打 `/write-prd` 就能讓 Claude 按照我們的標準格式幫你寫 PRD。不用每次都重新解釋格式、風格、流程。

## 有哪些 skill

| 指令 | 做什麼 | 什麼時候用 |
|------|--------|-----------|
| `/crypto-exchange-competitor-analysis` | 競品分析報告 | 寫 PRD **之前**先跑這個 |
| `/write-prd` | 寫 PRD | 主要的，寫完整的 PRD 文件 |
| `/design-api` | 設計 API | PRD 裡面要寫 API spec 的時候 |
| `/write-api-endpoint` | 寫 TypeScript endpoint | 工程師實作 API 的時候 |
| `/write-posthog-events` | 埋點規劃 | PRD 寫完**之後**跑這個 |

正常的完整流程是：

```
/crypto-exchange-competitor-analysis → /write-prd → /write-posthog-events
```

不一定每次都要跑全部，看需求。

## 安裝（第一次設定，5 分鐘）

### 1. 確認你有 Claude Code

如果你還沒裝，先裝：

```bash
npm install -g @anthropic-ai/claude-code
```

裝好後跑 `claude` 確認能打開。

### 2. Clone 這個 repo

```bash
git clone https://github.com/datou8283/prd-writer.git
```

### 3. 進去這個資料夾，打開 Claude Code

```bash
cd prd-writer
claude
```

就這樣，裝好了。

## 怎麼用

1. 在 `prd-writer` 資料夾裡開 Claude Code
2. 輸入 `/write-prd Homepage Navigation` （或任何你要寫的 feature 名稱）
3. Claude 會開始按照標準格式寫 PRD
4. 跟 Claude 對話，補充細節、調整範圍
5. 最後 Claude 會產出 `.docx` 檔案

### 小提醒

- 打 `/` 就會看到所有可用的 skill，用方向鍵選
- 如果你只是想改 PRD 的某一段，直接跟 Claude 說就好，不用重新跑 skill
- 產出的 `.docx` 會存在 `docs/` 資料夾（這個資料夾不會上傳到 GitHub）

## 有問題？

找 Danny。
