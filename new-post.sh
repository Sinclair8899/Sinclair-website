#!/bin/bash
if [ -z "$1" ]; then
    echo "用法: ./new-post.sh \"文章标题\""
    exit 1
fi
DATE=$(date +%Y-%m-%d)
FILENAME="content/blog/${DATE}-article.md"
cat > "$FILENAME" << INNER
---
title: "$1"
date: ${DATE}T10:00:00+08:00
draft: false
---

# $1

开始写作...

INNER
echo "✅ 已创建: $FILENAME"
echo "编辑: open $FILENAME"
