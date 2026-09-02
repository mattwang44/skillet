# Confluence API editing — traps that survive PUT 200

Applies when creating or editing Confluence pages programmatically (REST API,
storage format). Every rule below was learned from a real silent corruption.

## Storage-format surgery

- **No length-changing replacement after computing offsets.** Do ALL string
  replacements first, THEN compute splice offsets. Reversed order cuts inside
  a tag.
- **PUT 200 ≠ content landed.** Malformed XML is silently stripped by
  Confluence — the version is still created, the section is just gone.
  - Before PUT: validate well-formedness with an XML parser (e.g. Python
    `xml.parsers.expat`). When shimming entities to make the fragment
    parseable, the shim replacement text must not contain `<` (e.g. map
    `&le;` to the harmless text `le`, never to `<=`).
  - After PUT: fetch `body-format=export_view` and compare the rendered
    heading list and key phrases. Render-level verification is the only gate
    that catches server-side sanitization.
- **Positional extraction needs a content-signature assert.** "The first
  `<table>`" style extraction must assert the fragment contains an expected
  keyword before acting on it — otherwise you operate on the wrong element.
- **Concurrent editing race.** A user's open editor autosaves over API writes
  (and vice versa). Before every edit: fetch the latest version, diff, rebase
  your change on top of the user's wording. After writing, tell the user to
  close stale editor tabs before reopening.
- **Preserve `ac:inline-comment-marker` elements.** Editing the text inside
  the marker keeps the comment thread; deleting the marker orphans it.

## Links

- `ri:page` resolves by exact content-title match. If your output layer folds
  full-width punctuation (see zh-tw layer), the stored title may differ from
  what you sent — after creating a page, read the actual title bytes back via
  API and build links from the read-back value.
- Em-dashes in storage attributes are stored as the `&mdash;` entity — match
  and replace in entity form.
- An unresolvable `ri:page` link gets fossilized into a `createpage` URL the
  moment a user opens the page in the editor (clicking it then creates an
  empty page). Fix broken links immediately; if an edit session already
  happened, also purge `linkCreation=true` residue.
- **Verify after every upload**: fetch `body-format=export_view` and grep for
  `createpage`. Storage that looks legal does not mean the renderer resolved
  it; this is the only check that catches a broken link before a user does.
