# MailMind AI

AI-powered Gmail productivity assistant with Telegram integration, multi-account support, email intelligence, task extraction, calendar automation, AI drafting, and scheduled reports.

---

# Overview

MailMind AI connects one or more Gmail accounts to a Telegram bot and automatically:

* Monitors incoming emails
* Analyzes email content using AI
* Categorizes and prioritizes emails
* Extracts tasks and events
* Generates AI summaries
* Creates draft replies
* Sends daily and weekly reports
* Supports multiple Gmail accounts per user
* Allows account switching through Telegram

Everything is controlled directly from Telegram.

---

# Core Features

## Gmail Integration

* OAuth2 authentication
* Multiple Gmail accounts per user
* Secure token storage
* Automatic email synchronization
* Gmail account switching

## AI Email Analysis

Every email is analyzed and classified into:

* WORK
* PERSONAL
* NEWSLETTER
* PROMOTION
* ACCOUNT
* AI_NEWS
* IMPORTANT
* OTHER

Additional metadata:

* Priority
* Confidence Score
* Action Required
* Short Summary
* Detailed Summary

## Telegram Assistant

Interact entirely through Telegram.

Commands:

### Account Management

```text
/start
/accounts
/use <email>
```

### Email Search

```text
/recent
/today
/important
/urgent
```

### AI Search

```text
/ask <question>
```

Examples:

```text
/ask Which emails mention internships?

/ask Show me emails related to AI agents.

/ask What important emails arrived today?
```

### Draft Workflow

```text
/draft <number>
```

Reply actions:

```text
/accept
/decline
/askdetails
/custom <message>
/sendlast
```

### Tasks

```text
/tasks
/done <number>
```

### Calendar

```text
/events
/todayevents
```

---

# Architecture

```text
Telegram User
      |
      v
Telegram Bot
      |
      v
Telegram Command Agent
      |
      +------------------+
      |                  |
      v                  v
AI Services        Search Services
      |                  |
      +---------+--------+
                |
                v
            Supabase
                |
                v
        Gmail + Calendar
```

---

# Database Design

## users

Stores platform users.

```text
id
email
telegram_chat_id
active_gmail_account_id
created_at
```

Purpose:

* Maps Telegram users to MailMind users
* Stores active Gmail account selection

---

## gmail_accounts

Stores connected Gmail accounts.

```text
id
user_id
gmail_address
access_token
refresh_token
connected
```

Purpose:

* Multi-account Gmail support
* OAuth credential storage

Relationship:

```text
One User
    |
    +----> Multiple Gmail Accounts
```

---

## emails

Stores synchronized emails.

```text
id
user_id
gmail_account_id
gmail_message_id
subject
sender
body
received_at
processed
```

Purpose:

* Email persistence
* Multi-account email ownership

---

## email_analysis

Stores AI analysis results.

```text
id
gmail_message_id
user_id
gmail_account_id
category
priority
summary
short_summary
detailed_summary
confidence
action_required
calendar_processed
task_processed
```

Purpose:

* AI understanding layer
* Search and filtering

Important:

```text
user_id
gmail_account_id
```

must always be populated.

These fields enable multi-account filtering.

---

## tasks

Stores extracted tasks.

```text
id
gmail_account_id
title
description
completed
created_at
```

---

## calendar_events

Stores extracted events.

```text
id
gmail_account_id
title
start_time
end_time
```

---

## draft_sessions

Stores draft workflow state.

```text
id
user_id
gmail_message_id
email_index
draft_id
created_at
```

Purpose:

* Enables /accept
* Enables /decline
* Enables /askdetails
* Enables /custom

Important:

```text
draft_id
```

must exist.

---

# Multi-Account Architecture

## Problem

Originally:

```text
1 User
=
1 Gmail
```

This prevented account switching.

---

## Solution

Added:

```text
users.active_gmail_account_id
```

Current architecture:

```text
User
 |
 +---- Gmail A
 |
 +---- Gmail B
 |
 +---- Gmail C
```

Only one Gmail account is active at a time.

---

