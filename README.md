# Library Management System

This project, undertaken for the Embedded Systems (CPE16) course, involved the development of a library management system specifically designed for the Laguna State Polytechnic University College of Engineering. The primary objective was to gain practical experience in embedded systems development, specifically exploring the interplay between hardware and software components. 

**System Architecture:**
* **Microprocessor:** The core of the system utilized a Raspberry Pi single-board computer, serving as the central processing unit. 
* **Sensors:** An RFID reader was employed as the primary sensor for user authentication, leveraging the existing RFID tags embedded in the student and faculty IDs. While, RFID stickers were affixed to each book, enabling the system to identify and track individual library items.
* **Database:** SQLite was chosen as the database management system, providing a lightweight and efficient solution for storing and retrieving system data.
* **Software:** The system was programmed in Python, utilizing the tkinter library to create a user-friendly graphical user interface (GUI) for interaction.

**Key Features:**
* **User Authentication:** Employs RFID tags for secure and contactless user identification.
* **Database Management:** Utilizes SQLite for storing and managing user and book borrowing data, ensuring data integrity and efficient retrieval.
* **User Management:** Facilitates user registration, profile updates, and potential user restrictions based on predefined criteria.
* **Book Management:** Enables book inventory management, including adding, editing, and deleting book entries.
* **Borrowing and Returning:** Tracks book borrowing and returns using RFID tags, calculating due dates and highlighting approaching deadlines.
* **Graphical User Interface (GUI):** Provides a user-friendly interface for interacting with the system, featuring intuitive elements for managing books, users, and borrowings.
* **Search and Filter Functionality:** Enables efficient searching and filtering of user and book data based on various attributes.
* **Error Handling:** Implements robust error handling mechanisms to address potential issues like duplicate entries, missing data, and database connection errors.
* **Modular Design:** Employs a modular design with well-defined functions, promoting code maintainability and future extensibility.

**Learning Outcomes:**

* **Embedded Systems Fundamentals:** Gained practical experience in working with a microprocessor (Raspberry Pi) and integrating hardware (RFID reader) with software.
* **Database Management:** Learned to utilize SQLite for data storage and retrieval, implementing CRUD (Create, Read, Update, Delete) operations for efficient data management.
* **Python Programming:** Enhanced proficiency in Python programming, including GUI development using the tkinter library and database interaction with SQLite.
* **System Design and Development:** Developed a comprehensive understanding of the system design process, from conceptualization and hardware selection to software implementation and testing.
* **[Add other learning outcomes]**
