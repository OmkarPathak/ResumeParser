# User Roles & Access Control Guide

This system uses a Role-Based Access Control (RBAC) model with four primary roles.

## 1. Consultant / Admin (Owner)
- **Role Code**: `ADMIN`
- **Access**: Full system access.
- **Responsibilities**:
    - Manage all users (Recruiters, Clients, Candidates).
    - Configure system settings.
    - View global reports and analytics.
    - Oversee all jobs and submissions.

## 2. Recruiter
- **Role Code**: `RECRUITER`
- **Access**: Execution-level access.
- **Responsibilities**:
    - **Client Management**: Create and manage client profiles.
    - **Job Management**: Create jobs, post them, and manage their lifecycle.
    - **Candidate Sourcing**: Add candidates, parse resumes, and screen profiles.
    - **Submissions**: Submit candidates to clients and track interviews.
    - **Dashboard**: View personal performance metrics.

## 3. Client
- **Role Code**: `CLIENT`
- **Access**: Restricted access to their own jobs and candidates.
- **Responsibilities**:
    - **Job Requests**: Create new job requisitions (require approval).
    - **Candidate Review**: View screened candidate profiles submitted by recruiters.
    - **Feedback**: Provide feedback on candidates (Shortlist, Reject, Interview).
    - **Transparency**: View status of open positions.

## 4. Candidate
- **Role Code**: `CANDIDATE`
- **Access**: Limited personal profile.
- **Responsibilities**:
    - **Profile Management**: Update resume and personal details.
    - **Job Application**: Apply to open positions (if public portal enabled).
    - **Status Tracking**: View application status.

## Workflow Overview
1.  **Admin/Recruiter** adds a **Client**.
2.  **Client** or **Recruiter** creates a **Job**.
3.  **Recruiter** sources a **Candidate** (adds resume).
4.  **Recruiter** screens and **Submits** candidate to **Job**.
5.  **Client** reviews and provides feedback.
6.  **Admin** oversees the process and handles **Invoicing**.
