# 配音音色参考（cosyvoice-v3-flash 系统音色）

完整列表用 `bl speech synthesize --list-voices --model cosyvoice-v3-flash` 查。下面是适合儿童绘本的精选。

## 智能选角（默认行为）

脚本**不再死板轮流分配**，而是按角色的性别 / 年龄 / 性格自动选角：
1. 若 `story.json` 某段或某角色显式写了 `"voice":"<id>"` → 直接用它（最高优先级）。
2. 否则调用 `bl text chat` 当「选角导演」，从内置音色库（`VOICE_CATALOG`）里为每个角色挑最贴合的音色——男角配男声、女角配女声、童话中性角色配中性童声、旁白配温暖讲述声。
3. 选角失败时按性别关键词启发式兜底（男→男声池，女→女声池），保证不会出现「男孩配女声」这种错配。

要手动指定，在 `story.json` 的 `characters[].` 或某 `segments[].` 加 `"voice":"<id>"` 即可覆盖。用 `--no-auto-cast` 可关闭 LLM 选角只用启发式。

## 内置音色库（节选，男声/女声/中性）

**男声**：`longniuniu_v3`(阳光男童·小英雄) `longjielidou_v3`(顽皮男童·机灵鬼) `longze_v3`(温暖元气男) `longcheng_v3`(智慧青年男·王子) `longfei_v3`(热血磁性男·勇士) `longtian_v3`(磁性理智男·爸爸/国王) `longlaotie_v3`(东北直率男·丑角)

**女声**：`longhuhu_v3`(天真女童) `longling_v3`(奶声幼龄) `longxian_v3`(豪放假小子) `longhua_v3`(甜美少女/公主) `longanrou_v3`(温柔姐姐/妈妈) `longyan_v3`(温暖旁白) `longwan_v3`(柔声仙女) `longxiaoxia_v3`(沉稳女王/奶奶)

**中性 / 奇幻**：`longshanshan_v3`(戏剧化童声·精灵) `longpaopao_v3`(飞天泡泡音·魔法生物)

## 关键坑（务必遵守）

1. **系统音色不支持 `--instruction`**：加了会报 `428 InvalidParameter`。情绪只能用 `--rate`(0.5-2.0) 和 `--pitch`(0.5-2.0) 表达。build 脚本已内置 emotion→(rate,pitch) 映射。
2. **`--out x.mp3` 实际落盘是 WAV PCM 内容**，所以统一用 `.wav` 扩展名，浏览器/ffmpeg 都能正常读。
3. 多角色靠不同 voice ID 区分，单段如果旁白里夹角色对白，整段用该段 speaker 的音色即可（不做段内切音）。
