#!/bin/bash
# 로턴 블로그 자동 Google Drive 동기화

SOURCE="/Users/roturnjarvis/.openclaw/workspace/business/roturn/blog/"
DEST="$HOME/Google Drive/내 드라이브/로턴 블로그/"

# rsync로 양방향 동기화
rsync -av --delete "$SOURCE" "$DEST"

echo "[$(date)] 로턴 블로그 동기화 완료"
