# aliang-shortvideo · 短剧全流程制作

<p align="center">
  <img src="../../assets/aliang-shortvideo-1.gif" width="240" alt="短剧 demo：末日清道夫" />
  &nbsp;&nbsp;
  <img src="../../assets/aliang-shortvideo-2.gif" width="240" alt="短剧 demo：原子天堂" />
</p>

## 干什么

把**一句话灵感**逐步做成可拍/可播的短剧，五阶段流水线：

```
① 剧情大纲 → ② 分集剧本(台词) → ③ 分镜表 → ④ 批量出图 → ⑤ 图生视频(成片)
```

- 支持多题材：草根逆袭 / 复仇打脸 / 都市甜宠 / 悬疑反转 / 家庭伦理 / 古装重生 / 战神赘婿 / 搞笑沙雕
- 支持竖版 9:16、按单镜指定时长（5s/10s/15s）
- 22 种画风预设，可上传参考图迁移画风
- 每阶段产出后暂停，等你确认再继续

## 如何安装

需先安装百炼 CLI（见[仓库根 README](../../README.md#-前置依赖安装百炼-cli)），然后：

```bash
cp -R aliang-shortvideo ~/.claude/skills/
```

## 如何使用

对你的 AI 助手直接说，例如：

```
做个短剧，灵感是「外卖小哥其实是隐藏的修仙者」，悬疑反转，竖版 30 秒
```

AI 会带你走完大纲→剧本→分镜→出图，每步停下确认。

> 💰 **费用**：①~④（写作 + 出图）成本低，可放心跑；**⑤ 图生视频较贵，默认只产出 `bl video` 命令、不自动付费生成**，你确认要为某段付费后才真正生成。

## 目录结构

```
aliang-shortvideo/
├── SKILL.md                  # 技能主流程
├── references/
│   ├── genres.md             # 8 大题材爽点库 + 结构模板 + 内容红线
│   ├── styles.md             # 22 种画风预设
│   └── storyboard.md         # 分镜表 / storyboard.json 结构规范
└── scripts/
    ├── pick_beats.py         # 按题材随机抽爽点
    └── gen_images.py         # 读 storyboard.json 批量出图
```
