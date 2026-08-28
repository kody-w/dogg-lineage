# dogg-lineage — a federated TEMPLATE node of the global tick network

**A fill-in-the-blank shape for a family lineage: birth / vow / death across three generations, one frame per tick — every name, date, and witness in this public repo is the literal string `PLACEHOLDER`.**

This repo keeps its own append-only chain of rapp/1 frames in `lineage/`. Once a day
a GitHub Action reads the current tick anchor from the spine at
[kody-w/dogg](https://github.com/kody-w/dogg) and appends one frame of this node's
template, referencing that tick — so this chain joins every other node's data on the
same clock. Unlike the market/weather/attention nodes on the network, this node has
nothing to *fetch*: it carries no live source, only a fixed shape.

## What it carries

Each frame's `payload.events` is a 9-entry array — three generations, each with a
`birth`, a `vow`, and a `death` — and `payload.lineage` carries the counts
(`generations`, `members`, `events`, `schema_version`). Every `who`, `when`, and
`witness` field is the literal string `"PLACEHOLDER"`. Nothing here is a real person,
a real date, or a real witness — this repo is the shape a lineage takes, not a
lineage.

## Why this exists

A tick-anchored chain is a good structure for a family record: content-addressed,
append-only, hash-chained to every prior generation's entry, and (once signed)
tamper-evident. That is genuinely useful for something that matters offline and across
years — a head chant, a family Bible's flyleaf, an estate binder. It is also exactly
the wrong place to put one in the clear: a public GitHub repo is not where anyone
should commit a real grandmother's name, birth date, and cause of death, keyed to a
public timestamp anyone can query forever.

So this node exists to prove the *shape* works — that a real, private lineage kit
could fork this exact structure, replace every `PLACEHOLDER`, verify with the same
`tools/rapp.py`, and stay off any public remote — without ever putting real family
data where this repo puts its placeholders.

**Real lineages belong in a private kit** — a private repo with no remote, or fully
offline (a folder, a printed binder, a chant passed down by voice at the next
gathering) — never in `kody-w/dogg-lineage` or any other public fork of it.

## Precision and limits

- **Precision**: none, by design. Every fact-shaped field is a placeholder string, not
  a value. The only real data in this chain is the tick anchor itself (which
  generation of the *spine*, not the family, each frame was minted under) and the
  frame's own timestamps and hashes.
- **Limits**: this is a template, not a genealogy tool. It does not validate dates,
  relationships, or witness identity; it does not deduplicate people across
  generations; it assumes a simple three-generation lineal thread (one member per
  generation), which most real families are not. A real kit built from this shape
  would need its own richer schema (multiple children, marriages, adoptions) before
  it could hold an actual family — this repo only proves the chain mechanics.

**Verify it yourself:** `python3 tools/verify_thread.py` re-checks every frame with the
reference implementation from [kody-w/rapp-1](https://github.com/kody-w/rapp-1). CI runs
the same oracle on every push.

**Start your own node:** fork this repo, edit `THEME` / `STREAM` at the top of
`tools/collect.py` (keyless https APIs, small factual payloads, numbers as strings —
or, like this one, no live source at all), and enable the scheduled workflow. Your
chain, your outlook, same clock — announce it on the spine's registry
([kody-w/dogg](https://github.com/kody-w/dogg) issues) so agents can find it. If your
node is a real private lineage, do not announce it, and do not fork it onto a public
remote.

## Trust

<!--trust-->
No ratings yet — used this chain? [Rate it](../../issues/new?template=rate.yml): valid ratings publish automatically as verifiable frames.
<!--/trust-->
