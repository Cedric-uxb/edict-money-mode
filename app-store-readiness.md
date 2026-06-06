# CalmPlan App Store Readiness

This file collects the material needed before CalmPlan can be submitted to app stores.

## Current Best Path

1. Ship public HTTPS PWA first.
2. Test with 10-20 real users on phones.
3. Add analytics only after privacy review.
4. Wrap with Capacitor if store distribution is still worth it.
5. Submit to Google Play first, then Apple App Store.

## Store Positioning

Name: CalmPlan

Short tagline:

> Turn mental chaos into a calm 30-minute plan.

Chinese tagline:

> 把脑子里的混乱，变成今天能开始的 30 分钟计划。

Category:

- Productivity
- Education, if targeting students first

Avoid:

- Do not claim treatment for anxiety, depression, ADHD, or medical conditions.
- Do not call it therapy or mental health treatment.
- Use productivity, planning, stress organization, and task clarity language.

## App Description

CalmPlan helps students, job hunters, freelancers, and knowledge workers turn a messy brain dump into a short action plan. Type every task, worry, deadline, and loose thought into one box. CalmPlan sorts the list into what to do today, what to park for later, what to release for now, a 30-minute sprint, and one message draft you can send to reduce pressure.

CalmPlan is intentionally small. It does not ask you to rebuild your entire life. It helps you choose the next 30 minutes.

## Chinese Description

CalmPlan 帮学生、找工作的人、自由职业者和知识工作者，把混乱的脑内清单整理成一个简短行动计划。

你只需要把任务、焦虑、deadline 和零散想法都输入进去。CalmPlan 会帮你整理成：今天先做什么、哪些可以推迟、哪些可以先放下、一个 30 分钟冲刺计划，以及一段可以发给老师/客户/雇主的消息草稿。

CalmPlan 故意做得很小。它不是让你重新规划整个人生，而是帮你开始接下来的 30 分钟。

## Required Before Store Submission

- Public app URL
- Privacy policy URL
- App icon PNG sizes
- iPhone screenshots
- Android screenshots
- Support/contact email
- Bundle identifier, for example `com.edict.calmplan`
- Wrapped native app project, likely Capacitor
- Developer accounts:
  - Apple Developer Program: $99/year
  - Google Play Console: one-time developer fee

## Current Assets

- Web app: `apps/calmplan/index.html`
- Privacy policy: `apps/calmplan/privacy.html`
- Install instructions: `apps/calmplan/install.html`
- PWA manifest: `apps/calmplan/manifest.webmanifest`
- Icon: `apps/calmplan/assets/icon.svg`
- PWA icon PNGs: `apps/calmplan/assets/icon-192.png`, `apps/calmplan/assets/icon-512.png`
- Xiaohongshu poster: `apps/calmplan/assets/xiaohongshu-poster.png`

## 2026-06-06 Progress

- Added local browser save/restore for the current brain dump and latest plan.
- Added mobile-friendly Share action with Copy Markdown fallback.
- Updated privacy policy to disclose local storage of draft and plan content.
- Updated service worker cache version to refresh phone installs.
- Verified mobile viewport at 390x844 and desktop viewport at 1280x900 with no console errors.
- Added feedback page and Xiaohongshu feedback CTA for post-launch validation.

## Next Shipping Step

Deploy the PWA to a public HTTPS URL, then test Add to Home Screen on iPhone Safari and Android Chrome.
