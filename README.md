# Flutter Yt Dlp

A Flutter plugin for downloading and processing media using `yt-dlp` and `FFmpeg`. This plugin enables developers to fetch video metadata, select from various format types (combined video with sound, merged video and audio, or audio-only), and download media with progress tracking and format conversion options.

## Features

- **Fetch Video Information**: Retrieve metadata such as title, thumbnail, and a comprehensive list of available formats.
- **Format Categorization**: Access categorized formats:
  - Combined video with sound (`rawVideoWithSoundFormats`).
  - Separate video and audio for merging (`mergeFormats`).
  - Audio-only formats (`rawAudioOnlyFormats`).
- **Flexible Downloads**: Download media with options to:
  - Keep raw formats or convert to MP4/MP3.
  - Overwrite existing files or generate unique filenames.
  - Specify custom output filenames.
- **Progress and State Tracking**: Monitor download progress and state changes (e.g., preparing, downloading, merging, completed).
- **Enhanced Example**: A fully-featured example app demonstrating UI integration and download management.

## Installation

Add the plugin to your `pubspec.yaml`:

```yaml
dependencies:
  flutter_yt_dlp: ^0.2.0
```

Run the following command to fetch the package:

```bash
flutter pub get
```

Ensure your Android app has storage permissions configured, as downloads require write access to external storage.

## Usage

Import the package in your Dart code:

```dart
import 'package:flutter_yt_dlp/flutter_yt_dlp.dart';
```

### Fetching Video Information

Use `FlutterYtDlpClient` to fetch video metadata and formats:

```dart
final client = FlutterYtDlpClient();
final info = await client.getVideoInfo('<https://youtu.be/nl8o9PsJPAQ>');
print('Title: ${info['title']}');
print('Thumbnail: ${info['thumbnail']}');
```

The `info` map includes categorized formats:

- `rawVideoWithSoundFormats`: List of combined video and audio formats.
- `mergeFormats`: List of formats requiring video and audio merging.
- `rawAudioOnlyFormats`: List of audio-only formats.

### Starting a Download

Select a format from the categorized lists and start a download:

```dart
final format = info['rawVideoWithSoundFormats'][0]; // Choose a format
final outputDir = '/storage/emulated/0/Download'; // Ensure this directory exists
final taskId = await client.startDownload(
  format: format,
  outputDir: outputDir,
  url: '<https://youtu.be/nl8o9PsJPAQ>',
  overwrite: false, // Set to true to overwrite existing files
  overrideName: 'MyCustomVideo', // Optional custom filename
);
```

You can control conversion behavior:

- Set `format['downloadAsRaw'] = true` to keep the original format (e.g., WebM instead of MP4).
- Default behavior converts non-MP4 video or non-MP3 audio to standard formats.

### Monitoring Download Progress

Listen to download events for real-time updates:

```dart
client.getDownloadEvents().listen((event) {
  if (event['taskId'] == taskId) {
    if (event['type'] == 'progress') {
      final progress = (event['downloaded'] as int) / (event['total'] as int);
      print('Progress: ${(progress * 100).toStringAsFixed(2)}%');
    } else if (event['type'] == 'state') {
      print('State: ${event['stateName']}');
    }
  }
});
```

### Canceling a Download

Cancel an ongoing download using the task ID:

```dart
await client.cancelDownload(taskId);
```

### Getting the Thumbnail URL

Fetch the thumbnail URL separately if needed:

```dart
final thumbnailUrl = await client.getThumbnailUrl('<https://youtu.be/nl8o9PsJPAQ>');
print('Thumbnail URL: $thumbnailUrl');
```

## Migrating from 0.1.4 to 0.2.0

Version 0.2.0 introduces breaking changes to the API:

- **Old Methods Removed**: Methods like `getAllRawVideoWithSoundFormats` are replaced by `getVideoInfo`, which returns all metadata and categorized formats in one call.
- **Format Access**: Use `info['rawVideoWithSoundFormats']`, `info['mergeFormats']`, or `info['rawAudioOnlyFormats']` to access formats instead of separate method calls.
- **Download Parameters**: The `startDownload` method now takes a `format` map directly from the categorized lists and supports additional options like `overrideName`.
- **Models Simplified**: Format-specific classes (`Format`, `CombinedFormat`, `MergeFormat`) are no longer exposed; formats are handled as dynamic maps.
- Check the [example app](#example) for updated usage patterns.

## Example

The `example/` directory contains a comprehensive demo application showcasing:

- A user interface for entering URLs and selecting formats.
- Real-time progress and state updates.
- Provider-based state management for downloads.

Run the example with:

```bash
cd example
flutter run
```

Refer to `example/lib/main.dart` and related files for integration details.

## License

This plugin is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
