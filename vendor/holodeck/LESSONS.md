# Lessons for Holodeck

What building the Nashville Symphony 990 explorer taught, written so it applies to any corpus. Each is something that went wrong or nearly did.

**1. Never show noise.** Identical lines repeated once per document, debug counters ("91 disputed, in the replay"), and clouds of junk names made the "Added" card unreadable. Collapse identical messages to one with a count; keep internals (Fort flags, replay counts) in their own views; cap or drop name clouds. Check every copy of Holodeck, not only the one being edited.

**2. A silent failure is a bug that ships.** `.catch(() => {})` around IndexedDB writes hid that the `blobs` store was never created: `purgeLegacyHistory()` opened `fold-explorer` at version 1 first and left it empty, so no PDF or page was ever stored for any first-time visitor. Log failed saves. When two code paths open one database, both must create the schema, neither should pin a version, and every connection should close on `versionchange` so a repair can run.

**3. A source must be viewable as published, and clickable there.** Derived text is not the source. Keep the original (the PDF) and show it; make names, figures and dates clickable on the page itself. A scan has no text layer, so keep the OCR *word boxes* and draw them as an invisible layer; text-only OCR throws away the position that grounding needs.

**4. Offsets must come from one place.** The renderer counts each text item as length + 1 and each page as + 1. The loader builds the document text by the same rule from the same word list, so marks line up. If the derivation changes (new OCR), old saved text no longer matches: mark the new version and replace the old copy.

**5. Addresses and furniture are not content.** Path pieces of a URL became names ("EO"), dates and figures, and "- item" lines were glued into one statement. Mask URLs (same length, so offsets hold) before reading names, dates and figures; treat a list marker as a new line. Form labels ("Part I S", "Ye", "Sa") still pollute names: prose rules do not fit forms.

**6. Persisted browser state outlives the code.** Stale copies, duplicates under an older URL, and documents saved without their bytes all appeared after changes. Loaders must be idempotent: key by stable identity (title or manifest entry, not only URL), keep one copy, and repair missing blobs instead of skipping a document because it already exists.

**7. Test both ways, and on the live URL.** A clean profile and a stale one fail differently; GitHub Pages caches, so add a cache-buster and confirm the served file has your change. A written fix is not a verified fix: say which is which.

**8. Reuse the existing mechanism.** The record-type chips flip `offDocs`, the switch "Choose sources" already uses, so one click narrows every view. New filter plumbing per view would have missed most of them.

**9. Say where data came from.** `filings/manifest.csv` records IRS scan vs ProPublica render of the e-file vs e-file XML. OCR can misread a figure; say so on the source, and cross-check against structured data when it exists (the e-file XML matched the CSV to the dollar).

**10. Big derived files cost every deploy.** 35 MB of OCR word boxes made each Pages build take minutes. Generate sidecars deterministically, keep them beside their source, and consider a release asset or LFS before adding more.

**Known gaps:** no chart or table generator is wired into the UI (the-fold's `chartFrom`/`tables.js` and eoreader7's `measure.js` exist); `findFigures` drops bare numbers; Connections links names only; topic discovery names form text.
