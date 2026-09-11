# AI Data+ · project wiki

The public face of the programme: what AI Data+ is, how it is built, who signs what,
when a person has to look at a submission — and, for whoever has to run it, a developer
portal with the flywheel manual and the model endpoints.

Published with GitHub Pages. Every page is **one self-contained HTML file** — no CDN,
no external font, no build step. Open one off a USB stick and it still works, which is
why the pages are the way they are.

## The story

| Page | What it answers |
|---|---|
| `index.html` | **Overview** — the landing page. One submission, scrolled from the pack that arrives to the data the underwriter reads. Ends with the contents of this wiki. |
| `flow.html` | **How it works** — the whole programme in four pictures, then the process stage by stage. Three views (at a glance / module overview / full detail), printable. |
| `lifecycle.html` | **Step by step** — the seven steps of one submission: who runs each, who signs it off, and every outcome a step can have. |
| `rules.html` | **The rules** — how the machine decides what each file is, arranged by what a rule actually reads: the folder, the file name, the file type, the content. |
| `gate.html` | **RAG Gate** — red / amber / green, and every rule behind the colour, in plain words beside its rule name in `triage/gate.py`. |

## The developer portal

| Page | What it is |
|---|---|
| `developer.html` | The portal itself, in three parts: General (LLM API), Submission Agent (flywheel manual, the code), Facts Agent (to be filled). |
| `manual.html` | The flywheel manual. Built from `validate/manual/` in the code repo by `build.py`, which inlines every screenshot; that is why it is one 3.4 MB file. To refresh it, rebuild there and copy the result over this file. |
| `llm-api.html` | The two in-house OpenAI-compatible hosts: model ids, the reasoning switch each expects, and the gotchas. **Neither the API keys nor the addresses are on this page** — a host reads `<chat-host>` or `<vision-host>`, a key reads "see the internal note". The real values live together in the internal API note on the project share and in each stage's gitignored config. A host and port are credential-class here, not documentation: published together with "traffic is HTTP, not HTTPS" they are a recipe for lifting a key off the wire. Keep both off this page. |

### The password on it

The three developer pages ask for a password before they show anything. The password is
not written down anywhere in this repository — ask the project team, and pass it around
out of band.
The page starts with `class="wk-locked"` on `<html>`, so
a browser with JavaScript off shows the lock and nothing else; unlocking is remembered
in `sessionStorage` for that tab, and covers all three pages at once.

The password itself is **not** in the files. What is stored is a digest: sha256 of
salt + password, re-hashed with the salt 20,000 times. The page hashes what is typed the
same way and compares — so reading the source gives you a hash, not a password.

**Be honest about what this is.** It is a lock on a door, so a link that reaches the
wrong person does not open: it is not encryption. The page body is still in the file, and
anyone who reads the source can read it. That is why the real secrets stay out of these
pages — `llm-api.html` says "see the internal note" wherever a key belongs, and *that* is
the protection.

```
python tools/dev_gate.py --password <the password>      # re-apply, or change it
python tools/wiki_chrome.py                             # re-apply the nav bar + the page kit
```

Both scripts write the block into every page they cover, which is how the copies stay
identical. The password is an argument and is in neither script — a password in a
committed file is a published password. Run either one and commit the pages it rewrites.

### Kept out of search

Every page carries `<meta name="robots" content="noindex, nofollow, noarchive, nosnippet,
noimageindex">` directly under its `viewport` line, and `robots.txt` deliberately leaves
crawling open so that tag can be read. A `Disallow: /` would look stronger and be weaker:
the crawler would never fetch the page, never see the `noindex`, and a URL linked from
somewhere else could still be listed. Keep the tag on any page added later — it is the
whole mechanism.

This makes the site unlisted, not private. Anyone with the link still opens it, and a
crawler that ignores the tag still reads it, which is why the password gate above and the
rule about keeping real secrets off these pages both still apply. If the GitHub repository
is public, the same HTML is readable — and indexable — on github.com regardless of what
these pages say; making the repository private while leaving Pages published is the switch
for that.

## Four things to keep in step

- **The chrome.** Each page carries an identical copy of it, between
  `<!-- wiki chrome -->` and `<!-- /wiki chrome -->` right after `<body>`, with the
  password gate in the same shape below it on the three developer pages. The chrome
  owns the colour tokens, the sticky nav, the language switch, and the skip link.
  Edit `tools/wiki_chrome.py` and re-run it rather than editing seven copies by hand;
  the manual and the API reference both mark *Developer portal* as their current page.
  Two of the five pages do not sit beside the others: `rules.html` and `gate.html` are
  both about what the Submission Agent decides, so they hang under a **Submission
  Agent** dropdown. The grouping is the `MENU` tuple in the script - moving a page in
  or out of it is an edit there and a re-run, never a hand-edit of eight bars. The
  panel hangs off the bar rather than off the strip the button sits in, because that
  strip scrolls sideways on a narrow screen and clips whatever overflows it; its left
  is measured from the button. A browser with no JavaScript gets the two links in
  plain sight instead, out of the `<noscript>` block the same script writes.
