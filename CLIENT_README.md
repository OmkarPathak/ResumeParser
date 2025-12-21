# Resume Parser Application

This is a portable version of the Resume Parser application for macOS.

## Installation
1. Download the zip file to your macOS machine.
2. Unzip it to a location of your choice (e.g., Desktop or Documents).
3. Open the unzipped folder `ResumeParser`.

## ⚠️ Important: First Time Setup (Fix "App is Damaged" Error)
Mac security (Gatekeeper) often flags apps downloaded from the internet as "damaged" or "unidentified". You **MUST** run the fix command below before starting the app.

### Method 1: The Easy Fix Script
1. Inside the folder, look for **`fix_permissions.command`**.
2. **Right-click** (or Control-click) on it.
3. Select **Open**.
4. Click **Open** again in the dialog box.
5. A terminal will flash and close. The app is now fixed.

### Method 2: Manual Terminal Fix (If Method 1 fails)
1. Open the "Terminal" app on your Mac (Command+Space and type Terminal).
2. Type `xattr -cr ` (make sure there is a space at the end).
3. Drag and drop the `ResumeParser` folder from Finder into the Terminal window.
4. It should look like: `xattr -cr /Users/username/Desktop/ResumeParser`
5. Press **Enter**.

---

## How to Run the App
Once you have done the First Time Setup:
1. Inside the folder, locate **`run_portable_app.command`**.
2. Double-click to run it. 
   *(If it still says "Unidentified Developer", Right-click > Open > Open).*
3. A terminal window will open. **Do not close this window**.
4. Wait about **30 seconds**.
5. Your browser will open automatically to `http://127.0.0.1:8000`.

## Using the App
- **Upload Resume**: Go to the Home page to upload new resumes.
- **View Data**: Click "Data" to view and export the history.
- **Stop**: Close the terminal window.

## Troubleshooting
- **"Python3.framework is damaged"**: This means you didn't run the First Time Setup. Run the `fix_permissions.command` or the manual `xattr` command above.
- **Browser doesn't open**: Manually open Safari/Chrome and go to `http://127.0.0.1:8000`.
