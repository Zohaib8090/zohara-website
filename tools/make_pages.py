#!/usr/bin/env python3
"""Writes the website&rsquo;s pages (index, settings, store, games, link, welcome) from the text below, so the header, footer and
rail are identical everywhere. The result is plain static HTML that is committed: hosting needs no build step, and this script
only has to be run again when the text changes:  python3 tools/make_pages.py
"""
import html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://zohara-website.onrender.com"
ISO_URL = "https://objectstorage.ap-mumbai-1.oraclecloud.com/n/bm27e3oxmp04/b/zohara-os/o/zohara-os-2026.10.10-x86_64.iso"
V = "20261112a"  # bump when style.css or site.js change, so browsers fetch the new files
ISO_SHA = "9a4602141595fe8d1c2dc31ac0b0632ee1f6202a9db07e8943dab4fbce39518e"

NAV = [("index.html", "Home"), ("settings.html", "Settings"), ("store.html", "Store"), ("games.html", "Games"),
       ("link.html", "Link"), ("welcome.html", "Welcome")]


def e(s):
    return html.escape(s, quote=True)


_num = [1]


def head(title, desc, page, image="assets/og-image.jpg", extra=""):
    _num[0] = 1  # the first section of every page (its hero) is 01
    url = SITE + "/" + ("" if page == "index.html" else page)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  <meta name="theme-color" content="#080B10">
  <meta name="color-scheme" content="dark light">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Zohara OS">
  <meta property="og:locale" content="en_US">
  <link rel="canonical" href="{url}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/{image}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Zohara OS: a Linux that feels like home, with its desktop, taskbar and Start menu">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(title)}">
  <meta name="twitter:description" content="{e(desc)}">
  <meta name="twitter:image" content="{SITE}/{image}">
  <link rel="icon" href="assets/logo.svg" type="image/svg+xml">
  <link rel="icon" href="assets/icons/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="icon" href="favicon.ico" sizes="48x48">
  <link rel="apple-touch-icon" href="assets/icons/apple-touch-icon.png">
  <link rel="manifest" href="assets/site.webmanifest">
  <link rel="stylesheet" href="style.css?v={V}">{extra}
</head>
<body id="top">
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="wrap bar">
      <a class="brand" href="./" aria-label="Zohara OS, home"><img src="assets/logo.svg" alt="" width="30" height="30">Zohara OS</a>
      <button class="icon-btn menu-btn" id="menu" aria-label="Menu" aria-expanded="false" aria-controls="nav">&#9776;</button>
      <nav class="nav" id="nav" aria-label="Main">
{chr(10).join(f'        <a href="{h}"' + (' aria-current="page"' if h == page else '') + f'>{t}</a>' for h, t in NAV)}
        <a href="./#download" class="dl">Download</a>
        <button class="icon-btn" id="theme" aria-label="Switch between dark and light" title="Dark / light">&#9681;</button>
      </nav>
    </div>
  </header>
"""


def crumb(num, name):
    return f"""  <div class="crumb"><div class="wrap"><span>{num}</span><span>/</span><b>{e(name)}</b></div></div>
"""


FOOT = """  <footer class="site-footer">
    <div class="wrap">
      <div class="cols">
        <div>
          <p class="fh" role="heading" aria-level="2">Zohara OS</p>
          <p>Created and maintained by <strong>Zohaib Baig</strong> (<a href="https://github.com/Zohaib8090">@Zohaib8090</a>). Dual-licensed under MIT and GPL-3.0-or-later; third-party software keeps its own licenses.</p>
        </div>
        <div>
          <p class="fh" role="heading" aria-level="2">Pages</p>
          <ul>
            <li><a href="settings.html">Settings</a></li>
            <li><a href="store.html">Store</a></li>
            <li><a href="games.html">Games</a></li>
            <li><a href="link.html">Zohara Link</a></li>
            <li><a href="welcome.html">Welcome and installer</a></li>
          </ul>
        </div>
        <div>
          <p class="fh" role="heading" aria-level="2">Source</p>
          <ul>
            <li><a href="https://github.com/Zohaib8090/zohara">zohara</a>: the ISO, Store, Welcome, voice typing</li>
            <li><a href="https://github.com/Zohaib8090/zohara-settings">zohara-settings</a></li>
            <li><a href="https://github.com/Zohaib8090/zohara-packages">zohara-packages</a></li>
            <li><a href="https://github.com/Zohaib8090/zohara-pipeline">zohara-pipeline</a></li>
            <li><a href="https://github.com/Zohaib8090/zohara-link">zohara-link</a></li>
          </ul>
        </div>
      </div>
      <p class="legal">Windows is a trademark of Microsoft. Zohara OS is an independent project and is not affiliated with or endorsed by Microsoft, Brave Software, Valve, or Arch Linux.</p>
    </div>
  </footer>
  <script src="site.js?v={V}"></script>
</body>
</html>
"""


def sec(id_, rail, num, label, inner, cls=""):
    _num[0] += 1
    num = f"{_num[0]:02d}"  # numbers follow the rail: 01 is the hero, then 02, 03 ...
    return f"""  <section id="{id_}" data-rail="{e(rail)}"{(' class="' + cls + '"') if cls else ''}>
    <div class="wrap">
      <div class="head rv">
        <span class="hud"><i>{num}</i>{e(label)}</span>
{inner[0]}
      </div>
{inner[1]}
    </div>
  </section>
