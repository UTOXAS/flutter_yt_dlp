# Changelog

All notable changes to the `flutter_yt_dlp` plugin will be documented in this file.

## [0.2.0] - 2025-03-19

### Added

- **Modular Android Architecture**: Split `FlutterYtDlpPlugin.kt` into multiple Kotlin classes (`ChannelManager`, `DownloadManager`, `DownloadProcessor`, etc.) for improved maintainability.
- **Simplified Python Script**: Replaced multiple format-specific functions in `yt_dlp_helper.py` with `get_video_info` and `download_format`, streamlining native integration.
- **Format Categorization**: Added `format_categorizer.dart` to categorize formats on the Dart side into `rawVideoWithSoundFormats`, `mergeFormats`, and `rawAudioOnlyFormats`.
- **Enhanced Logging**: Introduced `logger.dart` for dedicated, configurable logging across the plugin.
- **New API Methods**: Added `getVideoInfo`, `getCombinedFormats`, `getMergeFormats`, `getAudioOnlyFormats`, and `getThumbnailUrl` to `FlutterYtDlpClient`.
- **Download Options**: Support for `overrideName` and `downloadAsRaw` in `startDownload` for custom filenames and raw format preservation.
- **Comprehensive Example App**: Revamped `example/` with a full UI, including format selection, progress tracking, and provider-based state management.

### Changed

- **API Overhaul**: Replaced specific format-fetching methods (e.g., `getAllRawVideoWithSoundFormats`) with a unified `getVideoInfo` approach, requiring users to access formats via the returned map (breaking change).
- **Plugin Class**: Renamed `FlutterYtDlpPlugin` to `FlutterYtDlpClient` with a simplified interface.
- **Model Simplification**: Removed `Format`, `CombinedFormat`, and `MergeFormat` classes; formats are now dynamic maps processed by `FormatCategorizer`.
- **Android FFmpeg Integration**: Shifted FFmpeg inclusion from `chaquopy.extractPackages` to `dependencies.implementation` in `android/build.gradle` (functionality unchanged).
- **Logging**: Moved logging setup from `utils.dart` to `logger.dart` for better encapsulation, reverting `print` usage from 0.1.4 to proper logging.

### Fixed

- **General Improvements**: Refactoring likely resolved minor bugs and performance issues from the monolithic 0.1.4 structure, though specific fixes aren’t detailed.

### Breaking Changes

- **API Changes**: Users must update code to use `getVideoInfo` and access categorized formats instead of old methods.
- **Download Method**: `startDownload` now requires a format map from `getVideoInfo` results and supports new parameters.
- **Model Removal**: Direct use of format classes is no longer possible; adapt to dynamic maps.

### Notes

- Refer to the updated [README.md](README.md) for new usage instructions and the [example app](example/lib/main.dart) for practical guidance.

## [0.1.4] - 2025-03-13

### Added

- Expanded Android NDK ABI support in `android/build.gradle` to include `armeabi-v7a`, `arm64-v8a`, `x86`, and `x86_64`, enhancing compatibility across a wider range of devices.
- Added try-catch block in `FlutterYtDlpPlugin.initialize()` to handle and report initialization errors, improving debugging capabilities.
- Added `changed_files.txt` and `old_codebase.txt` to `.gitignore` for better management of temporary development files.

### Changed

- Modified `setupLogging` in `utils.dart` to use `print` instead of `_logger.info` for log output.
- Updated `FlutterYtDlpPlugin.initialize()` to use `print` statements for initialization feedback instead of logging.

### Fixed

- No specific bugs fixed in this release; focus was on compatibility and debugging enhancements.

### Notes

- The use of `print` in `setupLogging` and `initialize()` is temporary and will be reverted to proper logging in the next release to adhere to `avoid_print` lint rules.
- File sizes remain under 100 lines, and functions average around 3 lines, maintaining clean code principles.

## [0.1.3] - 2025-03-13

### Added

- Split `flutter_yt_dlp.dart` into three files for improved maintainability:
  - `models.dart`: Contains data classes (`Format`, `CombinedFormat`, `MergeFormat`, `DownloadProgress`, `DownloadState`, `DownloadTask`).
  - `utils.dart`: Contains utility functions (`setupLogging`, `generateOutputPath`, `convertFormatToMap`).
  - `flutter_yt_dlp.dart`: Main plugin class with core functionality, including `formatBytes`.
- Added comprehensive Dartdoc comments to public APIs to address `public_member_api_docs` lint warnings.
- Exposed `formatBytes` as a public method in `FlutterYtDlpPlugin` for formatting byte sizes in a human-readable format.
- **Improved Null Safety**: Updated `Format`, `CombinedFormat`, and related classes to handle `null` values from platform channels, preventing type cast errors (e.g., `TypeError: type 'Null' is not a subtype of type 'String'`).

### Changed

- Updated `toLogString` methods in `models.dart` to use `String Function(int)` syntax for better type safety.
- Adjusted imports in `main.dart` to reflect the new modular file structure.
- Improved logging in `_fetchFormats` to use a ternary operator for format type checking.
- Renamed `_MyAppState` to `MyAppState` in `main.dart` to resolve `library_private_types_in_public_api`.

### Fixed

- Resolved `undefined_method: formatBytes` errors in `main.dart` by making `formatBytes` a public method in `FlutterYtDlpPlugin`.
- Fixed `undefined_identifier` errors in `utils.dart` by adding `import 'models.dart'`.
- Replaced `print` with logging in `setupLogging` to fix `avoid_print` lint warning.
- Corrected `forEach` usage in `_fetchFormats` to a `for` loop to address `avoid_function_literals_in_foreach_calls`.

### Notes

- File sizes are kept under 100 lines each, with functions averaging around 3 lines, adhering to clean code principles.
- Some `public_member_api_docs` warnings remain but are informational (severity 2).

## [0.1.2] - 2025-03-13

### Changed

- Removed unnecessary comments for cleaner and more maintainable code.

## [0.1.1] - 2025-03-12

### Added

- **Cancel Download Refinement**: Enhanced the `DownloadTask.cancel()` method with better stream cleanup and state management, ensuring robust cancellation of ongoing downloads.

## [0.1.0] - 2025-03-12

### Initial Release

- **Added**: Support for fetching media formats using `yt-dlp`:
  - Raw video with sound formats (`getAllRawVideoWithSoundFormats`).
  - Video and audio formats for merging (`getRawVideoAndAudioFormatsForMerge`).
  - Non-MP4 video formats for conversion to MP4 (`getNonMp4VideoWithSoundFormatsForConversion`).
  - Raw audio-only formats (`getAllRawAudioOnlyFormats`).
  - Non-MP3 audio formats for conversion to MP3 (`getNonMp3AudioOnlyFormatsForConversion`).
- **Added**: Download functionality with progress and state tracking:
  - Download raw video+sound, merged video+audio, and audio-only formats.
  - Real-time progress updates via `progressStream`.
  - State updates (preparing, downloading, merging, converting, completed, canceled, failed) via `stateStream`.
  - Option to cancel downloads mid-progress.
- **Added**: Example app demonstrating all features with a simple UI.
- **Platform**: Android-only support via Chaquopy for Python integration (minimum SDK 24).
- **Dependencies**: Integrated `yt-dlp` (2025.2.19) and FFmpeg (6.0) via Chaquopy.
- **Developed**: With assistance from Grok by xAI for design and implementation.

## [0.0.1]

- Placeholder for initial development version (not released).
