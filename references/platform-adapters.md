# Platform Adapters

## Web

Lock:
- viewport
- DPR/scale policy
- browser family
- zoom 100%
- fonts
- scrollbar behavior

Wait for `document.fonts.ready`, images, and stable layout. Disable animation/caret during screenshots.

Inspect `getBoundingClientRect()` and computed styles for stubborn mismatches.

## WeChat Mini Program

`rpx` is relative to a 750-rpx design width. For device logical width `W`:

```text
1 rpx ≈ W / 750 logical px
```

At 390 logical px, `1 rpx ≈ 0.52 px`.

Verify:
- system vs custom navigation bar
- status bar / safe area
- capsule/menu button reserved region
- tab bar
- image `mode`
- scroll-view sizing
- text rendering in DevTools/device
- device pixel ratio and screenshot export size

Use real WeChat DevTools/device capture for final evidence whenever possible. Browser recreation is diagnostic only.

## Flutter

Lock:
- logical viewport
- devicePixelRatio
- textScaleFactor
- platform
- SafeArea
- theme

Prefer golden tests/emulator screenshots.

## React Native

Lock:
- device/emulator
- density
- font scale
- platform font behavior
- safe area

Prefer device/emulator screenshots.

## Desktop native

OS theme, font renderer, and native controls can dominate visual diffs. Record OS/theme and use native screenshot tooling.
