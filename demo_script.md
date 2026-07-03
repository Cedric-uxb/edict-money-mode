# 3-Minute Demo Script

操作说明为中文；英文台词是录制时直接念的内容。

## 录制前准备

- 启动应用：`python -m streamlit run app.py`
- 浏览器准备两个标签页：GitHub README 和 Streamlit app。
- 不展示终端里的本地路径、私人日志、简历或账号信息。

## 0:00-0:25 - 项目定位

**画面操作：** 展示 GitHub README 开头和 Challenge Fit。

**英文台词：**

> This is Edict Work Mode, my July IBM AI Builders Challenge wildcard project. It is an intelligent work decision-support prototype for the Future of Work theme.

> The goal is to help a user decide which opportunities are realistic, safe, and worth pursuing before spending time, proposal credits, or reputation.

## 0:25-1:45 - 原型演示

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

然后调整 connects slider，点击 Run decision workflow。

**英文台词：**

> The prototype scores opportunities by fit, speed, trust, money, and risk. It can recommend apply, watch, or veto.

> I can also paste an unstructured opportunity description. The app extracts fields like platform, budget, proposal count, client signal, required connects, and skills, then sends the parsed opportunity through the same scoring workflow.

> It also checks resource constraints. For example, if an opportunity needs more proposal credits than the user has, the workflow blocks that action instead of blindly moving forward.

> The output is not an automatic submission. It is a decision memo and action plan that still requires human approval.

## 1:45-2:25 - 架构和 IBM Bob

**画面操作：** 回到 README，展示 AI Approach and Architecture，再展示 IBM Bob Usage 和 Bob screenshots。

**英文台词：**

> The architecture is organized as a set of specialized departments: classification, opportunity intelligence, planning, veto, resource checks, execution, compliance, and reputation.

> IBM Bob is the primary IBM AI-supported development tool for this project. Bob helped review the architecture, identify the opportunity parsing improvement, and prepare the project documentation.

## 2:25-2:55 - 限制和下一步

**画面操作：** 展示 Limitations 和 Future Improvements。

**英文台词：**

> This is a proof of concept. The current version uses transparent local parsing and scoring rules with sanitized sample data. Future versions can replace the parser with IBM Granite or another LLM layer, add real imports, and draft proposals while keeping human approval gates.

> Thank you for watching.
