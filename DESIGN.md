# Cappa Car Rentals — Design Document

**Author:** Chenul Methsuka Ranasinghe

## Overview

Cappa Car Rentals is a Python command-line application connected to a MySQL database. It manages the core operations of a vehicle rental business.

## Design Decisions

**Python:** Used for application logic, menu navigation, and user interaction because of its simplicity and readability.

**MySQL:** Used for persistent storage and relational data management.

**Relational database:** Five tables (`admin`, `users`, `customers`, `vehicles`, and `rentals`) separate the different entities and maintain relationships through primary and foreign keys.

**Command-line interface:** Chosen to keep the application straightforward while focusing on functionality and database operations.

## Implementation

The Python application handles authentication, vehicle management, customer records, rentals, returns, and receipts.

The SQL file creates the database structure and inserts sample records. Python communicates with MySQL using `mysql-connector-python`.

## Future Improvements

- Password hashing and improved credential security.
- Better input validation and error handling.
- Improved transaction management.
- A graphical or web-based interface.
- Automated testing.

## AI Disclosure

ChatGPT was used to assist with code review, troubleshooting, and drafting project documentation. The original application source code was written by me. I reviewed the documentation and remain responsible for understanding and explaining the implementation.
