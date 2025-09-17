# EduNexus Learning Management System

## Project Overview
A comprehensive multi-tenant Learning Management System built with Django REST Framework backend and React TypeScript frontend. The system supports institutional hierarchies, role-based access control, and core LMS functionality including assignments, attendance tracking, and grading.

## Recent Changes (2025-09-17)
- ✅ Set up Django backend with comprehensive models (User, Institute, Program, Branch, Semester, etc.)
- ✅ Implemented JWT-based authentication APIs with user registration and login
- ✅ Created React frontend with TypeScript, Tailwind CSS, and authentication system
- ✅ Set up role-based routing and protected routes
- ✅ Configured development workflows for both backend (port 8000) and frontend (port 5000)
- ✅ Established complete project structure following the technical specification

## Architecture

### Backend (Django REST Framework)
- **Port**: 8000
- **Database**: PostgreSQL with comprehensive academic hierarchy models
- **Authentication**: JWT tokens with SimpleJWT
- **Apps**: 
  - `core`: User management, authentication, institutes, roles
  - `academics`: Academic hierarchy (Programs, Branches, Semesters, Subjects)
  - `courses`: Course offerings, enrollments, assignments, attendance

### Frontend (React + TypeScript)
- **Port**: 5000
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **State Management**: React Context API for authentication
- **Routing**: React Router v6 with protected routes
- **API Client**: Axios with JWT token handling

## User Preferences
- Focused on building exactly what was specified in the technical brief
- Emphasis on comprehensive data models and clean architecture
- Full-stack TypeScript/Python implementation with modern tooling

## Project Architecture
The system follows a hierarchical academic structure:
- **Institute** → **Program** → **Branch** → **Academic Year** → **Semester** → **Subject**
- **Course Offerings** link subjects with faculty and semesters
- **Students** enroll in course offerings and submit assignments
- **Attendance** and **Grading** systems track academic progress

## Current Status
Phase 1 (Core Setup & Auth) is complete with:
- Multi-tenant database schema
- JWT authentication system
- React frontend with authentication flow
- Basic dashboard interface
- Development workflows running

## Next Steps
- Academic hierarchy management interface
- Course creation and enrollment system
- Assignment submission and grading functionality
- Attendance tracking interface
- Role-based permissions and access control