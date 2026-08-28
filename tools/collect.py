#!/usr/bin/env python3
"""A federated tick-network node: this repo's own append-only chain, keyed to the
global tick spine at kody-w/dogg.

THEME = "lineage" — a TEMPLATE family chain. It does not observe any live API; it is
a fill-in-the-blank shape for a genealogical thread (birth / vow / death events across
generations), anchored to the spine's tick so a filled-in copy of this node inherits
the same public clock as every other node. Every field that would be a real person's
name, date, or witness ships here as the literal string "PLACEHOLDER" — see README.md
for why real lineages are never meant to live in this public repo.

Every run reads the spine's current tick anchor and appends one frame of the template
under that tick — one frame per observed tick, same as every other node. Frames verify
with the reference implementation (tools/rapp.py, from kody-w/rapp-1); CI re-verifies
the whole chain on every push.
"""
import json, sys, pathlib, datetime, urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import rapp as R
import chainio

ROOT = pathlib.Path(__file__).resolve().parent.parent
SPINE_HEAD = "https://raw.githubusercontent.com/kody-w/dogg/main/ticks/HEAD.json"
TIMEOUT = 8

# ---- edit these three for your node -------------------------------------------------
THEME = "lineage"                                 # also the data directory name
STREAM = "lineage:@kody-w/dogg-lineage"           # your stream id (your repo, your name)
# This node has no external SOURCES: the template is fixed content, not fetched facts.
# rapp/1 canonical hashing forbids floats: numeric facts ride as strings or ints.
# -------------------------------------------------------------------------------------

GENERATIONS = 3
KINDS = ("birth", "vow", "death")


def utc():
    n = datetime.datetime.now(datetime.timezone.utc)
    return n.strftime("%Y-%m-%dT%H:%M:%S.") + f"{n.microsecond // 1000:03d}Z"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": f"tick-node-{THEME}"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read().decode())


def template_events():
    """A clearly FICTIONAL 3-generation family thread. who/when/witness are the
    literal string "PLACEHOLDER" — this repo carries the SHAPE of a lineage, never
    real names, dates, or witnesses. See README.md: real lineages belong in a private
    kit, passed down as the head chant, not committed to a public chain."""
    events = []
    for gen in range(1, GENERATIONS + 1):
        for kind in KINDS:
            events.append({
                "gen": gen,
                "kind": kind,
                "who": "PLACEHOLDER",
                "when": "PLACEHOLDER",
                "witness": "PLACEHOLDER",
            })
    return events


def template_lineage(events):
    return {
        "schema_version": 1,
        "generations": GENERATIONS,
        "members": GENERATIONS,           # one lineal placeholder per generation
        "events": len(events),
        "family_name": "PLACEHOLDER",
        "note": ("TEMPLATE ONLY. Fork this repo, replace every PLACEHOLDER with your "
                 "real family's names/dates/witnesses in a PRIVATE copy, and stop "
                 "pushing to a public remote before you do. See README.md."),
    }


def load_chain(d):
    return chainio.load_chain(d)


def main():
    spine = get(SPINE_HEAD)
    tick_n, tick_hash = spine["count"] - 1, spine["head_frame"]
    d = ROOT / THEME
    d.mkdir(exist_ok=True)
    chain = load_chain(d)
    head = chain[-1] if chain else None
    if head is not None and head["payload"].get("tick") == tick_n:
        print(f"{THEME}: tick {tick_n} already recorded — nothing to do")
        return
    events = template_events()
    payload = {"tick": tick_n, "tick_frame": tick_hash, "spine": "kody-w/dogg",
               "fetched_utc": utc(), THEME: template_lineage(events),
               "events": events, "sources_failed": []}
    if head is None:
        payload["about"] = (
            "A federated node of the global tick network: a TEMPLATE lineage chain, "
            "one frame per observed tick, keyed to the spine's tick anchors so it joins "
            "every other node's data on the same clock. This chain never carries a real "
            "family's data — see README.md.")
    f = R.build_frame(f"{THEME}.snapshot", STREAM, (head["seq"] + 1) if head else 0,
                      utc(), payload, prev=(head["payload_hash"] if head else None))
    ok, step, why = R.verify_frame(f, head=head, stream_id_of_record=STREAM)
    if not ok:
        raise ValueError(f"refusing invalid frame: {step}: {why}")
    chainio.append_frame(d, f, STREAM)
    print(f"{THEME} frame {f['seq']} @ spine tick {tick_n}: "
          f"{payload[THEME]['generations']} generations, {payload[THEME]['events']} events (template)")


if __name__ == "__main__":
    main()
