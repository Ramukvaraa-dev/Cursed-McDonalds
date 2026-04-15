# AppImage (optional)

PyInstaller already produces a self-contained folder in `dist/Cursed McDonalds/`.

If you want a single-file Linux artifact, wrap it as an **AppImage**.

Typical steps (on Linux):
1. Build with `bash packaging/linux/build.sh`
2. Install `appimagetool` (from the AppImage project)
3. Create an AppDir structure:
   - `AppDir/AppRun` (launches `Cursed McDonalds`)
   - `AppDir/usr/bin/` (contains the PyInstaller output)
   - `AppDir/usr/share/applications/` (desktop file)
   - `AppDir/usr/share/icons/hicolor/256x256/apps/` (icon)
4. Run `appimagetool AppDir`

This repo includes a desktop entry template at `packaging/linux/appimage/CursedMcDonalds.desktop`.

