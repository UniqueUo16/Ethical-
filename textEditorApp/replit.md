# TextPro Suite

## Overview

TextPro Suite is a web-based text processing application that provides professional text manipulation tools for writers, students, and businesses. The application is built as a single-page application with a Flask backend providing API endpoints for text processing operations. Currently, it implements case conversion functionality with support for uppercase, lowercase, title case, and sentence case transformations.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

**Authentication System**
- User authentication using Replit OAuth for secure login
- Flask-Login integration for session management
- PostgreSQL database for user data storage
- Protected API endpoints requiring authentication
- Landing page for unauthenticated users with login flow

**Frontend Architecture**
- Single-page application using vanilla JavaScript with Bootstrap for UI components
- Tool-based navigation system that dynamically shows/hides different text processing sections
- Real-time text processing with immediate feedback to users
- Responsive design using Bootstrap's grid system and dark theme
- Client-side text counting and statistics display
- User-specific interface with logout functionality

**Backend Architecture**
- Flask web framework with Flask-SQLAlchemy for database operations
- RESTful API design for text processing operations
- Authenticated request handling with JSON API endpoints
- Error handling and logging for debugging and monitoring
- ProxyFix middleware for proper handling behind reverse proxies
- Database models for user management and OAuth tokens

**Frontend Components**
- Navigation system with tool switcher using Bootstrap nav pills
- Text input areas with real-time character counting
- Button groups for different case conversion options
- Statistics display for text analysis
- Feather icons for enhanced UI experience

**API Design**
- POST `/api/convert-case` - Handles text case conversion with support for multiple case types
- JSON request/response format for all API interactions
- Comprehensive error handling with appropriate HTTP status codes

**Styling and UI**
- Bootstrap-based responsive design with custom CSS enhancements
- Dark theme implementation for better user experience
- Custom styling for cards, forms, and navigation elements
- Consistent visual hierarchy and spacing

## External Dependencies

**Frontend Libraries**
- Bootstrap CSS framework via CDN for responsive UI components
- Feather Icons library for consistent iconography
- Bootstrap JavaScript components for interactive elements

**Backend Libraries**
- Flask web framework for HTTP request handling
- Flask-SQLAlchemy for database operations and ORM
- Flask-Login for user session management
- Flask-Dance for OAuth authentication with Replit
- PyJWT for JSON Web Token handling
- psycopg2-binary for PostgreSQL database connectivity
- Werkzeug ProxyFix for reverse proxy compatibility
- Python's built-in regex library for text processing operations

**Development Tools**
- Python logging module for application monitoring
- Environment variable support for configuration management

**Database Architecture**
- PostgreSQL database with User and OAuth tables
- User authentication data storage (ID, email, profile info)
- OAuth token management for secure session handling
- Database migrations and schema management

**Hosting Requirements**
- Python runtime environment
- PostgreSQL database access
- Static file serving capability for CSS and JavaScript assets
- Template rendering support for Jinja2 templates
- Environment variables for database and authentication configuration