## Account Switching

Telegram:

```text
/use email@gmail.com
```

Updates:

```text
users.active_gmail_account_id
```

All commands automatically use:

```text
active_gmail_account_id
```

Examples:

```text
/recent
/draft
/ask
/tasks
/events
```

operate on the currently selected Gmail account.

---

# OAuth Flow

## Login

```text
/start
```

Telegram sends:

```text
/auth/google?chat_id=<telegram_chat_id>
```

---

## Callback

Flow:

```text
Google OAuth
      |
      v
Fetch Gmail Profile
      |
      v
Find User by Telegram Chat ID
      |
      v
Save Gmail Account
      |
      v
Auto-select first Gmail Account
```

Important:

Users are identified by:

```text
telegram_chat_id
```

NOT by Gmail address.

This allows:

```text
One Telegram User
    |
    +---- Multiple Gmail Accounts
```

---

# Email Sync Pipeline

Scheduler:

```text
EmailMonitorAgent
```

Flow:

```text
Fetch Gmail Messages
      |
      v
Check Existing Message
      |
      v
Save Email
      |
      v
Mark Processed
```

Duplicate emails are skipped.

---

# AI Analysis Pipeline

```text
EmailAnalyzerAgent
```

Flow:

```text
Unprocessed Emails
      |
      v
AI Analysis
      |
      v
Category
Priority
Summary
Action Required
      |
      v
Save Analysis
```

Ownership fields saved:

```text
user_id
gmail_account_id
```

---

# Draft Reply Pipeline

```text
/ draft 2
```

Flow:

```text
Select Email
      |
      v
Create Draft Session
      |
      v
Choose Reply Type
      |
      +---- /accept
      |
      +---- /decline
      |
      +---- /askdetails
      |
      +---- /custom
      |
      v
Generate AI Draft
      |
      v
Store Draft
      |
      v
/sendlast
      |
      v
Send Gmail Reply
```

---

# Scheduler Architecture

Runs automatically.

## EmailMonitorAgent

```text
Sync Gmail
```

---

## EmailAnalyzerAgent

```text
Analyze Emails
```

---

## TaskExtractorAgent

```text
Extract Tasks
```

---

## EventExtractorAgent

```text
Extract Calendar Events
```

---

## TelegramReportAgent

```text
Daily Telegram Summary
```

---

## WeeklyReportAgent

```text
Weekly Report
```

---

## Reminder Agents

```text
Task Reminder
Calendar Reminder
```

---

# Deployment

## Single Service Deployment

Uses:

```text
start.py
```

Starts:

```text
FastAPI
Telegram Bot
Scheduler
```

Architecture:

```text
start.py
    |
    +---- FastAPI
    +---- Telegram Bot
    +---- Scheduler
```

---

# Environment Variables

```env
SUPABASE_URL=
SUPABASE_KEY=

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

GOOGLE_REDIRECT_URI=

TELEGRAM_BOT_TOKEN=

BACKEND_URL=
```


The system dynamically maps users using:

```text
telegram_chat_id
```

---

# Key Lessons Learned

1. Multi-account support requires ownership fields everywhere.
2. Gmail accounts should belong to users, not emails.
3. Telegram chat ID is the primary user identity.
4. Active Gmail account selection simplifies all commands.
5. AI analysis records must store gmail_account_id.
6. Draft workflows require persistent session storage.
7. OAuth callbacks must attach Gmail accounts to existing Telegram users.
8. Deduplication is essential during email synchronization.
9. Scheduler, Telegram Bot, and API can run inside a single deployment service.
10. Every feature should filter using active_gmail_account_id for true multi-account support.

---

# Future Improvements

* Incremental Gmail sync using History API
* Email embeddings and vector search
* Voice commands in Telegram
* Smart reminders
* Team/shared inbox support
* Web dashboard
* Analytics and productivity insights
* Auto-generated daily agenda
* AI email triage
* Autonomous email assistant

---

# Author

MailMind AI

AI-powered Gmail Intelligence Assistant with Multi-Account Telegram Control.
