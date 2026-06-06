const form = document.querySelector("#planner-form");
const brainDump = document.querySelector("#brain-dump");
const persona = document.querySelector("#persona");
const energy = document.querySelector("#energy");
const energyLabel = document.querySelector("#energy-label");
const exampleButton = document.querySelector("#example-button");
const clearButton = document.querySelector("#clear-button");
const copyButton = document.querySelector("#copy-button");
const shareButton = document.querySelector("#share-button");
const saveStatus = document.querySelector("#save-status");
const langButtons = document.querySelectorAll(".lang-button");

const todayList = document.querySelector("#today-list");
const laterList = document.querySelector("#later-list");
const releaseList = document.querySelector("#release-list");
const sprintList = document.querySelector("#sprint-list");
const messageDraft = document.querySelector("#message-draft");
const taskCount = document.querySelector("#task-count");
const focusCount = document.querySelector("#focus-count");
const reliefCount = document.querySelector("#relief-count");
const STORAGE_KEYS = {
  draft: "calmplan-draft",
  language: "calmplan-language",
};

const i18n = {
  en: {
    kicker: "CalmPlan",
    title: "Turn mental chaos into a calm 30-minute plan.",
    summary:
      "Drop every task, worry, deadline, and loose thought here. CalmPlan sorts the mess into a short plan you can actually start.",
    modeLabel: "Mode",
    modeStudent: "Student",
    modeJobHunter: "Job hunter",
    modeFreelancer: "Freelancer",
    modeWorker: "Knowledge worker",
    energyLabel: "Energy",
    brainDumpLabel: "Brain dump",
    generateButton: "Generate plan",
    exampleButton: "Use example",
    clearButton: "Clear",
    installLink: "Install on phone",
    feedbackLink: "Give feedback",
    privacyLink: "Privacy",
    todayKicker: "Today",
    resultsTitle: "Your calm plan",
    copyButton: "Copy Markdown",
    shareButton: "Share",
    copiedButton: "Copied",
    sharedButton: "Shared",
    savedStatus: "Saved on this device",
    restoredStatus: "Restored from this device",
    itemsSorted: "items sorted",
    focusItems: "focus items",
    releaseItems: "release items",
    doToday: "Do today",
    parkLater: "Park for later",
    release: "Release",
    sprint: "30-minute sprint",
    messageDraft: "Message draft",
    noFocus: "No focus item yet.",
    nothingHere: "Nothing here yet.",
    emptyMessage:
      "Add a brain dump, then CalmPlan will draft one short message you can send to reduce pressure.",
    placeholder:
      "Example: finish stats homework, apply to 3 remote jobs, email professor, rent is stressing me out, prepare interview, laundry, call family",
    energyNames: {
      1: "Low",
      2: "Careful",
      3: "Steady",
      4: "Ready",
      5: "Sharp",
    },
    tagLabels: {
      due: "due",
      career: "career",
      school: "school",
      message: "message",
      stress: "stress",
      life: "life",
    },
    example: [
      "finish stats homework due tomorrow",
      "apply to 3 remote AI jobs",
      "email professor because I am confused about the project",
      "rent is stressing me out",
      "prepare for possible interview",
      "laundry",
      "call family",
      "organize Edict GitHub readme",
    ].join("\n"),
  },
  zh: {
    kicker: "CalmPlan",
    title: "把脑子里的混乱，变成今天能开始的 30 分钟计划。",
    summary:
      "把任务、焦虑、截止日期和零散想法都丢进来。CalmPlan 会帮你整理成一个更轻、更能执行的今日计划。",
    modeLabel: "模式",
    modeStudent: "学生",
    modeJobHunter: "找工作",
    modeFreelancer: "自由职业",
    modeWorker: "知识工作者",
    energyLabel: "精力",
    brainDumpLabel: "脑内清单",
    generateButton: "生成计划",
    exampleButton: "使用示例",
    clearButton: "清空",
    installLink: "下载安装到手机",
    feedbackLink: "反馈建议",
    privacyLink: "隐私",
    todayKicker: "今天",
    resultsTitle: "你的平静计划",
    copyButton: "复制 Markdown",
    shareButton: "分享",
    copiedButton: "已复制",
    sharedButton: "已分享",
    savedStatus: "已保存到本机",
    restoredStatus: "已从本机恢复",
    itemsSorted: "已整理事项",
    focusItems: "重点事项",
    releaseItems: "可放下事项",
    doToday: "今天先做",
    parkLater: "之后再说",
    release: "先放下",
    sprint: "30 分钟冲刺",
    messageDraft: "消息草稿",
    noFocus: "还没有重点事项。",
    nothingHere: "这里暂时为空。",
    emptyMessage: "输入脑内清单后，CalmPlan 会生成一段能帮你减压的消息草稿。",
    placeholder:
      "例子：明天交统计作业，投 3 个远程 AI 工作，给教授发邮件，房租让我焦虑，准备面试，洗衣服，给家里打电话",
    energyNames: {
      1: "很低",
      2: "小心来",
      3: "稳定",
      4: "可以冲",
      5: "状态好",
    },
    tagLabels: {
      due: "截止",
      career: "职业",
      school: "学习",
      message: "沟通",
      stress: "焦虑",
      life: "生活",
    },
    example: [
      "明天交统计作业",
      "投 3 个远程 AI 工作",
      "给教授发邮件问项目要求",
      "房租让我有点焦虑",
      "准备可能的面试",
      "洗衣服",
      "给家里打电话",
      "整理 Edict 的 GitHub README",
    ].join("\n"),
  },
};

