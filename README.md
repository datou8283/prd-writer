# PRD Writer

Claude Code skills — 讓 Claude 幫你寫競品分析、PRD、API 設計、埋點規劃、release note。

## 這是什麼

這個 repo 裡面有 9 個 Claude Code skill，裝好之後你在 Claude Code 裡面打 `/` 就能看到所有指令。不用每次都重新解釋格式、風格、流程。

最強的用法：打 `/feature-workflow` 一鍵跑完整個 PRD pipeline。

## 有哪些 skill

### 完整流程（一鍵搞定）

| 指令 | 做什麼 |
|------|--------|
| `/feature-workflow` | 一鍵跑完整個 PRD pipeline：競品分析 → 確認 scope → 寫 PRD → 4 角色 review → 埋點規劃 |

### 個別 skill（可單獨使用）

| 指令 | 做什麼 | 什麼時候用 |
|------|--------|-----------|
| `/crypto-exchange-competitor-analysis` | 競品分析報告 | 寫 PRD **之前**先跑這個 |
| `/write-prd` | 寫 PRD | 主要的，寫完整的 PRD 文件 |
| `/prd-review` | 4 角色 PRD review | PRD 寫完後跑，Product/Eng/Design/QA 四個角度審查 |
| `/design-api` | 設計 API | PRD 裡面要寫 API spec 的時候 |
| `/write-api-endpoint` | 寫 TypeScript endpoint | 工程師實作 API 的時候 |
| `/write-posthog-events` | 埋點規劃 | PRD 寫完**之後**跑這個 |
| `/write-release-note` | App release note | 產出 App Store + in-app 公告兩個版本 |
| `/admin-wireframe` | Admin 後台 wireframe | PRD 有 admin 頁面需求時自動或手動觸發 |

### 完整流程

```
/feature-workflow [feature name]
```

等同於自動跑完：

```
競品分析 → ⏸確認 scope → 寫 PRD → 4 角色 review → ⏸你決策 → 埋點規劃
```

中間有兩個人工 checkpoint，你確認後才會繼續。

不一定每次都要跑全部，個別 skill 也可以單獨使用。

## 安裝（第一次設定，5 分鐘）

### 1. 確認你有 Claude Code

如果你還沒裝，先裝：

```bash
npm install -g @anthropic-ai/claude-code
```

裝好後跑 `claude` 確認能打開。

### 2. Clone 這個 repo

```bash
git clone git@github.com:datou8283/prd-writer.git
```

### 3. 進去這個資料夾，打開 Claude Code

```bash
cd prd-writer
claude
```

就這樣，裝好了。

## 怎麼用

1. 在 `prd-writer` 資料夾裡開 Claude Code
2. 打 `/` 選你要用的 skill，或直接輸入 `/feature-workflow Chase Order`
3. Claude 會開始按照標準格式執行
4. 跟 Claude 對話，補充細節、調整範圍
5. 產出的 `.docx` 會存在 `docs/` 資料夾

### 小提醒

- 打 `/` 就會看到所有可用的 skill，用方向鍵選
- 如果你只是想改 PRD 的某一段，直接跟 Claude 說就好，不用重新跑 skill
- 產出的 `.docx` 會存在 `docs/` 資料夾（這個資料夾不會上傳到 GitHub）
- Memory 資料夾（`.claude/memory/`）會透過 git 同步，跨電腦也能保持 context

## 有問題？

找 Danny。
