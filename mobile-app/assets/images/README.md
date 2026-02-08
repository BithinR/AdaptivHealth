# Image Assets

This directory contains background images for the AdaptivHealth mobile app.

## Images

### login_background.jpg
- **Size**: 1080x1920 px (21 KB)
- **Usage**: Login screen background
- **Theme**: Professional medical - deep blue to light blue gradient
- **Colors**: #1e3a8a → #2563EB → #3b82f6

### dashboard_background.jpg
- **Size**: 1080x1920 px (16 KB)  
- **Usage**: Patient dashboard background
- **Theme**: Calming wellness - very light to soft blue gradient
- **Colors**: #f0f9ff → #dbeafe → #bfdbfe

## Image Generation

These images were generated programmatically using Python/Pillow to create smooth gradient backgrounds optimized for mobile devices. The images are stored locally in the repository as JPEG files with:
- Good quality (90% JPEG quality)
- Optimized file size (< 25 KB each)
- Mobile-optimized resolution (1080x1920)
- Smooth gradients with blur for professional look

## Usage in Flutter

Images are referenced in the app using AssetImage:

```dart
decoration: BoxDecoration(
  image: DecorationImage(
    image: AssetImage('assets/images/login_background.jpg'),
    fit: BoxFit.cover,
  ),
)
```

## Note

All images are stored locally in this repository. No external URLs or file paths are used.
