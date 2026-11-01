#!/bin/bash
if [ -z "$1" ] || [ -z "$2" ]; then echo "Usage: bash newpost.sh <filename> <title>"; exit 1; fi
DATE=$(date +"%b %d %Y")
cat <<EOF > "src/content/blog/$1.mdx"
---
title: "$2"
description: "ここに記事の説明文を入力してください。"
pubDate: "$DATE"
heroImage: "../../assets/default.jpg"
---

import AffiliateCard from "../../components/AffiliateCard.astro";
import RelatedArticle from "../../components/RelatedArticle.astro";

## はじめに

ここに本文を書きます。

## あわせて読みたい

<RelatedArticle url="/blog/amazfit-trex2-bumper/" image="/images/amazfit-trex2-bumper-card.jpg" title="Amazfit T-Rex 2にAmazonのバンパーカバーを装着レビュー" />
EOF
echo "Created: src/content/blog/$1.mdx"
