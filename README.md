# Zohara OS website

A static site: plain HTML and CSS, no build step, no JavaScript, no external fonts or trackers.

    index.html      the page
    style.css       styles (colours come from the logo: #0B0E14, #E8ECF1, #5FD4D4)
    404.html        not-found page
    assets/logo.svg the Zohara logo (copied from zohara-profile/airootfs/usr/share/pixmaps/zohara-logo.svg)
    assets/img/     screenshots, WebP, taken in the QEMU test VM

Preview locally: `python3 -m http.server 8080` in this folder, then open http://localhost:8080.

## Publishing on GitHub Pages

1. Create a public repository (suggested name: `zohara-website`) and push this folder to `main`.
2. Repository Settings > Pages > Build and deployment > Source: "Deploy from a branch", branch `main`, folder `/ (root)`.
3. The site appears at `https://<user>.github.io/<repo>/`. `404.html` has a `<base href="/zohara-website/">`, and
   `index.html` has absolute `og:` URLs; when a custom domain replaces the `github.io` address, change the base
   to `"/"` and update the `og:url` / `og:image` URLs.
4. A custom domain is optional: add it under Pages > Custom domain (and a `CNAME` file), then tick "Enforce HTTPS".

## Keeping it true

- Every claim on the page was checked against the repositories or in the VM. Update the download section when
  a direct ISO link exists, and the requirements table if the README's requirements change.
- Screenshots: retake them from a fresh install when the look changes (see `scripts/vm/README.md` in the
  `zohara` repository for the VM rig). They show a throwaway test account.

## License

The site's code and text are under the MIT License (see `LICENSE`). Third-party names, logos and software that
appear in the screenshots (Firefox, Steam, GIMP, Brave, KDE and others) belong to their owners and are not covered
by it.
