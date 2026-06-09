---
name: aliang-product-detail-photos
description: 高质量商品详情图生成。将产品图片去背景，根据产品特点生成多角度、多场景商品详情图。
---

# 商品详情图生成器

> **依赖：** 阿里云百炼 CLI (`bl`)，需配置 `DASHSCOPE_API_KEY`。

## 触发词

当用户提到"商品详情图"、"电商主图"、"产品图"、"去掉背景"、"做产品宣传图"时使用。

## 工作流

### 第一步：确认需求

向用户确认：
- **图片数量** — 需要几张（用户必须指定）
- **产品图片** — 原图路径
- **图片比例** — 1:1 方图 / 3:4 竖图 / 16:9 横图（默认 3:4）
- **风格偏好** — 简约 / 温馨 / 自然 / 科技感 等（默认简约）
- **输出目录** — 默认 `输出/`

### 第二步：产品理解与场景规划

用 `bl text chat` 分析产品，规划拍摄方案：

```bash
bl text chat --message "你是一位专业的电商摄影师。请分析产品图片，规划商品详情图拍摄方案。

产品图片：{product_image_path}
需要生成：{n}张，风格：{style}

请输出规划表，将{n}张图片拆分为「角度」+「场景」的组合，每张说明展示角度、场景背景、构图要点、光线氛围。"
```

向用户展示规划表，等待确认。

### 第三步：去除产品背景

```bash
bl image edit \
  --image {product_image_path} \
  --prompt "Remove the background completely, keep only the product itself with clean edges, output on solid white background" \
  --model qwen-image-2.0-pro \
  --out-dir {output_dir} \
  --out-prefix "product_no_bg"
```

### 第四步：逐张生成详情图

对每张图，用去背景后的产品图放入场景（效果比纯文本生成更准确）：

```bash
bl image edit \
  --image {product_no_bg_path} \
  --prompt "Place this product naturally in {scene_description}, {composition_details}, {lighting_details}, professional product photography, sharp focus, no text, no watermark, no logo" \
  --model qwen-image-2.0-pro \
  --size "{ratio}" \
  --out-dir {output_dir} \
  --out-prefix "product_{index}"
```

场景建议：
- 食品/饮料 → 餐桌、厨房、自然光线
- 服装/鞋帽 → 模特穿搭、纯色背景、生活场景
- 数码产品 → 简约科技风、办公桌面
- 儿童用品 → 温馨家居、明亮色彩
- 户外用品 → 自然风光、使用场景

### 第五步：整理输出

输出报告：

```
✅ 商品详情图生成完成

📁 输出目录：{output_dir}/{product_name}/
📊 共生成 {n} 张图片：
  - product_no_bg.png — 去背景产品图
  - product_01.png — [角度] + [场景]
  ...
```

## 关键命令

| 操作 | 命令 |
|------|------|
| 去背景 | `bl image edit --image <path> --prompt "Remove background..." --model qwen-image-2.0-pro` |
| 产品入场景 | `bl image edit --image <no_bg_path> --prompt "Place in {scene}..." --model qwen-image-2.0-pro --size "1:1"` |
| 纯文本生成 | `bl image generate --prompt "<description>" --model qwen-image-2.0-pro --size "3:4"` |
| 产品分析 | `bl text chat --message "<analysis prompt>"` |
