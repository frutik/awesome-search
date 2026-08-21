#!/usr/bin/env bash
set -e

TARGET_DIR="${1:-$HOME/.claude/skills}"
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/claude-skills"

echo "Symlinking skills into $TARGET_DIR"

mkdir -p "$TARGET_DIR"

for d in "$SRC_DIR"/*/; do
  name="$(basename "$d")"
  rm -rf "$TARGET_DIR/$name"
  ln -s "$d" "$TARGET_DIR/$name"
  echo "linked $name"
done

echo "Done."