"""


def frame(src, alt, caption, label, w=1280, h=877, big=False):
    return f"""<figure class="frame rv">
          <div class="bar2"><span></span><span></span><span></span><em>{e(label)}</em></div>
          <a href="{src}"><img src="{src}" alt="{e(alt)}" width="{w}" height="{h}" loading="lazy"></a>
          {('<figcaption>' + caption + '</figcaption>') if caption else ''}
        </figure>"""


def card(title, text, n=""):
    return f"""<div class="card rv">{('<span class="n">' + n + '</span>') if n else ''}<h3>{title}</h3><p>{text}</p></div>"""


def link_card(href, title, text, tag=""):
    return f"""<a class="card rv" href="{href}">{('<span class="tag ' + tag[0] + '">' + tag[1] + '</span> ') if tag else ''}<h3 style="margin-top:{'12px' if tag else '0'}">{title}</h3><p>{text}</p><span class="more">Open &rarr;</span></a>"""


def ticks(items):
    return '<ul class="ticks rv">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def write(name, text):
    text = text.replace("{V}", V)
    (ROOT / name).write_text(text, encoding="utf-8")
    print("wrote", name, len(text), "bytes")


# ══════════════════════════════════════════════════════ HOME ══════════════════════════════════════════════════════
def jsonld():
    import json
    data = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Zohara OS", "inLanguage": "en",
         "publisher": {"@id": SITE + "/#org"}},
        {"@type": "Organization", "@id": SITE + "/#org", "name": "Zohara OS", "url": SITE + "/",
         "logo": SITE + "/assets/icons/icon-512.png", "founder": {"@type": "Person", "name": "Zohaib Baig"},
         "sameAs": ["https://github.com/Zohaib8090/zohara-website"]},
        {"@type": "SoftwareApplication", "@id": SITE + "/#software", "name": "Zohara OS", "operatingSystem": "Linux",
         "applicationCategory": "OperatingSystem", "softwareVersion": "1.1", "url": SITE + "/", "downloadUrl": ISO_URL,
         "fileSize": "4.0 GB", "image": SITE + "/assets/og-image.jpg", "inLanguage": "en",
         "description": "An Arch-based Linux distribution with the KDE Plasma desktop, a Windows-style taskbar and Start menu, a Settings app and a software store.",
         "author": {"@id": SITE + "/#org"},
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD", "availability": "https://schema.org/InStock"}}]}
    return '\n  <script type="application/ld+json">' + json.dumps(data, indent=2) + "</script>"


def home():
    out = head("Zohara OS: a Linux that feels like home",
               "Zohara OS 1.1 is an Arch-based Linux with a desktop Windows users already know: taskbar and Start menu, a 3D desktop cube, Settings and a software store.",
               "index.html", extra=jsonld())
    out += """  <main id="main">
  <section class="hero" id="start" data-rail="Start">
    <div class="wrap">
      <span class="hud rv"><i>01</i>Arch &middot; KDE Plasma 6 &middot; Wayland</span>
      <h1 class="rv">A Linux that feels like <em>home</em>.</h1>
      <p class="lead rv">Zohara OS gives you a desktop you already know how to use: a familiar taskbar and Start menu, a Settings app laid out like Windows 11, a software store, and voice typing that runs entirely on your own computer.</p>
      <div class="cta rv"><a class="btn" href="#download">Get Zohara OS</a><a class="btn ghost" href="#desktop">Look around</a></div>
      <div class="chips rv"><span class="tag">1.1 &middot; build 2026.10.10</span><span class="tag">Free and open source</span><span class="tag">x86_64 PCs</span><span class="tag test">Still being finished</span></div>
      """ + frame("assets/img/desktop.webp", "The Zohara OS desktop with a taskbar, Start button and open windows", "A real capture from a laptop running Zohara OS 1.1.", "desktop", 1280, 800) + """
    </div>
  </section>
