set -e
cd quartz && npx quartz build --output ../docs  --directory ../obsidian/vault/Awesome\ Search && cd ..
# Quartz re-emits a note as its same-named folder's index page (Concepts.md ->
# Concepts/index.html) without re-anchoring the links inside it. See the script.
python3 fix-folder-pages.py docs
cp docs/History.html docs/index.html
