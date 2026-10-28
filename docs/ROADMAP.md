# Roadmap

The plan for CarpoolCampus, built one small, working feature at a time.
Each item is one pull request with code, tests, demo data and documentation.

**Progress: 2 of 80 items complete.**

Legend: ✅ done · 🔨 in this pull request · ⬜ planned · ⏭️ skipped

## Phase 1: Foundation

- ✅ **1.1** Project setup and home page
- ✅ **1.2** About page with privacy summary
- 🔨 **1.3** Friendly 404 and 500 error pages
- ⬜ **1.4** Site-wide settings in templates
- ⬜ **1.5** Mobile navigation menu

## Phase 2: Organizations

- ⬜ **2.1** Organization model and admin
- ⬜ **2.2** Email domains and organization lookup
- ⬜ **2.3** Campus model with postal code validation
- ⬜ **2.4** Seed real Canadian universities
- ⬜ **2.5** Supported organizations page
- ⬜ **2.6** Organization detail page
- ⬜ **2.7** Search and province filter for organizations
- ⬜ **2.8** Request a new organization

## Phase 3: Accounts

- ⬜ **3.1** Member profile model
- ⬜ **3.2** Sign up with organization email
- ⬜ **3.3** Log in and log out
- ⬜ **3.4** Email verification
- ⬜ **3.5** Profile page
- ⬜ **3.6** Edit profile
- ⬜ **3.7** Password reset
- ⬜ **3.8** Seed fake demo members
- ⬜ **3.9** Organization isolation helpers
- ⬜ **3.10** Delete my account

## Phase 4: Timetables

- ⬜ **4.1** Class block model
- ⬜ **4.2** My timetable page
- ⬜ **4.3** Add a class
- ⬜ **4.4** Edit and delete a class
- ⬜ **4.5** Weekly timetable grid
- ⬜ **4.6** Prevent overlapping classes
- ⬜ **4.7** Seed realistic timetables
- ⬜ **4.8** Daily commute times
- ⬜ **4.9** Copy a day's classes
- ⬜ **4.10** Import timetable from CSV

## Phase 5: Matching

- ⬜ **5.1** Home location from postal code
- ⬜ **5.2** Distance between members
- ⬜ **5.3** Demo home locations
- ⬜ **5.4** Shared commute days
- ⬜ **5.5** Match candidates
- ⬜ **5.6** Match score
- ⬜ **5.7** My matches page
- ⬜ **5.8** Filter matches
- ⬜ **5.9** Match detail page
- ⬜ **5.10** Cached match results
- ⬜ **5.11** Faster matching queries
- ⬜ **5.12** Matching preferences

## Phase 6: Carpools

- ⬜ **6.1** Carpool request model
- ⬜ **6.2** Send a carpool request
- ⬜ **6.3** Requests inbox
- ⬜ **6.4** Accept, decline or cancel requests
- ⬜ **6.5** Carpool groups
- ⬜ **6.6** My carpools page
- ⬜ **6.7** Seats and capacity
- ⬜ **6.8** Leave or remove from a carpool
- ⬜ **6.9** Share contact details after acceptance
- ⬜ **6.10** Seed demo carpools

## Phase 7: Auto-reshuffle

- ⬜ **7.1** In-app notifications
- ⬜ **7.2** Mark notifications as read
- ⬜ **7.3** Detect timetable changes
- ⬜ **7.4** Recalculate matches after a change
- ⬜ **7.5** Check carpools still fit schedules
- ⬜ **7.6** Notify members about changes
- ⬜ **7.7** Nightly reshuffle command
- ⬜ **7.8** What changed in my matches

## Phase 8: Organization admin and polish

- ⬜ **8.1** Organization admin role
- ⬜ **8.2** Organization dashboard
- ⬜ **8.3** Manage campuses as org admin
- ⬜ **8.4** Member list for org admins
- ⬜ **8.5** Members per campus chart
- ⬜ **8.6** Rate a carpool partner
- ⬜ **8.7** Show ratings on matches
- ⬜ **8.8** Report a member
- ⬜ **8.9** Block a member
- ⬜ **8.10** REST API basics
- ⬜ **8.11** Timetable API
- ⬜ **8.12** Matches API
- ⬜ **8.13** API documentation page
- ⬜ **8.14** Accessibility improvements
- ⬜ **8.15** Cross-organization matching (opt-in)
- ⬜ **8.16** Production readiness
- ⬜ **8.17** Version 1.0 release

## After v1: continuous improvement

Once every item above is done, the project moves to daily quality work:
fixing bugs, closing security findings, adding missing tests, improving
performance and readability. Progress is tracked in
[QUALITY.md](QUALITY.md).
