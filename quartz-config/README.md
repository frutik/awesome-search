# Quartz config for CI

`.github/workflows/build-and-deploy.yml` scaffolds a fresh `quartz/` checkout
on every run (it's gitignored, not part of this repo — see root `CLAUDE.md`)
at tag `v4.5.2` — the version the published site's footer reports — and
copies two files from here on top of it:

- `quartz.config.ts`
- `quartz.layout.ts`

## Where these came from

The original local `../quartz` checkout no longer exists on this machine and
its config was never committed anywhere. It was reconstructed by cloning
stock `jackyzha0/quartz#v4.5.2`, building it against the real vault content
into a scratch directory, and diffing the output byte-for-byte against the
published `docs/`.

Result: the only actual customizations are in `quartz.config.ts`:

- `pageTitle: "Awesome Search KG"`
- `baseUrl: "frutik.github.io/awesome-search"`

Everything else — theme colors, fonts (Schibsted Grotesk / Source Sans Pro /
IBM Plex Mono), footer links, favicon, og-image, analytics (plausible),
plugin list, and all of `quartz.layout.ts` — matched the stock v4.5.2
defaults exactly (verified via hash/content diff), so both files here are
just the stock template with those two fields changed.

One cosmetic-only mismatch was found and intentionally *not* reproduced: the
old published HTML used a `data-persist="true"` attribute where current
v4.5.2 source emits `spa-preserve` (a SPA-cache-internal attribute, renamed
at some point in Quartz's history). It doesn't affect page behavior — the
component that writes the attribute and the script that reads it always
agree within a single build — so this workflow just uses current v4.5.2
behavior throughout rather than trying to patch it.

If you ever actually customize the site again (new plugin, theme tweak,
comments, etc.), edit the two files in this directory directly — they're
now the source of truth CI builds from.
