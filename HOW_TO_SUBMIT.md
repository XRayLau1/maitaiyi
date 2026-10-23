# 如何提交参赛（手把手）

> 面向第一次用 GitHub 的人。全程约 15 分钟。

---

## 0. 开始前，先确认三件事

| 检查项 | 说明 |
|---|---|
| 有 GitHub 账号 | 没有就去 [github.com](https://github.com) 注册（邮箱要能收信，奖品通知靠它） |
| 项目文件夹位置 | `/Users/raylau/WorkBuddy/2026-10-23-22-32-19/mcd-personality-test` |
| 截止时间 | **2026-10-25 23:59（北京时间）**，定榜 10-26 00:00 |

---

## 1. 创建 Public 仓库

1. 登录 GitHub，点右上角 **「+」→ New repository**。
2. 填写：
   - **Repository name**：`maitaiyi`
   - **Description**：`麦门综合门诊：12 项问诊测出你的麦门体质，出具诊断证明书与 Rp. 处方笺（麦当劳 MCP）`
   - **Public** ← **必须选这个，选 Private 直接失去资格**
   - **不要勾** "Add a README file"（我们自己有，勾了会冲突）
3. 点 **Create repository**。

---

## 2. 上传文件

> ⚠️ **最容易出错的地方：文件必须在仓库根目录，不能多套一层文件夹。**
> 错误：`maitaiyi/mcd-personality-test/README.md`
> 正确：`maitaiyi/README.md`

### 方式 A · 网页拖拽（推荐，不用装任何东西）

1. 打开刚建好的仓库，点页面上的 **"uploading an existing file"**。
2. 打开访达，进入 `mcd-personality-test` 文件夹**内部**。
3. **全选里面的所有内容**（不要选中文件夹本身）：
   - `README.md`、`CONTEST_DECLARATION.md`、`MCP_INTEGRATION.md`
   - `mcp-config.example.json`、`SKILL.md`、`workbuddy.md`
   - `index.html`、`SUBMISSION_CHECKLIST.md`、`HOW_TO_SUBMIT.md`、`.gitignore`
   - `assets/`、`scripts/`、`outputs/` 三个文件夹
4. 全部拖到网页上传区，等进度条走完。
5. 底部填 commit 信息：`feat: 麦太医 · 麦门体质诊断` → 点 **Commit changes**。

> 网页上传支持拖文件夹，`assets`、`scripts`、`outputs` 会自动作为目录上传。

### 方式 B · Git 命令行

```bash
cd /Users/raylau/WorkBuddy/2026-10-23-22-32-19/mcd-personality-test

git init
git add .
git commit -m "feat: 麦太医 · 麦门体质诊断（麦当劳 MCP 参赛作品）"
git branch -M main
git remote add origin https://github.com/你的用户名/maitaiyi.git
git push -u origin main
```

> 第一次 push 会要求登录，按提示用浏览器授权即可。

### 方式 C · GitHub Desktop

下载 [GitHub Desktop](https://desktop.github.com/) → Add Local Repository → 选 `mcd-personality-test` → Publish repository → **取消勾选 "Keep this code private"** → Publish。

---

## 3. 上传后，补全仓库信息

这两项直接影响路人点 Star 的意愿：

1. 仓库首页右上角 **⚙️ Settings 旁的 About** → 点齿轮：
   - **Description**：填一句话介绍（见上方）
   - **Topics**：加 `mcdonalds` `mcp` `skill` `workbuddy` `mcp-server` `personality-test`
   - 勾选 **Use your README.md**（如果有 Website 一栏可留空）
2. 确认首页能正常显示 banner 图和六种体质图（图片路径是相对路径，正常会自动加载）。

---

## 4. 发报名 Issue（格式最严格的一步）

打开报名页：<https://github.com/M-China/mcd-developer-innovation-challenge/issues/new>

**标题**（直接复制）：

```
麦太医 · 麦门体质诊断
```

**正文**（直接复制，注意：**不要有空行、不要用 Markdown 链接**）：

```
【参赛申请】
项目名称：麦太医 · 麦门体质诊断
项目地址：https://github.com/你的用户名/maitaiyi
项目简介：麦门综合门诊，12 项问诊检测辣度甜度冰爽饱腹分享治愈六维口味基因，结合麦当劳 MCP 真实餐品与营养数据，出具诊断证明书与 Rp. 处方笺
```

### ⚠️ 三个必须遵守的格式要求（官方特别提示）

| 要求 | 错误示范 | 正确做法 |
|---|---|---|
| 标题与正文之间不要空行 | 标题后敲两个回车 | 直接写正文 |
| `【项目简介】`与内容之间不要换行 | `项目简介：`<br>`麦门综合门诊…` | `项目简介：麦门综合门诊…`（同一行） |
| 项目地址不要用 Markdown | `[仓库](https://...)` | 直接贴 `https://...` |

提交后，系统会自动回复一条「报名成功」的通知。**没收到回复就是格式有问题**，按失败原因改完重新提 Issue 即可。

---

## 5. 验证报名成功

| 检查 | 怎么查 |
|---|---|
| Issue 下有成功回复 | 回到你的 Issue 看评论 |
| 项目出现在 Issue 列表 | 活动仓库的 Issues 页能看到 |
| 项目进入排行榜 | `RANKING.md` 里搜你的仓库名（需 Star > 0 才进榜） |

---

## 6. 拉 Star（决定最终名次）

| 目标 | 需要 Star | 能拿到什么 |
|---|---:|---|
| **进前 100** | 约 **36+** | 汉堡回车键玩具 + 程序员徽章 + 3000 WorkBuddy 积分 |
| 进前 50 | 约 **71+** | 同上（名次更靠前） |
| 进前 3 | 900+ | 巨无霸兑换券 20–50 次 + 10240 积分（需强运营，不建议硬冲） |

**三个有效动作：**

1. 把 `assets/web-result.png` 发朋友圈/小红书，配文「我查出了我的麦门体质，你也来挂个号」+ 仓库链接。
2. 发到麦当劳爱好者群、程序员群、V2EX / 即刻。
3. 找 10 个朋友「真的点进去测一遍，再顺手点个 Star」——真实体验后的 Star 最稳。

---

## 7. 常见报名失败原因

| 原因 | 怎么修 |
|---|---|
| 仓库是 Private | Settings → 最下方 Danger Zone → Change visibility → Public |
| 缺 `mcp-config.example.json` | 主 README 的表格里没列，但活动细则**明确要求**，务必上传 |
| `CONTEST_DECLARATION.md` 被改过 | 重新从官方仓库下载原文件覆盖，一个字都不能动 |
| Issue 格式不符 | 检查是否有多余换行、链接是否用了 Markdown |
| 项目没真实使用 MCP | 本项目已在 `MCP_INTEGRATION.md` 说明实际调用的 Tool，并在 `index.html` 中体现营养数据来源 |
| 仓库创建时间不在范围内 | 需在 2025-12-25 ~ 2026-10-25 之间创建（新建的仓库天然满足） |
| 同一账号多个项目 | 只有 Star 最高的那个进榜，其余不计 |

---

## 8. 提交前最后一遍

- [ ] 仓库 Public
- [ ] 6 个必交文件都在**根目录**
- [ ] `CONTEST_DECLARATION.md` 未被修改
- [ ] `mcp-config.example.json` 里没有真实 Token（只有 `${MCD_MCP_TOKEN}`）
- [ ] 首页图片能正常显示
- [ ] Issue 已提交并收到成功回复
- [ ] 已把仓库链接发出去

**做完这些，就等 10-26 00:00 定榜了。**
