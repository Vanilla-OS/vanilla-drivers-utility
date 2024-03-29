<div align="center">
    <img src="data/icons/hicolor/scalable/apps/org.vanillaos.DriversUtility.svg" height="64">
    <h1>Vanilla Drivers Utility</h1>
</div>

<div align="center">

[![Translation Status][weblate-image]][weblate-url]

[weblate-url]: https://hosted.weblate.org/engage/vanilla-os/
[weblate-image]: https://hosted.weblate.org/widgets/vanilla-os/-/vanilla-drivers-utility/svg-badge.svg

<p>A frontend in GTK 4 and Libadwaita for ubuntu-drivers.</p>
<br />
<img src="data/screenshot.png">
</div>

## Build
### Dependencies
- build-essential
- meson
- libadwaita-1-dev
- gettext
- desktop-file-utils
- ubuntu-drivers-common

### Build
```bash
meson build
ninja -C build
```

### Install
```bash
sudo ninja -C build install
```

## Run
```bash
vanilla-drivers-utility

# embedded mode
vanilla-drivers-utility --embedded
```

## Other distributions
This utility works on any Ubuntu-based distribution, just note that `NoDisplay=true` is set
in the desktop file, since Vanilla OS uses the embedded mode. If you want to use the
standalone mode, you can remove this line and the icon will be shown in the applications
menu of your distribution.
