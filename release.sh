set -e
sh build-web.sh
git add obsidian/ docs/
# tolerate an empty commit so an already-committed backlog still gets pushed
git commit -a -m wip || true
git push
