# 儿童绘本故事生成 Prompt 模板

用 `bl text chat --message "<下面填好的提示词>" --output json` 调用，取 `.choices[0].message.content`。

把 `{THEME}`、`{N}`（段数，默认 6）、`{AGE}`（默认 4-8 岁）替换后使用：

```
你是一位儿童绘本作家。请创作一个温暖、有教育意义的原创儿童绘本故事，主题：{THEME}。要求：

1. 适合 {AGE} 儿童，语言简单生动，有重复的韵律感。
2. 分成 {N} 个段落（场景），每段 2-4 句话。
3. 有 1 个旁白 + 2-3 个有对白的角色。
4. 严格输出 JSON，不要任何额外文字、不要 markdown 代码块：

{
  "title": "故事标题",
  "characters": [{"name":"角色名","role":"narrator|character","trait":"性格一句话"}],
  "segments": [
    {"id":1,"speaker":"narrator 或某角色名","text":"要朗读的文字（旁白叙述或角色台词，纯中文，可含对白）",
     "emotion":"朗读情绪，从下面词表里选","image_prompt":"该段画面描述，含主角/场景/动作/情绪"}
  ]
}

5. segments 必须正好 {N} 段。image_prompt 要具体到能直接画图，且每段都点明主角外形以保证全书形象一致。
6. 【多音色关键】speaker 字段要尽量分配给不同角色，不要每段都填旁白：当一段以某个角色的台词为主时，speaker 就填该角色名（这样配音才会用不同音色）。理想情况下旁白段和各角色段交替出现，至少有 1/3 的段落 speaker 是具体角色而非旁白。纯叙述的段落才填旁白。
7. emotion 只能取以下之一：温柔讲述 / 紧张转为安心 / 害怕发抖 / 坚定鼓励 / 充满希望与力量 / 欢快喜悦 / 兴奋 / 难过低落 / 好奇。
8. 【极重要】JSON 字符串值内部，对白一律使用中文全角引号 " "，绝对禁止使用英文半角双引号，否则 JSON 会损坏。image_prompt 也只用中文，不要出现任何半角双引号。
```

## 解析返回（含容错）

```python
import json
raw = json.load(open("story_raw.json"))               # bl ... --output json 的原始输出
content = raw["choices"][0]["message"]["content"].strip()
if content.startswith("```"):                          # 去掉可能的代码围栏
    content = content.split("\n", 1)[1].rsplit("```", 1)[0]
story = json.loads(content)                            # 若失败，多半是模型用了英文引号→重新生成并强调第7条
json.dump(story, open("story.json", "w"), ensure_ascii=False, indent=2)
```

若 `json.loads` 报 `Expecting ',' delimiter`：几乎都是对白里混入了英文半角引号 `"`，把 prompt 第 7 条再强调一次重新生成即可，不要手工修补。
