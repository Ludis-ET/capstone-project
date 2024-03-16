# Library Manegement System - Django Capstone Project

## Project Overview
This Django Capstone Project is designed to manage a library system efficiently and effectively. It encompasses key functionalities such as CRUD operations, user authentication, and intricate database relationships to provide a seamless experience for both administrators and students.

## Features

### User Authentication
- **Registration & Login**: Secure user registration and login process.
- **Role Differentiation**: Distinct roles for students, admins, and super admins.
- **Privilege Control**: Restrict book management capabilities to admins and super admins.
- **Super Admin Specials**: Super admins can create new admins and restrict student access.

### Book Management
- **Book Model**: A robust model with attributes like title, author, genre, and status.
- **CRUD Operations**: Full suite of book management tools for admins and super admins.
- **Access Control**: Only authorized personnel can modify book details.

### Reviews and Ratings
- **Student Interaction**: Students can review and rate books they have borrowed.
- **Rating Display**: Each book shows an average rating based on student feedback.

### Search & Filters
- **Book Search**: An intuitive search function for finding books.
- **Advanced Filters**: Genre, author, and status filters to refine searches.

### Borrowing Books
- **Borrowing Limit**: Students are limited to borrowing 3 books at a time.
- **Tracking System**: Monitor which books are borrowed and by whom.

## Requirements
The project requires the following:
- Django framework for backend operations.
- A relational database system for storing user and book information.
- Frontend technology  for a user interface.


