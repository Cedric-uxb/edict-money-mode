# Proof Before Apply Demo Script

操作说明为中文；英文台词是录制时直接念的内容。目标时长：2 分 20 秒到 2 分 40 秒。

## 录制前准备

- 启动应用：`python3 -m streamlit run app.py`
- 浏览器准备两个标签页：GitHub README 和 Streamlit app。
- README 停在顶部评估表，Streamlit 停在输入框。
- 不展示终端本地路径、账号、邮件、登录页或私人机会数据。

## 0:00-0:20 - 问题

**画面操作：** 展示 README 标题、简介和评估表。

**英文台词：**

> This is Edict Work Mode: Proof Before Apply. Students and early-career builders often waste time, proposal credits, and reputation on opportunities that look attractive but contain unsafe conditions.

> Edict makes that decision inspectable before any application is submitted.

## 0:20-1:20 - 单一高风险场景

**画面操作：** 切换到 Streamlit，把下方文本粘贴进 `Paste opportunity text`：

```text
Python automation fix with unpaid test task
Platform: Upwork
Budget: Hourly: $10.00 - $40.00
Proposals: Fewer than 5
Client: Payment verified, 5.0 rating
Connects: 8
Skills: Python, Automation, API, Google Sheets

Complete an unpaid test task before a contract is offered.
```

点击 `Run decision workflow`，在表格中找到新机会，展示 `veto`、risk 和 reason。再快速指出 Connects monitor 和最终人工批准提示。

**英文台词：**

> This opportunity has strong technical fit, a verified client, and low competition. A naive score would recommend applying.

> But the description requires an unpaid test before a contract. Edict treats that as a hard safety signal, returns veto, and explains the risk.

> The same workflow checks proposal credits, and it never spends Connects or submits an application automatically. The user keeps final control.

## 1:20-1:55 - 可复现证据

**画面操作：** 回到 README 的评估表，依次指向 baseline、after 和 `evals/cases.jsonl` 链接。

**英文台词：**

> I tested the rules on twelve synthetic cases. The baseline missed unpaid tests, off-platform crypto payment, and credential sharing.

> After one shared risk-rule change, exact agreement improved from seventy-five to one hundred percent, and veto recall improved from fifty-seven point one four to one hundred percent while precision stayed at one hundred percent.

> This is a small synthetic rule evaluation, not a claim of real-world model accuracy.

## 1:55-2:30 - IBM Bob 证据

**画面操作：** 展示 README 中两张 IBM Bob 截图，再打开 `BOB.md` 的 Verified Bob Contribution。

**英文台词：**

> IBM Bob reviewed the repository and recommended a minimal opportunity parsing workflow that reused the existing scoring and veto architecture.

> The repository preserves Bob screenshots, the implementation commit, and a development log. I accepted the focused parser and kept it local instead of adding an unnecessary external model dependency.

> Edict is intentionally transparent, privacy-conscious, and human-approved. Thank you.
