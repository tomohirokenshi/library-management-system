# Library Management System

This project, undertaken for the Embedded Systems (CPE16) course, involved the development of a library management system specifically designed for the Laguna State Polytechnic University College of Engineering. The primary objective was to gain practical experience in embedded systems development, specifically exploring the interplay between hardware and software components. 

## System Architecture
* **Microprocessor:** The core of the system utilized a Raspberry Pi single-board computer, serving as the central processing unit. 
* **Sensors:** An RFID reader was employed as the primary sensor for user authentication, leveraging the existing RFID tags embedded in the student and faculty IDs. While, RFID stickers were affixed to each book, enabling the system to identify and track individual library items.
* **Database:** SQLite was chosen as the database management system, providing a lightweight and efficient solution for storing and retrieving system data.
* **Software:** The system was programmed in Python, utilizing the tkinter library to create a user-friendly graphical user interface (GUI) for interaction.

## Key Features
* **User Authentication:** Employs RFID tags for secure and contactless user identification.
* **Database Management:** Utilizes SQLite for storing and managing user and book borrowing data, ensuring data integrity and efficient retrieval.
* **User Management:** Facilitates user registration, profile updates, and potential user restrictions based on predefined criteria.
* **Book Management:** Enables book inventory management, including adding, editing, and deleting book entries.
* **Borrowing and Returning:** Tracks book borrowing and returns using RFID tags, calculating due dates and highlighting approaching deadlines.
* **Graphical User Interface (GUI):** Provides a user-friendly interface for interacting with the system, featuring intuitive elements for managing books, users, and borrowings.
* **Search and Filter Functionality:** Enables efficient searching and filtering of user and book data based on various attributes.
* **Error Handling:** Implements robust error handling mechanisms to address potential issues like duplicate entries, missing data, and database connection errors.
* **Modular Design:** Employs a modular design with well-defined functions, promoting code maintainability and future extensibility.

## Reflections
This project served as a valuable learning experience, providing a practical application of embedded systems concepts. The integration of hardware and software components presented unique challenges, requiring careful consideration of data transfer, signal processing, and error handling. Working with the SQLite database and implementing CRUD operations reinforced the importance of efficient data management within a software system. The project also fostered critical thinking and problem-solving skills as I encountered and overcame various technical hurdles, such as optimizing RFID data processing and ensuring system stability. This hands-on experience has strengthened my understanding of embedded systems development and motivated me to further explore its applications in real-world scenarios. 
