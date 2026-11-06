FILE INTEGRITY MONITORING SYSTEM

1. Project Overview

The File Integrity Monitoring System is a cybersecurity project developed using Python. It monitors files and detects unauthorized changes.

2. Objective

To maintain file integrity by identifying modified, deleted, and newly created files.

3. Technologies Used

Python

SHA-256 Hashing Algorithm

JSON

File Handling

Operating System Module

4. Key Features

Create baseline of files.

Generate SHA-256 hashes.

Detect modified files.

Detect deleted files.

Detect newly created files.

Maintain activity logs.

5. Working

The system first creates a baseline by calculating SHA-256 hashes of files in a selected folder.

During an integrity check, it calculates the hashes again and compares them with the saved baseline.

If a file is modified, deleted, or newly created, the system displays a warning.

6. Testing Results

Modified file detection: Successful

New file detection: Successful

Deleted file detection: Successful

7. Conclusion

The project demonstrates how file integrity monitoring can help identify unexpected changes and support basic cybersecurity protection.

8. Future Scope

Email notifications

Graphical user interface

Automatic scheduled monitoring

Improved reporting features