let language = localStorage.getItem(STORAGE_KEYS.language) || "en";
let lastPlan = null;
let saveStatusTimer = null;

langButtons.forEach((button) => {
  button.addEventListener("click", () => {
    setLanguage(button.dataset.lang);
  });
});

energy.addEventListener("input", () => {
  updateEnergyLabel();
  saveDraft();
});

persona.addEventListener("change", () => {
  saveDraft();
});

brainDump.addEventListener("input", () => {
  saveDraft();
});

exampleButton.addEventListener("click", () => {
  brainDump.value = t("example");
  generateAndRender();
});

clearButton.addEventListener("click", () => {
  brainDump.value = "";
  lastPlan = null;
  localStorage.removeItem(STORAGE_KEYS.draft);
  setSaveStatus("");
  renderPlan(emptyPlan());
});

form.addEventListener("submit", (event) => {
  event.preventDefault();
  generateAndRender();
});

copyButton.addEventListener("click", async () => {
  const markdown = planToMarkdown(lastPlan || emptyPlan());
  await navigator.clipboard.writeText(markdown);
  copyButton.textContent = t("copiedButton");
  setTimeout(() => {
    copyButton.textContent = t("copyButton");
  }, 1400);
});

shareButton.addEventListener("click", async () => {
  const markdown = planToMarkdown(lastPlan || emptyPlan());
  if (navigator.share) {
    await navigator.share({
      title: "CalmPlan",
      text: markdown,
    });
    shareButton.textContent = t("sharedButton");
  } else {
    await navigator.clipboard.writeText(markdown);
    shareButton.textContent = t("copiedButton");
  }
  setTimeout(() => {
    shareButton.textContent = t("shareButton");
  }, 1400);
});

function setLanguage(nextLanguage) {
  language = nextLanguage;
  localStorage.setItem(STORAGE_KEYS.language, language);
  document.documentElement.lang = language === "zh" ? "zh-CN" : "en";
  document.querySelectorAll("[data-i18n]").forEach((node) => {
    node.textContent = t(node.dataset.i18n);
  });
  persona.querySelectorAll("option").forEach((option) => {
    option.textContent = t(option.dataset.i18n);
  });
  brainDump.placeholder = t("placeholder");
  langButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.lang === language);
  });
  updateEnergyLabel();
  renderPlan(lastPlan || emptyPlan());
  if (!navigator.share) {
    shareButton.textContent = t("shareButton");
  }
}

function t(key) {
  return i18n[language][key];
}

function updateEnergyLabel() {
  energyLabel.textContent = t("energyNames")[energy.value];
}

function generateAndRender() {
  const plan = buildPlan(brainDump.value, persona.value, Number(energy.value));
  lastPlan = plan;
  saveDraft();
  renderPlan(plan);
}

function saveDraft() {
  const draft = {
    text: brainDump.value,
    persona: persona.value,
    energy: energy.value,
    plan: lastPlan,
    savedAt: new Date().toISOString(),
  };
  localStorage.setItem(STORAGE_KEYS.draft, JSON.stringify(draft));
  setSaveStatus(t("savedStatus"));
}

function restoreDraft() {
  const raw = localStorage.getItem(STORAGE_KEYS.draft);
  if (!raw) return;
  try {
    const draft = JSON.parse(raw);
    brainDump.value = draft.text || "";
    persona.value = draft.persona || persona.value;
    energy.value = draft.energy || energy.value;
    lastPlan = draft.plan || null;
    updateEnergyLabel();
    renderPlan(lastPlan || emptyPlan());
    setSaveStatus(t("restoredStatus"));
  } catch {
    localStorage.removeItem(STORAGE_KEYS.draft);
  }
}