"""
    out += sec("desktop", "Desktop", "02", "Made for people coming from Windows", (
        '        <h2>A desktop you already know.</h2>\n        <p class="lead">Linux is powerful, but it usually asks you to learn a new way of doing everything. Zohara keeps the parts you know and puts a button on the parts that used to need a terminal.</p>',
        '<div class="grid g3">' +
        card("Taskbar and Start menu", "A Start button, a Start menu with search and Favorites, and a Windows-flavoured look on top of KDE Plasma. Nothing to relearn on day one.", "A") +
        card("Voice typing, fully offline", "Press <kbd>Meta</kbd> + <kbd>H</kbd>, speak, and the words are typed where your cursor is. Recognition runs on your computer with whisper.cpp; nothing is uploaded.", "B") +
        card("A 3D desktop cube", "Your desktops turn as a cube with 3 and 4 finger swipes. Press <kbd>Meta</kbd> + <kbd>C</kbd> to see every desktop at once and drag windows between them.", "C") +
        card("Live wallpaper", "Pick a video and it loops behind your windows. It is quiet unless you turn the sound on.", "D") +
        card("Sound your way", "Left and right balance for each speaker or headset, volume up to 150%, and an equalizer that changes while the music plays.", "E") +
        card("Graphics choice per app", "On a laptop with two graphics chips, choose which one each app uses: the power for the apps that need it, the battery for the rest.", "F") +
        '</div>'))
    out += sec("settings", "Settings", "03", "Zohara Settings", (
        '        <h2>Settings that change <em>real things</em>.</h2>\n        <p class="lead">A custom Settings app in the Windows 11 layout: display, sound, Bluetooth, network, storage, accounts, default apps, gaming, printers and more. Each page controls the actual system, not a mock-up.</p>',
        '<div class="split">' + ticks([
            "<b>Updates you control.</b> Pick a channel, choose what to update, undo the last update.",
            "<b>USB drives and SD cards.</b> Rename, format, check and repair, close safely, or write a bootable USB from an ISO.",
            "<b>Privacy.</b> A firewall and device access in one place, one indicator for camera and microphone use.",
            "<b>Memory and performance</b> in plain words, with the defaults a click away.",
            '<b>Troubleshoot.</b> Problems found and fixed, with a report you can send.']) +
        frame("assets/img/settings-home.webp", "The Zohara Settings home page with a left rail and card groups", "Settings: a left rail and card groups, like the Windows 11 layout.", "settings") +
        '</div><div class="cta rv" style="margin-top:34px"><a class="btn ghost" href="settings.html">Everything in Settings &rarr;</a></div>'))
    out += sec("store", "Store", "04", "Zohara Store", (
        '        <h2>One place for your apps.</h2>\n        <p class="lead">Zohara Store installs apps and handles updates. It shows what is changing, lets you choose what to update, and offers a way back if an update goes wrong.</p>',
        '<div class="split flip">' + ticks([
            "<b>Many sources, one list.</b> The system repositories, a large set of prebuilt community apps, and Flathub.",
            "<b>Snapshots around updates.</b> On Btrfs a snapshot is taken before and after every package change.",
            "<b>Updates follow a date the project approves</b>, not the raw Arch stream."]) +
        frame("assets/img/store.webp", "Zohara Store showing apps to install", "Zohara Store: find and install apps in one place.", "store", 1280, 890) +
        '</div><div class="cta rv" style="margin-top:34px"><a class="btn ghost" href="store.html">About the Store &rarr;</a></div>'))
    out += sec("games", "Games", "05", "Games", (
        '        <h2>Windows games, <em>no Steam in the way</em>. <span class="tag test">In testing</span></h2>\n        <p class="lead">Games from Steam, Lutris and Heroic show up on their own. In the newest builds, a Windows game or installer opens with a double-click and runs through Proton-GE or Wine, with its own settings for the graphics chip, Game Mode and the performance overlay.</p>',
        '<div class="grid g3">' +
        card("Double-click and play", "<code>.exe</code>, <code>.bat</code>, <code>.msi</code> and shortcuts open with Proton-GE or Wine. Proton-GE is downloaded when you ask for it and checked against its published checksum.", "01") +
        card("Safety mode", "A program you have not added as a game runs in a protected space that sees an empty home folder, not your files, passwords or browser.", "02") +
        card("A gear on every game", "Graphics chip, Game Mode, MangoHud, DirectX through Vulkan, game options and variables, for Steam, Lutris, Heroic and your own games.", "03") +
        '</div><div class="cta rv" style="margin-top:34px"><a class="btn ghost" href="games.html">How it works &rarr;</a></div>'))
    out += sec("link", "Link", "06", "Zohara Link", (
        '        <h2>Your phone and your computer, <em>together</em>. <span class="tag test">In development</span></h2>\n        <p class="lead">A companion for Android: share the clipboard, send files, see phone notifications on the desktop, and use the phone as a touchpad, keyboard and game controller. Pairing is a PIN you type once; nothing leaves your network unless you set up Tailscale.</p>',
        '<div class="grid g3">' +
        card("Clipboard, files, notifications", "Copy on one, paste on the other. Send a file either way. Phone notifications appear on the desktop.", "01") +
        card("A touchpad that feels like one", "Pointer acceleration, two-finger scroll, tap to click, tap-and-drag. Events go straight to a virtual input device.", "02") +
        card("A game controller", "The phone shows up on the computer as a wired Xbox 360 controller, with sticks, triggers, a direction pad and buttons.", "03") +
        '</div><div class="cta rv" style="margin-top:34px"><a class="btn ghost" href="link.html">About Zohara Link &rarr;</a></div>'))
    out += sec("safe", "Safe", "07", "Safe by design", (
        '        <h2>Problems get reported, <em>not hidden</em>.</h2>\n        <p class="lead">Zohara is careful where careful matters: before an update, before a disk is touched, and when something goes wrong.</p>',
        '<div class="grid g3">' +
        card("Snapshots around updates", "On Btrfs, a snapshot is taken before and after every package change, so there is something to go back to.", "A") +
        card("Hard to wipe by accident", "The disks inside the computer and the one Zohara runs from are locked. Every erase names the drive, lists what is on it and needs you to type ERASE.", "B") +
        card("Reports, not mysteries", "If the installer fails, one button on the Welcome screen saves a report to a USB stick. Installed, Settings keeps a log and offers one-click fixes.", "C") +
        card("A safer lock screen", "It no longer locks you out after a wrong password.", "D") +
        card("Updates you can say no to", "Programs that fit your hardware are suggested, and you can decline any of them.", "E") +
        card("Notify, never surprise", "Update checks tell you; they do not install on their own.", "F") +
        '</div>'))
    out += sec("inside", "Inside", "08", "What is inside", (
        '        <h2>Built on <em>solid parts</em>.</h2>',
        '<div class="grid g2">' +
        card("Arch Linux base", "With the KDE Plasma 6 desktop on Wayland.") +
        card("The Zen kernel", "Tuned for desktop and gaming rather than servers.") +
        card("NVIDIA open drivers included", "Supported NVIDIA GPUs need no manual driver setup.") +
        card("Brave Origin as the browser", "Brave&rsquo;s ad and tracker blocking without the wallet, VPN or news.") +
        card("The Calamares installer", "It can install alongside Windows when it finds it, and never picks &ldquo;Erase disk&rdquo; for you.") +
        card("Honest status", "Zohara OS is still being finished. Some Settings pages do not respond yet, and the ISO is built from the latest development work. Please try it in a virtual machine or on a spare computer first.") +
        '</div>'))
    out += sec("download", "Download", "09", "Download", (
        '        <h2>Try it <em>today</em>.</h2>\n        <p class="lead">The ISO is about 4.0 GB. It is hosted on Oracle Cloud object storage, because it is too large for a GitHub release file.</p>',
        f"""<div class="split">
        <div class="rv" style="display:grid;gap:18px">
          <p><span class="tag new">Zohara OS 1.1</span> <span class="tag">build 2026.10.10</span></p>
          <p class="cta"><a class="btn" href="{ISO_URL}">Download the ISO (4.0&nbsp;GB)</a></p>
          <p class="mono" style="font-size:.8rem;color:var(--faint)">SHA-256 (also in SHA256SUMS next to the download):</p>
          <div class="hash">{ISO_SHA}</div>
          <ol class="steps">
            <li>Write the ISO to a USB stick with Ventoy, balenaEtcher or <code>dd</code>.</li>
            <li>Boot from the stick and choose <b>Install Zohara</b>, or <b>Try Zohara</b> to look around first.</li>
          </ol>
          <p class="note"><b>Before you boot.</b> Turn off Secure Boot (the bootloaders are not signed yet). If the installer shows no disks, set storage mode to AHCI instead of RAID / Intel RST. On a PC with Windows, choose Install alongside or Manual partitioning.</p>
        </div>
        <div class="rv">
          <table>
            <tr><th>Processor</th><td>64-bit x86 (Intel or AMD). Older CPUs work; voice typing is slower on them.</td></tr>
            <tr><th>Memory</th><td>4 GB RAM</td></tr>
            <tr><th>Storage</th><td>20 GB free</td></tr>
            <tr><th>Firmware</th><td>UEFI or legacy BIOS</td></tr>
            <tr><th>Graphics</th><td>Intel, AMD, or a modern NVIDIA card</td></tr>
          </table>
          <p style="margin-top:18px;color:var(--faint);font-size:.9rem">Tagged versions and release notes are on the <a href="https://github.com/Zohaib8090/zohara/releases">GitHub Releases page</a>. The newest development build is on <a href="https://github.com/Zohaib8090/zohara/actions">GitHub Actions</a> (sign-in required).</p>
        </div>
      </div>"""))
    out += "  </main>\n" + FOOT
    write("index.html", out)


# ══════════════════════════════════════════════════ SETTINGS PAGE ═══════════════════════════════════════════════════
def settings():
    out = head("Zohara Settings: the control panel that changes real things", "Zohara Settings is a Windows 11-style Settings app that controls the real system: display, sound, network, updates, privacy, drives, gaming and more.", "settings.html", "assets/img/settings-home.webp")
    out += crumb("02", "Settings") + '  <main id="main">\n'
    out += """  <section class="hero" id="overview" data-rail="Overview"><div class="wrap">
      <span class="hud rv"><i>01</i>Zohara Settings</span>
      <h1 class="rv">One app for <em>everything</em> about your computer.</h1>
      <p class="lead rv">A left rail and card groups, like the Windows 11 layout, written for Zohara in Rust and GTK. Every page changes the real system, and changes show up as the system changes, within a second.</p>
      """ + frame("assets/img/settings-home.webp", "Zohara Settings home", "The Settings home page.", "settings / home") + "\n    </div></section>\n"
    out += sec("look", "Look & sound", "01", "Make it yours", (
        '        <h2>The desktop, <em>your way</em>.</h2>',
        '<div class="grid g3">' +
        card("Taskbar and windows", "Hide, float or fade the taskbar, move the window buttons, and set the cube and animation options with sliders.") +
        card("3D desktop cube", "Turn desktops as a cube, open the overview, move windows between desktops, or let each new app open on its own desktop.") +
        card("Live wallpaper", "A video that loops behind your windows, quiet unless you turn the sound on.") +
        card("Sound", "Balance for every output, volume up to 150%, an equalizer that changes while the music plays.") +
        card("Touchpad and mouse", "Reverse the scroll direction on each separately, tune speed, acceleration, tap to click and left-handed mode.") +
        card("Accessibility", "Contrast, text size, a screen reader and more.") +
        '</div><div class="shots" style="margin-top:28px">' +
        frame("assets/img/settings-sound.webp", "Sound settings", "<b>Sound.</b> Volume, balance for every device, and an equalizer.", "sound") +
        frame("assets/img/settings-touchpad.webp", "Touchpad and mouse settings", "<b>Touchpad and mouse.</b> Scroll direction, speed, tap to click.", "touchpad") +
        frame("assets/img/settings-accessibility.webp", "Accessibility settings", "<b>Accessibility.</b> Contrast, text size, a screen reader.", "accessibility") +
        '</div>'))
    out += sec("system", "System", "02", "System", (
        '        <h2>Display, power, <em>memory</em>.</h2>',
        '<div class="grid g3">' +
        card("Display", "Resolution, scale and night light.") +
        card("Power and battery", "Power mode, sleep and lid rules.") +
        card("Memory and performance", "Plain-language controls for swap behaviour, cache pressure and compressed memory, with the defaults a click away.") +
        card("Graphics choice per app", "On a laptop with two graphics chips, choose which one each app uses.") +
        card("Keyboard", "Shortcuts, key repeat and layouts.") +
        card("Default apps", "Choose what opens each kind of file.") +
        '</div><div class="shots" style="margin-top:28px">' +
        frame("assets/img/settings-display.webp", "Display settings", "<b>Display.</b> Resolution, scale and night light.", "display") +
        frame("assets/img/settings-power.webp", "Power and battery settings", "<b>Power and battery.</b> Power mode, sleep and lid rules.", "power") +
        frame("assets/img/settings-keyboard.webp", "Keyboard settings", "<b>Keyboard.</b> Shortcuts, key repeat and layouts.", "keyboard") +
        '</div>'))
    out += sec("updates", "Updates", "03", "Updates and apps", (
        '        <h2>Updates you <em>control</em>.</h2>\n        <p class="lead">Pick a channel, choose what to update, and undo the last update. Programs that fit your hardware are suggested, and you can say no to any of them. Update checks tell you; they never install on their own.</p>',
        '<div class="shots">' +
        frame("assets/img/settings-update.webp", "Zohara Update", "<b>Updates.</b> A channel, what to update, undo.", "updates") +
        frame("assets/img/settings-apps.webp", "Apps settings", "<b>Apps.</b> Installed apps, startup apps and web apps.", "apps") +
        frame("assets/img/settings-default-apps.webp", "Default apps", "<b>Default apps.</b> What opens each kind of file.", "default apps") +
        '</div>'))
    out += sec("drives", "Drives", "04", "Drives and storage", (
        '        <h2>USB drives, SD cards and <em>external disks</em>.</h2>\n        <p class="lead">Plug one in and it shows up in Settings.</p>',
        '<div class="split">' + ticks([
            "<b>Rename and format</b> as exFAT, FAT32, ext4 or Btrfs.",
            "<b>Check and repair</b>, and close it safely before you unplug it.",
            "<b>Make a bootable USB.</b> Choose an ISO or disk image and write it from Settings, with a read-back check afterwards. Your administrator password is asked before anything is written.",
            "<b>Hard to wipe by accident.</b> The disks inside the computer and the one Zohara runs from are locked. Every erase names the drive, lists what is on it and needs you to type ERASE; Settings checks it is still the same drive just before it starts."]) +
        '<div class="note ok rv"><b>Why so careful?</b> A wrong click on a disk tool is the one mistake that cannot be undone, so the app makes the safe path the only easy one.</div></div>'))
    out += sec("privacy", "Privacy", "05", "Privacy and troubleshooting", (
        '        <h2>Safe, and <em>honest</em> about problems.</h2>',
        '<div class="shots">' +
        frame("assets/img/settings-privacy.webp", "Privacy and security", "<b>Privacy and security.</b> A firewall and device access in one place, one indicator for camera and microphone use.", "privacy") +
        frame("assets/img/settings-troubleshoot.webp", "Troubleshoot", "<b>Troubleshoot.</b> Problems found and fixed, with a report you can send.", "troubleshoot") +
        frame("assets/img/settings-gaming.webp", "Gaming", "<b>Gaming.</b> Your games found for you, and Game Mode.", "gaming") +
        '</div>'))
    out += sec("next", "Next", "06", "In testing now", (
        '        <h2>Coming <em>next</em>. <span class="tag test">In testing</span></h2>\n        <p class="lead">These are built and being tested in the development channel. They are not in the 1.1 ISO.</p>',
        '<div class="grid g3">' +
        card("Windows games", "Open Windows programs with a double-click, with Proton-GE or Wine, a Safety mode, and settings for each game.", "01") +
        card("Games from every launcher", "A settings gear for Steam, Lutris and Heroic games: graphics chip, Game Mode, MangoHud, options.", "02") +
        card("Java for Minecraft", "See which Javas are installed, which a Minecraft version needs, and install or switch the system Java.", "03") +
        card("Zohara Link and game streaming", "Pair a phone, use it as a touchpad and game controller, and stream the screen as live video.", "04") +
        card("Live graphics view", "Which graphics chip each app is using right now, with load, memory and temperature, without waking a sleeping chip.", "05") +
        card("Proton-GE updates", "A notice when a newer Proton-GE is out. You press Update; nothing is automatic.", "06") +
        '</div>'))
    out += "  </main>\n" + FOOT
    write("settings.html", out)


# ═══════════════════════════════════════════════════ STORE PAGE ═════════════════════════════════════════════════════
def store():
    out = head("Zohara Store: one place for your apps", "Zohara Store installs apps and handles updates, showing what is changing and offering a way back if an update goes wrong.", "store.html", "assets/img/store.webp")
    out += crumb("03", "Store") + '  <main id="main">\n'
    out += """  <section class="hero" id="overview" data-rail="Overview"><div class="wrap">
      <span class="hud rv"><i>01</i>Zohara Store</span>
      <h1 class="rv">Find and install apps in <em>one place</em>.</h1>
      <p class="lead rv">Zohara Store installs apps and handles updates. It shows what is changing, lets you choose what to update, and offers a way back if an update goes wrong.</p>
      """ + frame("assets/img/store.webp", "Zohara Store", "The Store.", "store", 1280, 890) + "\n    </div></section>\n"
    out += sec("sources", "Sources", "01", "Where apps come from", (
        '        <h2>Many sources, <em>one list</em>.</h2>',
        '<div class="grid g3">' +
        card("System repositories", "Arch Linux&rsquo;s official repositories.", "A") +
        card("Community builds", "A large set of prebuilt community apps (Chrome, Spotify, VS Code, Zoom and more).", "B") +
        card("Flathub", "Sandboxed apps from Flathub, added for you the first time it is missing.", "C") +
        '</div><p class="note rv" style="margin-top:22px"><b>The AUR, with a warning.</b> The newest builds can also search the AUR (community-made, not reviewed by Zohara). Before anything is built, the Store shows a warning with Cancel as the default, lets you read the real build script, and only then offers to build and install it.</p>'))
    out += sec("updates", "Updates", "02", "Updates", (
        '        <h2>You decide <em>what updates</em>.</h2>',
        '<div class="split">' + ticks([
            "<b>Updates follow a date that the project approves</b>, not the raw Arch stream. The approval list is signed, and a machine checks the signature.",
            "<b>Snapshots around every change.</b> On Btrfs, a snapshot is taken before and after every package change.",
            "<b>A channel picker.</b> A computer follows one channel; you can change it on the Updates page.",
            "<b>Separate on purpose.</b> Settings updates the system; the Store updates Flathub apps. They are separate programs, so one cannot break the other."]) +
        frame("assets/img/settings-update.webp", "Zohara Update page", "Updates: pick a channel, choose what to update, undo the last update.", "updates") + '</div>'))
    out += "  </main>\n" + FOOT
    write("store.html", out)


# ═══════════════════════════════════════════════════ GAMES PAGE ═════════════════════════════════════════════════════
def games():
    out = head("Zohara Games: Windows games with no Steam in the way", "Windows programs and games open with a double-click through Proton-GE or Wine, with settings for every game, on Zohara OS. In testing.", "games.html", "assets/img/settings-gaming.webp")
    out += crumb("04", "Games") + '  <main id="main">\n'
    out += """  <section class="hero" id="overview" data-rail="Overview"><div class="wrap">
      <span class="hud rv"><i>01</i>Games <span class="tag test">In testing</span></span>
      <h1 class="rv">Play Windows games <em>without Steam</em> in the middle.</h1>
      <p class="lead rv">The layers that run Windows games live in the operating system. You turn them on in Settings, then double-click a game. Steam is not needed for that, and a Steam, Lutris or Heroic game still gets the same per-game settings.</p>
      <p class="note rv"><b>In testing.</b> Everything on this page is built and being tested in the development channel. It is not in the 1.1 ISO, and it has been tried on one laptop (Intel and NVIDIA graphics), not on AMD.</p>
      """ + frame("assets/img/settings-gaming.webp", "The Gaming page in Settings (Zohara OS 1.1)", "The Gaming page in Zohara OS 1.1. The newer parts below are in the development channel.", "gaming") + "\n    </div></section>\n"
    out += sec("double", "Double-click", "01", "Double-click and play", (
        '        <h2>Windows programs <em>just open</em>.</h2>\n        <p class="lead">Turn on &ldquo;Open Windows programs with a double-click&rdquo; in Settings (it is on by default in the newest builds). Then <code>.exe</code>, <code>.bat</code>, <code>.msi</code> and Windows shortcuts open from your file manager.</p>',
        '<div class="split">' + ticks([
            "<b>Proton-GE</b> is Valve&rsquo;s Proton plus extra fixes for more games. It is downloaded when you ask (about 565 MB) and checked against the published checksum before it is unpacked.",
            "<b>Plain Wine</b> is the other choice, for programs that do better without Proton.",
            "<b>One Windows folder per game</b>, so a game&rsquo;s settings and saves stay together. Programs an installer made can be found and added as games, with the program&rsquo;s own icon.",
            "<b>Right-click</b> a Windows file to run it once with Proton-GE, with Wine, or on the dedicated graphics chip, or to add it as a game.",
            "<b>When something fails to start,</b> you get a notice with an &ldquo;Open the log&rdquo; button, and every game keeps its own log."]) +
        '<div class="note ok rv"><b>On a laptop with two graphics chips</b>, each game can be told to use the dedicated one, and a live view shows which chip every running app is on, with load, memory and temperature, without waking a sleeping chip.</div></div>'))
    out += sec("safety", "Safety", "02", "Safety mode", (
        '        <h2>An unknown program <em>stays in its box</em>.</h2>\n        <p class="lead">Wine and Proton can read and delete everything in your home folder. Double-clicking makes it easy to run something you have not checked, so a program that is not one of your games runs in a protected space.</p>',
        '<div class="split flip">' + ticks([
            "It sees an <b>empty home folder</b>: no Documents, no browser data, no SSH keys, no Steam login.",
            "It can write only to <b>its own Windows folder</b> and its own program folder.",
            "It is made with <b>bubblewrap</b>, the technology Flatpak uses, and can be switched off per game, per start, or for everything.",
            "Tested by running a real program through Proton-GE: it could not read a secret file placed in the home folder, and a file it wrote there never reached the real disk."]) +
        '<div class="note rv"><b>What it is not.</b> It limits damage; it is not an antivirus. The program can still use the internet. Anti-cheat and some copy protection will not run inside it, and Game Mode does not reach into it.</div></div>'))
    out += sec("gear", "Settings", "03", "A gear on every game", (
        '        <h2>Every game, <em>every launcher</em>.</h2>\n        <p class="lead">One settings window for games you added by hand and for the ones Steam, Lutris and Heroic found.</p>',
        '<div class="grid g3">' +
        card("Graphics chip", "Automatic, or the dedicated one on a laptop with two.", "A") +
        card("Game Mode and MangoHud", "Priority while the game runs, and a frame-rate overlay.", "B") +
        card("DXVK and options", "DirectX through Vulkan on or off, extra game options and environment variables.", "C") +
        card("Proton-GE version", "Pin an older version for one game, or use the newest.", "D") +
        card("Windows components", "Install Visual C++, DirectX 9 files, fonts or .NET into one game&rsquo;s Windows folder.", "E") +
        card("Reset", "Start a game with a fresh Windows folder (the old one goes to the trash).", "F") +
        '</div><p class="note rv" style="margin-top:22px"><b>For Steam games,</b> the choices are written to Steam&rsquo;s own launch options while Steam is closed. For Lutris and Heroic they are written to each launcher&rsquo;s own per-game settings. A backup of the file is kept the first time.</p>'))
    out += sec("java", "Java", "04", "Java and Minecraft", (
        '        <h2>The right Java <em>for the version</em>.</h2>',
        '<div class="split">' + ticks([
            "Shows the <b>system Javas</b> that are installed and the ones launchers such as Modrinth bring with them.",
            "Minecraft 1.20.5 and newer needs Java 21, 1.18 to 1.20.4 needs Java 17, older versions need Java 8.",
            "<b>Install or switch</b> the system Java with one button (your password is asked).",
            "A launcher installed as a Flatpak cannot see the system Java and uses its own, which the page says."]) +
        '<div class="note rv"><b>Honest limit.</b> Fixing a particular Minecraft launcher problem needs its error message; this page shows what is installed and lets you change it.</div></div>'))
    out += "  </main>\n" + FOOT
    write("games.html", out)


# ════════════════════════════════════════════════════ LINK PAGE ═════════════════════════════════════════════════════
def link():
    out = head("Zohara Link: your phone and your computer, together", "Zohara Link is an Android companion for Zohara OS: share the clipboard, send files, see notifications, use the phone as touchpad or keyboard. In development.", "link.html")
    out += crumb("05", "Link") + '  <main id="main">\n'
    out += """  <section class="hero" id="overview" data-rail="Overview"><div class="wrap">
      <span class="hud rv"><i>01</i>Zohara Link <span class="tag test">In development</span></span>
      <h1 class="rv">Your phone and your computer, <em>together</em>.</h1>
      <p class="lead rv">A companion for Android that shares your clipboard and files, shows your phone&rsquo;s notifications on the desktop, and turns the phone into a touchpad, a keyboard and a game controller.</p>
      <p class="note rv"><b>Not released.</b> The computer side is in the development channel. The Android app is a test build that is not on any store: it installs from GitHub and has had builds and tests, but little use on real phones yet.</p>
    </div></section>
