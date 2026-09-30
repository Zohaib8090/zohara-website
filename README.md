# Zohara OS website

A static site: plain HTML and CSS, no build step, no JavaScript, no external fonts or trackers.

    index.html      the page
    style.css       styles (colours come from the logo: #0B0E14, #E8ECF1, #5FD4D4)
    404.html        not-found page
    assets/logo.svg the Zohara logo (copied from zohara-profile/airootfs/usr/share/pixmaps/zohara-logo.svg)
    assets/img/     screenshots, WebP, taken in the QEMU test VM

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
- Screenshots: retake them from a fresh install when the look changes (see `scripts/vm/README.md` in the
  `zohara` repository for the VM rig). They show a throwaway test account.

## License

The site's code and text are under the MIT License (see `LICENSE`). Third-party names, logos and software that
appear in the screenshots (Firefox, Steam, GIMP, Brave, KDE and others) belong to their owners and are not covered
by it.
