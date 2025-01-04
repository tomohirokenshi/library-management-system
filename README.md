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

## Dependencies
* **Python:** The primary programming language for the system.
* **tkinter:** Python's standard GUI library for creating the user interface.
* **sqlite3:** Python library for interacting with SQLite databases.
* **RPi.GPIO:** Python library for controlling GPIO pins on the Raspberry Pi, used for interfacing with the RFID reader.
* **mfrc522:** Python library for interacting with the MFRC522 RFID reader module.
* **pandas:** Python library for data manipulation and analysis.
* **datetime:** Python library for working with dates and times.
* **PIL (Pillow):** Python Imaging Library for image processing and display.
* **smtplib:** Python library for sending emails. 

## Recommendations:
**Automated Book Data Entry:**
 * In this project, the book information is manually typed in the system, which is kind of a tedious process for the librarian or faculty handling the system. 
 * **Recommendation:** Image processing could help in making this process easier. Reading and analyzing the text on the book cover can significantly speed up data entry, and the system could allow for minimal manual editing to correct any errors.
**Real-time Clock Implementation:**
 * The project struggles with real-time accuracy. Our testing revealed that shutting down the Raspberry Pi resets the computer's time, requiring manual time and date adjustments each time the system is powered on. 
 * **Recommendation:** Integrate a Real-Time Clock (RTC) module with the Raspberry Pi. This dedicated hardware component maintains accurate time and date even during power outages, ensuring reliable timekeeping for the library system. 
**Remote Access and User Authentication:**
 * The current system is limited to local usage on the Raspberry Pi, restricting its accessibility. 
 * **Recommendations:**
     * **Cloud Deployment:** Explore deploying the system on a cloud platform (e.g., AWS, Google Cloud, or a more affordable option like Heroku) to enable remote access.
     * **Username and Password Authentication:** Implement username and password authentication alongside RFID for enhanced security and to allow students to access their profiles remotely.
     * **Mobile App Development:** Develop a mobile application that interacts with the cloud-deployed system, allowing students to check borrowing history, book availability, and receive notifications.

## Reflections
This project served as a valuable learning experience, providing a practical application of embedded systems concepts. The integration of hardware and software components presented unique challenges, requiring careful consideration of data transfer, signal processing, and error handling. Working with the SQLite database and implementing CRUD operations reinforced the importance of efficient data management within a software system. The project also fostered critical thinking and problem-solving skills as I encountered and overcame various technical hurdles, such as optimizing RFID data processing and ensuring system stability. This hands-on experience has strengthened my understanding of embedded systems development and motivated me to further explore its applications in real-world scenarios. 
