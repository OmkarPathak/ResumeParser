# User Workflows Guide

This document defines the standard operating procedures and workflows for each user role in the Resume Parser system.

## 1. Recruiter Workflows

Recruiters are the primary operators of the system, acting as the bridge between candidates and clients.

### A. Onboarding a New Candidate
1.  **Navigate to Candidates**: Click on the **Candidates** link in the sidebar.
2.  **Add Candidate**: Click the **+ Add Candidate** button in the top right.
3.  **Upload Resume**: 
    -   Fill in potential basic details (Name, Email) if known.
    -   Upload the candidate's Resume (PDF/DOCX).
    -   The system will automatically **parse** the resume to extract Experience, Skills, and Contact Info.
4.  **Review Profile**: After upload, you will be redirected to the **Candidate Detail** page. Review the parsed data and edit if necessary.

### B. Creating a Job Opening
1.  **Navigate to Jobs**: Click on **Jobs** in the sidebar.
2.  **Create Job**: Click **+ Create Job**.
3.  **Fill Job Details**:
    -   **Title**: Job role title (e.g., Senior Python Developer).
    -   **Client**: Select the hiring Client.
    -   **Description**: Paste the JD. The AI Matcher uses this for scoring.
    -   **Status**: Set to `OPEN`.
4.  **Save**: The job is now live and ready for candidate submissions.

### C. Submitting a Candidate to a Job
1.  **Go to Candidate Profile**: Open the profile of the candidate you wish to submit.
2.  **Locate "Applied Jobs"**: Scroll to the "Applied Jobs" section.
3.  **Select Job**: Use the dropdown to select an active Job Opening.
4.  **Submit**: Click **Apply**. The candidate is now linked to the job, and the Client can see them.

---

## 2. Client Workflows

Clients use the portal to view progress on their open positions and review submitted candidates.

### A. Reviewing Submitted Candidates
1.  **Navigate to Jobs**: Click on **My Jobs** in the sidebar.
2.  **Select Job**: Click on the Title of the job you want to check.
3.  **View Applicants**: Scroll to the "Applicants" or "Submissions" section.
4.  **Action**: You can view the candidate's resume and providing status updates (e.g., Shortlist, Reject) will be a feature in Phase 3.

### B. Requesting a New Job
1.  **Navigate to Jobs**: Click **My Jobs**.
2.  **Create Request**: Click **+ Post Job**.
3.  **Details**: Enter the Job Title and Description.
4.  **Submission**: This creates a Job with `PENDING` status, alerting the Recruiter to review and approve it.

---

## 3. Candidate Workflows

Candidates have a streamlined view focused on their personal profile and applications.

### A. Profile Completion (One-Time)
1.  **Registration**: Sign up via the Register page.
2.  **Onboarding Wizard**: 
    -   The first time you login, you are directed to the Onboarding page.
    -   **Upload Resume**: Upload your CV to auto-fill your profile.
3.  **Verification**: You will land on your **Candidate Profile**. Ensure all details (Skills, Experience) are accurate.

### B. Tracking Applications
1.  **My Profile**: Your dashboard is your Profile page.
2.  **Applied Jobs**: This section lists all jobs you have been submitted to, along with their current status (e.g., Applied, Interviewing, Hired).
3.  **Update Profile**: Click **Edit Profile** to update your resume or contact details at any time.

---

## 4. Admin Workflows

Admins have full access to all above workflows but primarily focus on System Management.

### A. Managing Users
1.  **Access Admin Panel**: Navigate to `/admin` (Django Admin).
2.  **Users**: Create/Edit Users and assign Roles (`RECRUITER`, `CLIENT`, `ADMIN`).
3.  **Clean Up**: Delete duplicate candidates or invalid job postings.