"""
    out += sec("share", "Share", "01", "Share", (
        '        <h2>Clipboard, files, <em>notifications</em>.</h2>',
        '<div class="grid g3">' +
        card("Clipboard", "Copy on one, paste on the other.", "A") +
        card("Files", "Send a file from the phone to the computer, or from the computer to the phone.", "B") +
        card("Notifications and media", "Phone notifications appear on the desktop; play, pause and skip from the phone.", "C") +
        '</div>'))
    out += sec("control", "Control", "02", "Control", (
        '        <h2>A touchpad, a keyboard and a <em>game controller</em>.</h2>\n        <p class="lead">The computer makes virtual input devices and writes the phone&rsquo;s events straight to them, so the pointer follows your finger instead of lagging behind it.</p>',
        '<div class="split">' + ticks([
            "<b>Touchpad.</b> Pointer acceleration, tap to click, two-finger tap to right-click, two-finger drag to scroll smoothly, tap-then-drag to hold the button.",
            "<b>Keyboard</b> keys, including held keys, and typing.",
            "<b>Game controller.</b> The phone appears as a wired Xbox 360 controller, the one every game and Steam already know: two sticks, two triggers, a direction pad and eleven buttons.",
            "<b>Full-screen remote.</b> See the screen and control it as a touchpad or a touch screen."]) +
        '<div class="note rv"><b>You decide.</b> A phone may only see the screen or control the mouse when you switch that on for it in Settings &gt; Zohara Link. Both are off until you choose.</div></div>'))
    out += sec("stream", "Stream", "03", "Game streaming", (
        '        <h2>Live video from the computer <em>to the phone</em>. <span class="tag test">In development</span></h2>\n        <p class="lead">The screen is captured through the desktop&rsquo;s own screen-sharing permission, encoded with a hardware video encoder, and sent as live video with WebRTC. The phone decodes it with its own hardware.</p>',
        '<div class="split flip">' + ticks([
            "<b>Hardware encoding.</b> The Intel chip&rsquo;s encoder first, so the NVIDIA chip can stay asleep; NVENC when the NVIDIA chip is already running the game; software as a last resort.",
            "<b>Encrypted</b> end to end by WebRTC, set up over the connection the phone is already paired on.",
            "<b>Input travels back</b> on the same stream.",
            "<b>One-time permission.</b> The desktop asks once whether Zohara Link may share the screen."]) +
        '<div class="note rv"><b>Honest status.</b> The pieces are built and tested separately: a whole test stream between two programs, the signalling against the real daemon, and the screen-sharing permission on a real laptop. A stream to a real phone has not been tried yet, and delay has not been measured. Sound is not built.</div></div>'))
    out += sec("safe", "Private", "04", "Private by design", (
        '        <h2>Nothing leaves <em>your network</em>.</h2>',
        '<div class="grid g3">' +
        card("A PIN you type once", "Pairing is closed until you press Pair a phone. The PIN is shown on the computer and typed on the phone; it never travels over the network.", "A") +
        card("Pinned and encrypted", "The connection is TLS with the computer&rsquo;s certificate pinned on the phone.", "B") +
        card("Away from home", "With Tailscale on both, the phone reaches the computer from any network. Zohara Link can sign in and out of Tailscale for you.", "C") +
        '</div>'))
    out += "  </main>\n" + FOOT
    write("link.html", out)


# ══════════════════════════════════════════════════ WELCOME PAGE ════════════════════════════════════════════════════
def welcome():
    out = head("Zohara Welcome and installer", "The Zohara Welcome app and installer: install, try, or move your files from an old Linux install, with checks at every step.", "welcome.html")
    out += crumb("06", "Welcome") + '  <main id="main">\n'
    out += """  <section class="hero" id="overview" data-rail="Overview"><div class="wrap">
      <span class="hud rv"><i>01</i>Zohara Welcome</span>
      <h1 class="rv">Install it, try it, or <em>move in</em>.</h1>
      <p class="lead rv">What you see on the live USB and the first time you sign in. Install Zohara, try it without installing anything, or move your files over from an old Linux install.</p>
    </div></section>
