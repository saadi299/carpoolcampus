# Campus Management Guide

This guide explains how organization administrators view and manage campuses associated with an educational institution in CarpoolCampus.

## Overview

Each organization registered in CarpoolCampus can have one or more physical campuses (for example, *Main Campus*, *St. George*, or *Mississauga*). Every campus includes street address details, a validated Canadian postal code, and precise geographic coordinates (latitude and longitude) used for carpool route matching.

---

## Viewing Campuses for an Organization

To view campuses configured for an organization:

1. Log in to the Django Admin interface at `/admin/` using an administrative account (e.g., `admin@utoronto.ca`).
2. In the navigation sidebar, click on **Organizations** under the **ORGANIZATIONS** header.
3. Select the organization you wish to manage from the list (e.g., **University of Toronto**).
4. Scroll down to the **Campuses** inline section at the bottom of the organization detail page.

---

## Adding a New Campus

To add a campus to an existing organization:

1. Open the target **Organization** detail page in the admin portal.
2. In the **Campuses** section, locate the blank row at the bottom of the list.
3. Enter the following required details:
   - **Name**: A descriptive name for the campus (e.g., `St. George Campus`).
   - **Address**: The street address (e.g., `27 King's College Circle`).
   - **Postal code**: A valid Canadian postal code (e.g., `M5S 1A1` or `m5s1a1`). The system automatically converts the entry to upper-case with a single space.
   - **Lat**: Latitude coordinate in decimal degrees (e.g., `43.662892`).
   - **Lng**: Longitude coordinate in decimal degrees (e.g., `-79.395656`).
4. Click **Save** at the bottom of the page.

---

## Direct Campus Administration

You can also view and edit campuses directly from the dedicated Campuses admin list:

1. Navigate to `/admin/organizations/campus/`.
2. Use the search bar to search by campus name, address, postal code, or organization name.
3. Click on any campus entry to update its address, coordinates, or postal code.
4. Click **Save**.

---

## Validation & Business Rules

- **Unique Campus Names**: Each campus name must be unique within an organization. Two campuses in the same organization cannot share the exact same name.
- **Postal Code Validation**: Postal codes must be valid Canadian postal codes in `A1A 1A1` format. Postal codes containing invalid letters (such as D, F, I, O, Q, U, or W/Z as initial characters) are rejected automatically with a clear error message.
- **Coordinate Precision**: Geographic coordinates accept up to 6 decimal places (e.g., `43.472285`), ensuring accurate proximity calculations for carpool matches.
