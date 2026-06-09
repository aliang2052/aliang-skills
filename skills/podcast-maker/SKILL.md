---
name: podcast-maker
description: 多人对话脚本转语音播客：为不同角色分配音色，逐句生成后用 ffmpeg 拼接成完整音频。
---

# 多人对话播客制作 Skill

## 触发词

当用户提供多角色对话脚本、播客剧本、访谈内容，并要求"做成声音"、"制作播客"、"配音"时使用。

## 工作流

### 第一步：分析对话，分配音色

1. 识别对话中的角色数量和各自特点（性格、年龄、语气）
2. 列出可用音色：

```bash
bl speech synthesize --list-voices --model cosyvoice-v3-flash
```

3. 为每个角色匹配合适的音色：

| 角色类型 | 推荐音色 | 说明 |
|----------|---------|------|
| 活泼女性 | `longanhuan` | 欢脱元气女 |
| 沉稳女性 | `longxiaoxia_v3` | 沉稳权威女 |
| 知性女性 | `longanwen_v3` | 优雅知性女 |
| 磁性男性 | `longtian_v3` | 磁性理智男 |
| 温暖男性 | `longze_v3` | 温暖元气男 |
| 青年男性 | `longcheng_v3` | 智慧青年男 |

4. 向用户展示音色方案，确认后继续。

### 第二步：逐句生成语音

创建临时目录存放分句音频：

```bash
mkdir -p {输出目录}/{对话标题}_语音
```

按对话顺序，为每句生成音频。阿琳用 `longanhuan`、老陈用 `longtian_v3` 举例：

```bash
# 阿琳第1句
bl speech synthesize \
  --text "好了，咱今天就唠唠——AI 这么猛，到底还需要什么样的人才？" \
  --voice longanhuan \
  --out "{输出目录}/{对话标题}_语音/阿琳_01.mp3"

# 老陈第1句
bl speech synthesize \
  --text "我觉得是 T 字型的人。" \
  --voice longtian_v3 \
  --out "{输出目录}/{对话标题}_语音/老陈_01.mp3"
```

继续为所有对话逐句生成。命名格式：`{角色名}_{序号}.mp3`

**注意：**
- 使用 `--model cosyvoice-v3-flash`（系统音色默认，可不写）
- 如需调整语速/语调，添加 `--rate` / `--pitch` 参数

### 第三步：创建 ffmpeg 拼接列表

在语音目录下创建 `concat_list.txt`，按对话顺序排列：

```
file '阿琳_01.mp3'
file '老陈_01.mp3'
file '阿琳_02.mp3'
file '老陈_02.mp3'
...
```

### 第四步：拼接为完整音频

**关键发现：Bailian TTS 虽然输出 `.mp3` 扩展名，实际格式是 WAV（PCM）。** 因此拼接时必须转码：

```bash
ffmpeg -y -f concat -safe 0 -i {输出目录}/{对话标题}_语音/concat_list.txt \
  -c:a libmp3lame -b:a 192k \
  {输出目录}/{对话标题}_完整版.mp3
```

- `-y`：自动覆盖已存在文件
- `-c:a libmp3lame`：转码为真 MP3
- `-b:a 192k`：192kbps 音质

### 第五步：清理与报告

1. 删除临时 `concat_list.txt`
2. 向用户报告：
   - 完整音频路径和时长
   - 分句音频目录位置
   - 使用的音色方案

## 输出示例

```
✅ 播客制作完成！

完整音频：输出/T型人才对话_完整版.mp3
  - 时长：68秒
  - 格式：MP3, 192kbps, 24kHz
  - 大小：1.3MB

音色方案：
  阿琳 → longanhuan（欢脱元气女）
  老陈 → longtian_v3（磁性理智男）

分句音频：输出/T型人才对话_语音/（13个文件）
```

## 进阶：添加片头/片尾音效

如果需要添加背景音乐或音效：

```bash
# 片头音频 + 完整对话拼接
ffmpeg -y -f concat -safe 0 \
  -i <(printf "file 'intro.mp3'\nfile '完整版.mp3'\nfile 'outro.mp3'\n") \
  -c:a libmp3lame -b:a 192k \
  {输出目录}/{对话标题}_带片头.mp3
```

## 注意事项

- Bailian TTS 不支持在同一条命令中切换音色，必须逐句生成
- 如果对话很长（>20句），可并行生成以提高效率
- 使用 `cosyvoice-v3.5-flash` 模型时（克隆音色），命令中的 `--model` 参数必须显式指定
