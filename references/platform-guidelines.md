# Platform Guidelines

The visual workflow is platform-independent; rendering evidence is not.

## Web
Use deterministic Chromium/Playwright where possible. Lock viewport, DPR, fonts, animation and content state.

## WeChat / other mini-programs
Respect runtime units, system chrome, capsule/navigation areas and native text/image rendering. Browser screenshots can aid iteration but should not be the final fidelity proof when native DevTools/device capture is available.

## Flutter / React Native / native mobile
Lock logical viewport, DPR/density, safe areas, font scale, theme/platform and use emulator/device/golden-test captures.

## Desktop native
OS controls/font rasterization/theme may dominate diffs. Compare under the intended OS/theme and disclose environment differences.
