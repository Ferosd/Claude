"""Replace the inline-SVG data-URI favicon with the real file-based set.

Every live page currently has a single line:
    <link rel="icon" href="data:image/svg+xml,...C...">
We swap it for proper PNG/ICO links (incl. apple-touch-icon). Falls back to
inserting before </head> if no such line exists. Skips backups/ and .audit/.
Idempotent: skips pages that already reference the real set.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {"backups", ".audit", ".git", "node_modules", "vendor"}

LINKS = (
    '    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">\n'
    '    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">\n'
    '    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">\n'
    '    <link rel="shortcut icon" href="/favicon.ico">\n'
)

INLINE_MARK = 'rel="icon" href="data:image/svg'
REAL_MARK = "favicon-32x32.png"


def iter_html():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            if f.endswith(".html"):
                yield os.path.join(dirpath, f)


def main():
    replaced, inserted, skipped = [], [], []
    for path in iter_html():
        with open(path, encoding="utf-8") as fh:
            html = fh.read()
        rel = os.path.relpath(path, ROOT)

        if REAL_MARK in html:
            skipped.append(rel + " (already real set)")
            continue

        lines = html.split("\n")
        out, done = [], False
        for line in lines:
            if not done and INLINE_MARK in line:
                # preserve the line's leading indentation
                indent = line[: len(line) - len(line.lstrip())]
                block = "".join(indent + l.lstrip() + "\n"
                                for l in LINKS.rstrip("\n").split("\n"))
                out.append(block.rstrip("\n"))
                done = True
            else:
                out.append(line)
        if done:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write("\n".join(out))
            replaced.append(rel)
            continue

        # fallback: insert before </head>
        idx = html.lower().rfind("</head>")
        if idx == -1:
            skipped.append(rel + " (no inline icon, no </head>)")
            continue
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html[:idx] + LINKS + html[idx:])
        inserted.append(rel)

    print(f"Replaced inline-SVG favicon in {len(replaced)} files.")
    print(f"Inserted (fallback) in {len(inserted)} files.")
    if inserted:
        for r in inserted:
            print("  +", r)
    if skipped:
        print(f"Skipped {len(skipped)}:")
        for r in skipped:
            print("  -", r)


if __name__ == "__main__":
    main()
