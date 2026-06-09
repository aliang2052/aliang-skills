# aliang-skills · 百炼 AI 创作技能包

> 一套基于 **阿里云百炼 CLI（`bl`）** 的 [Claude Code](https://claude.com/claude-code) / Agent Skills 合集。
> 把"做短剧、做电商图、做儿童故事、做有声绘本、做播客、做配音"这些 AIGC 流程，
> 固化成可一句话触发的技能 —— 你只管说要什么，AI 自动走完整流程。

全部技能共用一个底座：阿里云百炼的文生图 / 图生视频 / TTS / 多模态能力。安装一次 `bl`，六个技能全部可用。

---

## 📦 技能一览

| 技能 | 干什么 | 触发词示例 |
|------|--------|-----------|
| [**aliang-shortvideo**](skills/aliang-shortvideo) | 一句话灵感 → 短剧成片：大纲→剧本→分镜→批量出图→图生视频 | "做个短剧""把这个点子做成短剧" |
| [**aliang-product-detail-photos**](skills/aliang-product-detail-photos) | 产品图去背景 + 生成多角度/多场景电商详情图 | "做商品详情图""电商主图""去掉背景" |
| [**aliang-kids-story-maker**](skills/aliang-kids-story-maker) | 按年龄/时长生成儿童故事，并配音 + 配插图 | "制作儿童故事""睡前故事" |
| [**aliang-picturebook-audiobook**](skills/aliang-picturebook-audiobook) | 故事主题 → 有声绘本：多音色配音 + 统一画风配图 + 网页/视频/音频 | "做有声绘本""把故事做成有声书" |
| [**aliang-podcast-maker**](skills/aliang-podcast-maker) | 多人对话脚本 → 分角色配音 → ffmpeg 拼成完整播客 | "把这段对话做成播客""配音" |
| [**aliang-bailian-voice-clone**](skills/aliang-bailian-voice-clone) | 用百炼克隆音色（CosyVoice v3.5）合成语音 | "克隆声音合成""TTS" |

> 💡 每个技能目录下都有独立的 README，写清了它的功能、安装和用法。

---

## 🔧 前置依赖：安装百炼 CLI

所有技能都依赖阿里云百炼命令行工具 `bl`。

```bash
# 1. 安装 CLI（需要 Node.js）
npm install -g bailian-cli

# 2. 配置 API Key（在百炼控制台获取：https://bailian.console.aliyun.com）
export DASHSCOPE_API_KEY=sk-你的key
#   或者
bl auth login --api-key sk-你的key

# 3. 验证
bl auth status
```

部分技能用到音频合并 / 视频导出，需要额外装 [`ffmpeg`](https://ffmpeg.org/)：

```bash
brew install ffmpeg     # macOS
```

---

## 📥 安装技能

技能就是一个个目录，放进 Claude Code 的技能目录即可被自动识别。

### 方式一：全部安装（推荐）

```bash
git clone https://github.com/aliang2052/aliang-skills.git
cp -R aliang-skills/skills/* ~/.claude/skills/
```

### 方式二：只装某一个

```bash
# 例：只要短剧技能
cp -R aliang-skills/skills/aliang-shortvideo ~/.claude/skills/
```

装好后，在 Claude Code 里输入 `/` 或直接说出触发词，对应技能就会被调用。

> 其他支持 Agent Skills 规范的客户端（如 `.qwen/skills`、`.agents/skills`），把目录放到对应位置同样可用。

---

## 🚀 如何使用

安装后**无需记命令**，直接用自然语言对 Claude Code 说话即可。例如：

```
做个短剧，灵感是「外卖小哥其实是隐藏的修仙者」，竖版 30 秒
```
```
帮我把这张产品图（./保温杯.jpg）做成 5 张电商详情图，简约风
```
```
给 5 岁的孩子做一个 3 分钟的睡前故事，要配音和插图
```

AI 会按技能内置的流程分步执行，关键节点暂停等你确认。

---

## 💰 费用提示

- 文生图 / TTS 价格较低；**图生视频较贵**。
- `aliang-shortvideo` 的"图生视频"阶段默认**只产出命令、不自动付费生成**，需你显式确认要为哪段付费后才会真正生成。请放心试用前面的免费/低价阶段。
- 各模型实时单价以[阿里云百炼官方定价页](https://help.aliyun.com/zh/model-studio/model-pricing)为准（文生图 / TTS / 视频生成等分模型计价）。

---

## ⚠️ 关于克隆音色

`aliang-bailian-voice-clone` 用到的克隆音色 ID 是**个人百炼账号私有资源，无法共享**。
仓库里相关 ID 已替换为占位符（`cosyvoice-v3.5-flash-YOUR_xxx_VOICE_ID`）。
使用前请在[百炼控制台](https://bailian.console.aliyun.com/)创建你自己的克隆音色，再把占位符换成你的真实 ID。
普通系统音色（如 `longanwen_v3` 等）无需克隆，开箱即用。

---

## License

[MIT](LICENSE)
