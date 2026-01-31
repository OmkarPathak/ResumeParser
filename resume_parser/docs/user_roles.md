# User Role Guide

This document outlines the capabilities and workflows for each user role in the Resume Parser system.

## 1. Candidate
*The job seeker.*

**Capabilities:**
*   **Registration**: Sign up with "Candidate" role.
*   **Profile Management**:
    *   Upload Resume (Drag & Drop).
    *   Automatic Profile Creation from Resume (Parsing).
    *   View/Edit Profile Details.
    *   View AI Summary and Strengths.
*   **Job Application**:
    *   Browse Open Jobs.
    *   Apply to jobs (Tracking status: Applied, Interviewing, Hired, etc).
*   **Onboarding**: 
    *   If a Recruiter uploaded their resume previously, the system attempts to "Claim" the existing profile based on email match during onboarding.

**Workflow:**
1.  Register -> Login -> Dashboard (Onboarding if no profile).
2.  Upload Resume -> Review Parsed Data.
3.  Go to "Open Jobs" -> Click "Apply".

---

## 2. Recruiter
*The primary operator managing candidates and jobs.*

**Capabilities:**
*   **Candidate Management**:
    *   View full "Candidate Database" (Table/Card view).
    *   Upload Candidates (individually).
    *   Edit Candidate details.
    *   *Delete Candidates* (Permission granted).
    *   Search/Filter Candidates (by name, skill, tag).
*   **Job Management**:
    *   Create Jobs for Clients.
    *   View/Edit Jobs.
    *   Track Applications per Job.
*   **Interview Management**:
    *   Schedule Interviews (upcoming feature).
*   **Dashboard**:
    *   View key metrics (Total Candidates, Open Jobs).

**Workflow:**
1.  Login -> Dashboard (Resume List).
2.  "Upload New" -> Add candidate manually.
3.  "Create Job" -> Define job specs for a Client.

---

## 3. Client
*The external company hiring for positions.*

**Capabilities:**
*   **Job Viewing**:
    *   View *only* jobs associated with their Client account.
    *   View Applications for their jobs.
*   **Status Tracking**:
    *   See which candidates are "Shortlisted" or "Hired".
*   **Invoicing**:
    *   View Invoices (upcoming feature).

**Workflow:**
1.  Login -> Dashboard (Job List).
2.  Click Job -> View Applicants.

---

## 4. Admin
*System administrator.*

**Capabilities:**
*   **Full Access**:
    *   Manage Users (Create/Delete Recruiters, Clients).
    *   Manage all Candidates and Jobs.
    *   Access Django Admin Panel.
*   **Configuration**:
    *   Manage System Settings.

**Workflow:**
*   Standard Admin operations via `/admin/` or the main dashboard.