function setSaveStatus(message) {
  clearTimeout(saveStatusTimer);
  saveStatus.textContent = message;
  if (!message) return;
  saveStatusTimer = setTimeout(() => {
    saveStatus.textContent = "";
  }, 1800);
}

function buildPlan(text, mode, energyLevel) {
  const items = parseItems(text);
  const analyzed = items.map((item) => analyzeItem(item, mode));
  const sorted = [...analyzed].sort((a, b) => b.score - a.score);

  const maxToday = energyLevel <= 2 ? 2 : 3;
  const today = sorted.filter((item) => item.kind !== "release").slice(0, maxToday);
  const todaySet = new Set(today.map((item) => item.text));
  const release = sorted.filter((item) => item.kind === "release" || item.score <= 1).slice(0, 5);
  const releaseSet = new Set(release.map((item) => item.text));
  const later = sorted
    .filter((item) => !todaySet.has(item.text) && !releaseSet.has(item.text))
    .slice(0, 7);

  return {
    mode,
    energyLevel,
    items: analyzed,
    today,
    later,
    release,
    sprint: buildSprint(today, energyLevel),
    message: buildMessage(today, mode),
  };
}

function parseItems(text) {
  return text
    .split(/\n|,|;|，|；/)
    .map((item) => item.trim())
    .filter(Boolean)
    .slice(0, 24);
}

function analyzeItem(text, mode) {
  const lower = text.toLowerCase();
  let score = 2;
  const tags = [];

  if (/(due|tomorrow|today|tonight|deadline|urgent|exam|interview|明天|今天|今晚|截止|考试|面试|要交|ddl)/.test(lower)) {
    score += 4;
    tags.push("due");
  }
  if (/(apply|resume|job|proposal|client|upwork|handshake|interview|投|简历|工作|申请|客户|面试)/.test(lower)) {
    score += mode === "job-hunter" ? 4 : 2;
    tags.push("career");
  }
  if (/(homework|assignment|class|professor|study|quiz|exam|paper|作业|课程|教授|学习|测验|论文|项目)/.test(lower)) {
    score += mode === "student" ? 4 : 2;
    tags.push("school");
  }
  if (/(email|message|call|ask|reply|send|邮件|消息|电话|问|回复|发送|发)/.test(lower)) {
    score += 2;
    tags.push("message");
  }
  if (/(stress|worried|anxious|scared|overwhelmed|rent|money|health|焦虑|担心|害怕|压力|房租|钱|健康)/.test(lower)) {
    score += 1;
    tags.push("stress");
  }
  if (/(laundry|clean|dishes|groceries|walk|family|洗衣|打扫|洗碗|买菜|散步|家里|家人)/.test(lower)) {
    score -= 1;
    tags.push("life");
  }
  if (/(cannot control|waiting|maybe|what if|hope|afraid|控制不了|等|也许|万一|希望|怕)/.test(lower)) {
    score -= 2;
  }

  const kind = score <= 1 || (tags.includes("stress") && !hasActionVerb(lower)) ? "release" : "task";
  return { text, score, tags: [...new Set(tags)], kind };
}

function hasActionVerb(text) {
  return /(finish|send|email|call|apply|write|prepare|submit|study|fix|organize|pay|schedule|完成|发送|发邮件|打电话|申请|写|准备|提交|学习|修|整理|支付|安排)/.test(text);
}

function buildSprint(today, energyLevel) {
  if (today.length === 0) {
    return language === "zh"
      ? ["用 5 分钟写下所有乱掉的想法。", "选一个会让明天更轻松的小动作。", "只开始 10 分钟，不要求完美。"]
      : [
          "Set a 5-minute timer and write every loose thought in the input box.",
          "Pick one item that would make tomorrow easier.",
          "Do the smallest visible next step.",
        ];
  }

  const first = today[0].text;
  const minutes = energyLevel <= 2 ? [5, 15, 10] : [3, 22, 5];
  if (language === "zh") {
    return [
      `${minutes[0]} 分钟：打开「${first}」相关材料，写下下一步具体动作。`,
      `${minutes[1]} 分钟：只做这个动作，不重新规划整个人生。`,
      `${minutes[2]} 分钟：保存、发送，或写一句交接/下一步说明。`,
    ];
  }
  return [
    `${minutes[0]} min: open the materials for "${first}" and define the next visible action.`,
    `${minutes[1]} min: work only on that action; no reorganizing the whole day.`,
    `${minutes[2]} min: send, save, or write the next handoff note.`,
  ];
}

