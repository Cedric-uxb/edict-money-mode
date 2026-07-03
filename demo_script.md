# Short Demo Script

操作说明为中文；英文台词是录制时直接念的内容。

## 录制前准备

- 启动应用：`python -m streamlit run app.py`
- 浏览器准备两个标签页：GitHub README 和 Streamlit app。
- 不展示终端里的本地路径、私人日志、简历或账号信息。

## 0:00-0:15 - 项目定位

**画面操作：** 展示 GitHub README 开头和 Challenge Fit。

**英文台词：**

> This is Edict Work Mode, my July IBM AI Builders Challenge wildcard project for the Future of Work theme.

> It helps users decide which work opportunities are safe, realistic, and worth pursuing.

## 0:15-1:25 - 原型演示

**画面操作：** 切换到 Streamlit app，展示 opportunity board。把下面这段粘贴到 Paste opportunity text，然后确认新机会出现在表格里：

```text
Fix Google Sheets API automation
Platform: Upwork
Budget: Hourly: $10.00 - $40.00
Proposals: Fewer than 5
Client: Payment verified, 5.0 rating
Connects: 8
Skills: Python, Google Sheets, API, Automation

Need a small script fix for a Google Sheets API workflow.
```

然后点击 Run decision workflow。如果时间紧，不要调 slider。

**英文台词：**

> The prototype scores each opportunity by fit, speed, trust, money, and risk. It recommends apply, watch, or veto.

> I can paste a job description. The app extracts budget, proposal count, client signal, connects, and skills, then scores it with the same workflow.

> It also checks proposal credits. If the user does not have enough connects, the workflow blocks the action.

> Nothing is submitted automatically. The user still approves every final action.

## 1:25-1:55 - 架构和 IBM Bob

**画面操作：** 回到 README，只展示 IBM Technology Evidence / IBM Bob screenshots。不用详细讲完整架构。

**英文台词：**

> The workflow is organized into small decision departments for classification, planning, veto, resource checks, compliance, and reputation.

> IBM Bob is the primary IBM AI-supported development tool. Bob reviewed the architecture, suggested the parsing improvement, and helped prepare the documentation.

## 1:55-2:20 - 限制和下一步

**画面操作：** 展示 Limitations 和 Future Improvements。

**英文台词：**

> This is a proof of concept. It uses local transparent parsing and sanitized sample data. A future version could replace the parser with IBM Granite while keeping human approval gates.

> Thank you for watching.
