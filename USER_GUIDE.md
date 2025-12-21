# Resume Parser Application - User Guide

## Prerequisites
- **macOS**: This application is optimized for macOS.
- **Python 3**: macOS usually comes with Python 3 installed. If not, please install it from [python.org](https://www.python.org/downloads/).

## How to Run the Application

1.  **Locate the Folder**: Open the folder containing these files.
2.  **Run the Script**: Double-click on the file named `run_app.command`.
3.  **Wait for Setup**: A terminal window will open.
    - If it's the first time, it might take a few minutes to install necessary libraries.
    - You will see text scrolling in the terminal. This is normal.
4.  **Start Using**: Once the setup is complete, your default web browser will automatically open the application at `http://127.0.0.1:8000`.

## How to Use Features

### Uploading Resumes
- Go to the **Home** page.
- Select one or more Resume files (PDF, DOCX).
- Optionally add a **Tag** (e.g., "Developer", "HR").
- Click **Upload**.

### Viewing Data
- Click on **Data** in the top navigation bar.
- You will see a list of all uploaded resumes.

### Searching and Filtering
- **Search**: Use the search bar to find resumes by Name, Email, or Skills.
- **Filter**: Use the dropdown menu to filter resumes by specific *Tags*.

### Editing Resumes
- Click the **Edit** button next to any resume.
- You can update their details or add a **Remark**.
- Click **Update** to save.

### Exporting Data
- On the **Data** page, click **Export to Excel (CSV)**.
- A file named `resumes.csv` will downloaded, which you can open in Excel or Numbers.

## Troubleshooting
- **Terminal says "Permission denied"**:
  - Open terminal and run: `chmod +x run_app.command` inside the folder.
- **Browser doesn't open**:
  - Manually open your browser and go to `http://127.0.0.1:8000`.
- **To Stop the App**:
  - Close the Terminal window.
