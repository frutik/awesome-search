set -e
#sh build-web.sh
#git add obsidian/ docs/
git add obsidian/ mails/ drafts/
# tolerate an empty commit so an already-committed backlog still gets pushed
git commit -a -m wip || true
git push