- **The page kit.** `index.html` is the reference for how this wiki looks — white ground
  with two soft washes and a dot grid, navy display headings, one warm orange accent,
  14px cards that lift on hover. The kit is that look written down: palette, shadows,
  radii, a type ladder, the page head (`.wkhead`), the *Keep reading* cards and the
  footer. It rides in the same script, between `<!-- wiki page kit -->` and
  `<!-- /wiki page kit -->`, with the cards between `<!-- wiki next -->` and
  `<!-- /wiki next -->`, and it is loaded **after** the chrome so its tokens win over
  whatever a page declared for itself. It goes on `flow.html`, `lifecycle.html`, `rules.html` and
  `gate.html` only: the Overview carries none of it because it *is* the reference and
  declares the same palette for itself, and the developer portal is its own room.
  A page then styles itself out of the kit's tokens — a hard-coded hex on those three
  pages is a defect, not a decision.
- **Both languages.** Every visible string exists in English and Chinese, and the two are
  edited in the same pass. An English change with no Chinese change is how the two
  versions start meaning different things. In the chrome the pair is
  `<span class="wk-en">` / `<span class="wk-zh">`; each page's own body text uses that
  page's existing convention. The one deliberate exception is `llm-api.html`, a developer
  cheat sheet kept in English, which says so on the page. Switching language happens
  in the nav bar, once, for the whole wiki.
- **The manual is a copy.** It is generated in the code repository, not edited here — so
  copying a fresh build over `manual.html` wipes the chrome, the password gate and the
  `noindex` tag, and that is exactly how it once ended up the only ungated, indexable
  page on the site. **Re-run both scripts after every copy**, in this order:
  `python tools/wiki_chrome.py` then `python tools/dev_gate.py --password <the password>`.
  `wiki_chrome.py` restores the `noindex` tag on any page missing it, so that half can no
  longer be forgotten; the gate still needs the password, which is why it is a second step.

The language choice is shared across the wiki through `localStorage["aidp.lang"]` and
the switch in the nav bar, so a reader who switches to Chinese stays in Chinese as
they move between pages. Pages that have extra work on a switch (rebuilding a
chart, rewriting a title) listen for `aidp:lang`. The illustrated manual still
writes `flywheel-manual-lang` as well, so a rebuild of that file does not forget
the last choice, but it follows the wiki bar.

## How these pages are written

Four tests, applied line by line. They were set over four rounds on
`rules.html`, and every round's correction turned out to be the same one: the
page kept talking about itself instead of about the system.

- **Every line is a fact or an action.** A sentence either states something true
  about the system, or tells the reader what they can do. Everything else goes —
  sentences explaining the page to its own reader, design rationale, the history
  of a rule, the evidence a decision rested on, and anything the table below it
  already shows. Two that were cut by name: 「规则可依据的只有这些。各有所长，也各
  有盲区。」 states the obvious, and 「读了哪几样，最能说明这条规则靠不靠得住。」
  means nothing to anybody who has not already read the code.
- **Name the thing, never a metaphor for it.** 材料包, 信封 and 清单 all went:
  a reader who does not already know the system cannot decode any of them. Write
  邮件、压缩包、图片、简报. Where a rule matches on literal names, print the names —
  `Slip & End't` and `U W Information`, not 「提交材料的位置」. A label that needs a
  glossary is the wrong label.
- **The Chinese is written, not translated.** The failure mode is 翻译腔: English
  em-dash asides carried straight across, 会 / 被 / 它 kept where Chinese drops
  them, 「如果⋯⋯就会被⋯⋯」 for 若⋯⋯则, and translated metaphors. Break the aside
  into its own sentence or use a colon; drop every pronoun the sentence can carry
  without. Both languages are edited in the same pass — see *Both languages*
  above, which is the mechanical half of the same rule.
- **Colour encodes the reader's question, not the system's taxonomy.** The answer
  badge on `rules.html` had six colours for six roles; the reader's question is
  whether the file goes downstream, so it has two — green for CORE, neutral for
  every other answer. The same test is why no card carries an edge band and no
  small tag carries a stripe.

`manual.html` is generated in the code repository and is **not** edited to this
standard here — it has its own, stricter one (write so a reviewer can act, never
teach the system), which lives beside its source.