"""
    out += sec("install", "Install", "01", "Installing", (
        '        <h2>An installer that <em>asks first</em>.</h2>',
        '<div class="split">' + ticks([
            "<b>Calamares</b> does the install, and can install alongside Windows when it finds it.",
            "It <b>never picks &ldquo;Erase disk&rdquo; for you.</b>",
            "<b>Try Zohara</b> boots the full desktop from the USB stick so you can look around before changing anything.",
            "<b>If the installer fails,</b> one button on the Welcome screen saves a report to a USB stick."]) +
        '<div class="note rv"><b>Before you boot.</b> Turn off Secure Boot, since the bootloaders are not signed yet. If no disks show, set the storage mode to AHCI instead of RAID / Intel RST.</div></div>'))
    out += sec("move", "Move in", "02", "Moving in", (
        '        <h2>Bring your files, <em>safely</em>.</h2>\n        <p class="lead">Coming from another Linux install on the same computer? Welcome can move your files across, one at a time, and tells you which of your old apps have a Zohara equivalent.</p>',
        '<div class="grid g3">' +
        card("Move, verify, delete", "Each file is copied beside its destination, checked with SHA-256 against the original, renamed into place, and only then deleted from the old disk. Only one file&rsquo;s worth of extra space is needed, so it works on nearly full disks.", "A") +
        card("Nothing is overwritten", "If a file with the same name exists here, the old one is saved as &ldquo;name (old system).ext&rdquo;. An identical file is simply not copied twice.", "B") +
        card("A failed file stays put", "A file that does not verify stays on the old disk. Old system files are only deleted when every file succeeded and you asked for it.", "C") +
        card("Apps translated", "Debian and Ubuntu package names are matched to Arch packages, so the programs you used can be offered again.", "D") +
        card("Your own disk is protected", "The old partition must not be mounted anywhere else, so the disk Zohara runs from cannot be picked by mistake.", "E") +
        '</div>'))
    out += sec("first", "First sign-in", "03", "After the install", (
        '        <h2>The first time you <em>sign in</em>.</h2>',
        '<div class="split">' + ticks([
            "Welcome shows once on an installed system, with shortcuts to <b>migrate</b>, to <b>accounts</b> and to <b>updates</b> (both in Settings).",
            "Close it and it stays out of the way."]) + '<div></div></div>'))
    out += "  </main>\n" + FOOT
    write("welcome.html", out)


if __name__ == "__main__":
    home(); settings(); store(); games(); link(); welcome()
