# Forish - Game Shop Web Application

## Overview
Forish is a modern web-based game shop platform built using Flask and SQLite. The application provides a comprehensive gaming marketplace where users can browse, purchase, and manage their digital game library. Through features like user authentication, game reviews, shopping cart functionality, and a robust tagging system, Forish delivers a complete e-commerce experience for gaming enthusiasts.

## Key Features
Forish enables users to fully participate in a digital gaming marketplace. Users begin by registering an account, which gives them access to browse and purchase games from our curated collection. Each user gets their own personal library where they can access their purchased games and manage their collection. The platform includes a sophisticated review system where users can rate games and share their experiences with others. A streamlined shopping cart system makes purchasing multiple games simple and efficient. Users can also easily find games through our search system with tag filtering, and connect with our store through our contact page which includes our physical location and social media presence.

## Technical Architecture

### Database Schema
The application uses SQLite with a carefully designed schema to manage all aspects of the game shop. At its core, the users table stores account information, while the games table maintains our catalog of titles. These are connected through several relationship tables: user_games tracks ownership, reviews stores user feedback, and cart_items manages shopping sessions. The tagging system uses tags and game_tags tables to implement flexible game categorization.

### Core Files and Functionality

#### `app.py`
The main application file serves as the backbone of Forish, handling everything from initial setup to request processing. It configures the Flask application, establishes database connections, and manages user sessions. The file implements route handlers for all major functionality, incorporating security middleware through the login_required decorator. Error handling is comprehensive, ensuring users receive clear feedback when issues arise.

#### Templates
The application's interface is built through a series of thoughtfully designed templates. The layout.html file serves as the foundation, providing consistent navigation and styling across the platform. Game.html delivers detailed views of individual titles, adapting its display based on whether users own the game or have it in their cart. The index.html template creates an engaging shop interface, while library.html gives users quick access to their owned games. Cart.html manages the purchasing process, and contacts.html helps users connect with our physical store.

### Security Measures
Security is a top priority in Forish's implementation. Passwords are protected using Werkzeug's security functions for hashing. The application uses session-based authentication to maintain user states securely. All database queries are parameterized to prevent SQL injection attacks. Template escaping protects against XSS vulnerabilities, while CSRF protection safeguards all forms.

### Design Decisions
The choice of SQLite as our database system prioritizes simplicity and portability while maintaining robust data integrity through foreign key constraints. The user interface leverages Bootstrap for responsive design, enhanced with custom CSS to create a gaming-focused aesthetic. Code organization emphasizes modularity and reusability, with clear separation between routes, templates, and helper functions.

The application's features are implemented with user experience in mind. Cart updates happen asynchronously to prevent page reloads, all forms include server-side validation, and the search system offers flexible filtering options. The tagging system is designed to scale with our growing game catalog.

## Future Improvements
Looking ahead, we plan to enhance Forish with several major features. Payment processing integration will streamline purchases, while user profiles will enable personalized experiences. A recommendation system will help users discover new games, and an administrative interface will simplify content management. We're also exploring integration with external game APIs and implementing performance optimizations for larger catalogs.

## Setup and Installation
Getting Forish running is straightforward. After cloning the repository, install the required dependencies using pip install -r requirements.txt. Initialize the database with flask init-db, set your environment variables for development or production, and launch the application with flask run.

## Technologies Used
Forish is built on a robust stack of modern web technologies. The Flask web framework provides our application structure, while SQLite handles data persistence. Bootstrap 5.3 enables responsive design, with Jinja2 handling template rendering. Dynamic features are implemented in JavaScript, and the Google Maps API powers our store location feature.

This project represents a comprehensive implementation of web development principles, showcasing thoughtful database design and user experience considerations in creating a modern e-commerce platform for digital games.
