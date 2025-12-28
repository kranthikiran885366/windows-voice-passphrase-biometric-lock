## How to Publish and Share on GitHub

1. Go to your GitHub repository page.
2. Click on "Releases" (right sidebar or top menu).
3. Click "Draft a new release".
4. Upload your `windows_locker.exe` file as a release asset.
5. Add a release title and description, then publish the release.
6. Copy the direct download link for `windows_locker.exe` from the release page.

### Example Download Link
**[Download Windows Locker (.exe) from GitHub Releases](YOUR_GITHUB_RELEASE_LINK_HERE)**


# Windows Locker: Desktop Security App

## How to Build the .exe

1. Make sure Python and pip are installed on your Windows system.
2. Place your custom app icon in `windows/app_icon.ico` (optional, recommended for branding).
3. Open Command Prompt and navigate to your project folder.
4. Run the build script:

    ```bat
    build_windows_exe.bat
    ```

5. After the build completes, your `.exe` file will be located in the `dist/` folder as `windows_locker.exe`.

## How to Run the .exe

1. Go to the `dist/` folder.
2. Double-click the `windows_locker.exe` file to launch the Windows Locker security application.
3. No Python installation is required for end users.

## How to Distribute
- Share the `.exe` file from the `dist/` folder with users.
- Users can download and run the `.exe` directly.
- For best results, compress the `.exe` into a .zip before sharing.

### Download Link
Once you upload the `.exe` file to your website or cloud storage, add the download link here:

**[Download Windows Locker (.exe)](YOUR_DOWNLOAD_LINK_HERE)**

## Notes
- This build is Windows-only and uses PyQt5 for the UI.
- If you add new dependencies, update `requirements.txt` and rebuild.
- For advanced packaging (installer, code signing), see [PyInstaller docs](https://pyinstaller.org/).
