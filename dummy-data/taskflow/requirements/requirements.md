# TaskFlow Software Requirements

## REQ-001 — User Registration

Users must be able to create an account using:

- Full name
- Email address
- Password

The system must reject duplicate email addresses.

Passwords must contain at least 8 characters.


## REQ-002 — User Login

Registered users must be able to log in using their email address and password.

Invalid credentials must be rejected.


## REQ-003 — Password Reset

Users must be able to request a password reset using their registered email address.

The system must send a password reset link.

The password reset token must expire after 15 minutes.


## REQ-004 — Create Task

Authenticated users must be able to create tasks.

Each task must contain:

- Title
- Description
- Due date
- Priority

Priority must be one of:

- LOW
- MEDIUM
- HIGH


## REQ-005 — Delete Task

Authenticated users must be able to delete their own tasks.

Users must not be able to delete tasks belonging to another user.


## REQ-006 — Task Search

Users must be able to search their tasks using the task title.


## REQ-007 — Login Audit

Every successful login must create an audit record containing:

- User ID
- Login timestamp
- IP address