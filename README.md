# Zohara OS website

A static site: plain HTML and CSS, no build step, no JavaScript, no external fonts or trackers.

    index.html      the page
    style.css       styles (colours come from the logo: #0B0E14, #E8ECF1, #5FD4D4)
    404.html        not-found page
    assets/logo.svg the Zohara logo (copied from zohara-profile/airootfs/usr/share/pixmaps/zohara-logo.svg)
    assets/img/     screenshots, WebP. Since the 1.1 release they are real captures from the owner's laptop (hero, Store,
                    Settings pages, Start menu); only the Wi-Fi name on settings-home.webp is blurred

Preview locally: `python3 -m http.server 8080` in this folder, then open http://localhost:8080.

## Hosting

The main address is **https://zohara-website.onrender.com/** (Render, static site). Settings used: repository
`zohara-website`, branch `main`, Root Directory empty, Build Command empty, Publish Directory `./`. Every push to
`main` redeploys. `index.html` has a `canonical` link and `og:` URLs pointing at that address; change them if the
address changes (for example when a custom domain is added in Render's settings).

The same repository is also published on GitHub Pages at https://zohaib8090.github.io/zohara-website/ (Settings >
Pages > branch `main`, folder `/`). Nothing on the page depends on the host: all links are relative and
`404.html` is self-contained. Switch Pages off if a second copy is not wanted.

## Keeping it true

- Every claim on the page was checked against the repositories or in the VM. Update the download section when
  a direct ISO link exists, and the requirements table if the README's requirements change.
- Screenshots: retake them when the look changes. Look at every picture before it goes on the page: a capture shows every window of
  the desktop and the Wi-Fi name, device names and Bluetooth devices in Settings. Convert to WebP 1280 wide (`Pillow`, quality about 84).
  The Start menu picture shows the owner's pinned taskbar apps (the owner chose to keep it).

## License

The site's code and text are under the MIT License (see `LICENSE`). Third-party names, logos and software that
appear in the screenshots (Firefox, Steam, GIMP, Brave, KDE and others) belong to their owners and are not covered
by it.

## Publishing a new ISO (what changes on the page)

Only the Download section of `index.html` changes: the `<h3>` (version and build date), the Oracle link, the size in the button,
and the SHA-256 in the "Optional: check it" step. Do it **after** the ISO is in the Oracle bucket and its public download was hashed
(see `zohara/docs/HANDOFF-2026-10-12.md`, "How the release was done"). The bucket keeps only the newest two ISOs; the SourceForge
mirror button was removed for 1.1 (add it back only when the mirror has the same build). Push to `main`, wait for Render, then compare
`sha256sum` of the live image files and check the live page text. The page has no `sitemap.xml` or `robots.txt` yet.

## Page map

Single page, `index.html`, sections in order: top (hero), `#features` (Made for people coming from Windows), `#new` (New in Zohara OS 1.1),
`#screenshots` (A look around, 15 pictures), What is inside (with `#status`), `#download`, `#requirements`, Open source (repositories).
Other files: `404.html`, `style.css`, `assets/`, `google0dfec91cc0809278.html` (Google Search Console verification), `CNAME`.
