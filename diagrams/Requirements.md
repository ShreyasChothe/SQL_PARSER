Requirements.md -



1. Hardware Requirements
●	Processor: Intel / AMD (Dual Core or higher)

●	RAM: Minimum 4 GB

●	Storage: Minimum 500 MB free disk space

●	Input Device: Keyboard

●	Output Device: Monitor

 
2. Software Requirements
2.1 Operating System
●	Windows / Linux / macOS

2.2 Programming Language
●	Python 3.x (for CLI and parser implementation)

2.4 Development Tools
●	Command Line Interface (Terminal / Command Prompt)

●	Text Editor or IDE (VS Code, PyCharm)
3. Functional Requirements
The system shall:
1.	Accept user commands via CLI

2.	Core Engine Implementation
        The core validation engine shall:
	Parse SQL queries using grammar rules
	Validate syntax.
	Generate error objects with detailed messages
	If no errors it must generate Tokens.

3.	The engine shall be designed for extensibility, allowing new SQL dialects to be added without major redesign.

4.	Convert valid commands into ANSI SQL queries
The system shall support both DML (SELECT, INSERT, UPDATE, DELETE) and DDL (CREATE, DROP, ALTER) statements as well as supports subqueries.
The system shall accept SQL queries in the form of strings entered by the use toor.

5.	  Validation Scope
The system shall validate queries against ANSI SQL standards.
	The system shall include a parser to read and analyze query grammar.
	The system shall verify and validate the query grammar
6. Output Formats
 -The system shall support saving query validation results to files as the following:                                
		TXT – plain text report
		JSON – structured output suitable for programmatic use
		CSV – tabular output for spreadsheet applications
-If errors are present, the system shall output them in the same selected format.

7.	 Batch Processing Support
The engine shall support batch processing, allowing multiple SQL queries to be read from a file and processed sequentially.
Batch processing shall not affect the performance of individual query validation.


8.	Perform CRUD operations:

○	Create records

○	Read records

○	Update records

○	Delete records

9.	Display query results in a human readable format

10.	Handle invalid commands gracefully

11.	Allow safe exit from the system

 
4. Non-Functional Requirements
1. Supported Versions
●	The system shall support the following software versions:

○	Operating System: Windows 10 and above, Linux (Ubuntu 20.04+).

○	Python —-

2. Character Restriction
●	The system shall accept SQL queries with a maximum character limit per query to ensure efficient parsing and validation.

●	Long queries exceeding the character limit shall be prompted with an appropriate warning.

3. Memory Utilization
●	The system shall optimize memory usage by processing queries one at a time in memory, particularly during batch processing.

●	Large files shall be handled efficiently without loading the entire file into memory at once.
4. Supported Platforms
●	The system shall be platform-independent across supported operating systems.

●	The CLI shall function identically on Windows, Linux, and macOS without requiring platform-specific changes.

5. Dependencies
●	The system depends on the following:

○	Regex library/module – for pattern-based syntax validation

○	Parser module – for grammar and structure validation

○	Standard I/O and file handling libraries for reading/writing queries and results

●	All dependencies shall be cross-platform compatible and lightweight to avoid heavy system load.



 
6. Database Requirements
1.	Relational schema designed using:

○	Primary keys

○	Foreign keys (if applicable)

○	Constraints (NOT NULL, CHECK, UNIQUE)

2.	Normalized tables (up to 3NF)

3.	Sample dataset for testing

4.	Support for ANSI SQL operations

7. Security Requirements

1.	Prevent SQL injection using parameterized queries

2.	Restrict direct SQL access from user input

3.	Validate all user inputs before execution

 
8. Constraints and Assumptions
●	The system is CLI-based only

●	Designed for educational and academic use

●	Internet connection not required