function buildMessage(today, mode) {
  const target = today.find((item) => item.tags.includes("message")) || today[0];
  if (!target) return t("emptyMessage");

  if (language === "zh") {
    if (mode === "student") {
      return `老师您好，我正在处理「${target.text}」，想确认一下我接下来应该优先关注哪一部分。您方便帮我确认一下重点吗？`;
    }
    if (mode === "job-hunter") {
      return "您好，谢谢这个机会。我可以进一步沟通岗位，也可以提供一个简短的相关项目示例供您参考。";
    }
    if (mode === "freelancer") {
      return "您好，我看过任务了。开始前我想先确认期望输出、一个示例输入和截止时间，这样可以更快交付。";
    }
    return `您好，简单同步一下：我会先处理「${target.text}」，完成下一步后再更新进展。`;
  }

  if (mode === "student") {
    return `Hi Professor, I am working on "${target.text}" and want to make sure I am focusing on the right next step. Could you please confirm what matters most for this part?`;
  }
  if (mode === "job-hunter") {
    return "Hi, thank you for the opportunity. I am available to discuss the role and can share a concise example of relevant project work if useful.";
  }
  if (mode === "freelancer") {
    return "Hi, I reviewed the task. My next step would be to confirm the expected output, one example input, and the deadline before I start.";
  }
  return `Hi, quick update: I am focusing first on "${target.text}" and will follow up once the next concrete step is complete.`;
}

function renderPlan(plan) {
  renderList(todayList, plan.today, true);
  renderList(laterList, plan.later, false);
  renderList(releaseList, plan.release, false);
  renderTextList(sprintList, plan.sprint);
  messageDraft.textContent = plan.message;
  taskCount.textContent = plan.items.length;
  focusCount.textContent = plan.today.length;
  reliefCount.textContent = plan.release.length;
}

function renderList(node, items, ordered) {
  node.innerHTML = "";
  if (items.length === 0) {
    const empty = document.createElement("li");
    empty.className = "empty";
    empty.textContent = ordered ? t("noFocus") : t("nothingHere");
    node.appendChild(empty);
    return;
  }

  for (const item of items) {
    const li = document.createElement("li");
    li.textContent = item.text;
    for (const tag of item.tags.slice(0, 2)) {
      const badge = document.createElement("span");
      badge.className = `tag ${tag}`;
      badge.textContent = t("tagLabels")[tag] || tag;
      li.appendChild(badge);
    }
    node.appendChild(li);
  }
}

function renderTextList(node, items) {
  node.innerHTML = "";
  for (const item of items) {
    const li = document.createElement("li");
    li.textContent = item;
    node.appendChild(li);
  }
}

function emptyPlan() {
  return {
    mode: "student",
    energyLevel: Number(energy.value),
    items: [],
    today: [],
    later: [],
    release: [],
    sprint: buildSprint([], Number(energy.value)),
    message: t("emptyMessage"),
  };
}

function planToMarkdown(plan) {
  const labels = {
    mode: t("modeLabel"),
    energy: t("energyLabel"),
    today: t("doToday"),
    later: t("parkLater"),
    release: t("release"),
    sprint: t("sprint"),
    message: t("messageDraft"),
  };
  const lines = [
    "# CalmPlan",
    "",
    `${labels.mode}: ${persona.options[persona.selectedIndex].text}`,
    `${labels.energy}: ${t("energyNames")[plan.energyLevel]}`,
    "",
    `## ${labels.today}`,
    ...markdownItems(plan.today.map((item) => item.text)),
    "",
    `## ${labels.later}`,
    ...markdownItems(plan.later.map((item) => item.text)),
    "",
    `## ${labels.release}`,
    ...markdownItems(plan.release.map((item) => item.text)),
    "",
    `## ${labels.sprint}`,
    ...markdownItems(plan.sprint),
    "",
    `## ${labels.message}`,
    "",
    plan.message,
    "",
  ];
  return lines.join("\n");
}

function markdownItems(items) {
  if (!items.length) return ["- None"];
  return items.map((item) => `- ${item}`);
}

if ("serviceWorker" in navigator && location.protocol !== "file:") {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("./sw.js").catch(() => {});
  });
}

setLanguage(language);
restoreDraft();
