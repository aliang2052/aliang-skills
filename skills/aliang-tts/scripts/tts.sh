#!/bin/bash
# 阿亮 TTS 合成脚本
# 用法: tts.sh "播报文本" [输出文件名] [voice_id]
# 默认使用科技风音色，1.2倍速

VOICE_TECH="cosyvoice-v3.5-flash-YOUR_TECH_VOICE_ID"
VOICE_WARM="cosyvoice-v3.5-flash-YOUR_WARM_VOICE_ID"

TEXT="${1}"
OUTPUT_NAME="${2}"
VOICE="${3:-$VOICE_TECH}"

# 项目根目录（本脚本在 .qwen/skills/aliang-tts/scripts/ 下）
OUTPUT_DIR="声音/阿亮口播输出"

# 生成默认文件名：内容总结_年月日时分秒
if [ -z "$OUTPUT_NAME" ]; then
  # 提取文本前 15 个字符作为总结，去除空格和换行
  SUMMARY=$(echo "$TEXT" | sed 's/[[:space:]]//g' | LANG=zh_CN.UTF-8 cut -c1-15)
  TIMESTAMP=$(date +%Y%m%d%H%M%S)
  OUTPUT_NAME="${SUMMARY}_${TIMESTAMP}.mp3"
fi

# 确保输出目录存在
mkdir -p "$OUTPUT_DIR"

OUTPUT_PATH="$OUTPUT_DIR/$OUTPUT_NAME"

echo "🎙️ 开始合成..."
echo "音色: $VOICE"
echo "输出: $OUTPUT_PATH"
echo "---"

bl speech synthesize \
  --text "$TEXT" \
  --model cosyvoice-v3.5-flash \
  --voice "$VOICE" \
  --out "$OUTPUT_PATH" \
  --language zh \
  --rate 1.2 \
  2>&1

if [ $? -eq 0 ]; then
  echo "---"
  echo "✅ 合成完成: $OUTPUT_PATH"
else
  echo "❌ 合成失败"
  exit 1
fi
