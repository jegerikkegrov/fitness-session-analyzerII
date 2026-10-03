# Smart Fitness Session Analyzer

Python programming Assignment II - Option A

## Description

The program reads the participants profiles and fitness session data from CSV files.
The program validates the records, rejects invalid data, analyzes usable fitness sessions
and creates report files.

## Project structure

main.py - entry point of the application, it handles command-line arguments, loads input files,
runs the analysis and starts report generation.

models.py - contains the main classes such as ReferenceProfile, Participant, Observation and FitnessSession.
these clases represent the fitness data used by the program.

csv_reader.py - Reads the participant and fitness session CSV files, converts CSV values to suitable python types,
connects sessions to participant and records rejected rows. 

validation.py - contains validation functions for participant IDs, session IDs numerical ranges, timestamps and signal quality.

exceptions.py - Defines the custom exceptions "InvalidIdentifierError" and "InvalidRecordError", these are used when invalid identifiers or records are detected.

analysis.py - Analyzes usable observations, compares session data with the participants personal reference profile and produces
a structured classification result.

reports.py - creates the output directory and writes the analysis summary,
readable analysis report and rejected-record report.

test_analyzer.py - contains automated tests for valid and invalid identifiers, boundary values and invalid records and missing files.

data/ - Contains the official input files: Participant profiles, valid fitness sessions, and intentionally invalid fitness session data.

output/ - created by the program at runtime and contains analysis_summary.csv, analysis_report.txt and rejected_records.txt
 
## Validation
Participant IDs must follow the format P followed by the three digits ex. "P001".
Fitness session IDs must follow the format "FIT-YYYY-NNN".
Numerical values are checked using numerical ranged comparison rather than regular expressions. 

Signal quality values must be between 0 and 1. for this project, a signal quality below "0.5"
is treated as poor-quality data and the observation is rejected.

This 0.5 threshold is a documented project rule because the supplied data dictionary defines the valid 0-1 range
but does not specify a poor-signal threshold. 

## analysis
Sessions with fewer than four usable observations are classified as "insufficient usable data"-
Usable sessions are compared with the participants personal baseline heart rate and classified
as resting, moderate or high activity.
The program also checks whether heart rate and activity level decrease from the first observation
to the last observation as an indication of recovery.

## Object-Oriented Design
The program uses composition:
A "participant" contains a "ReferenceProfile". 
A "FitnessSession" contains a "Participant" and multiple "Observations" objects.

## Running the program
As mentioned above, the main.py is used to run the code. So from the repository root,
python main.py

Optional command-line arguments 

    python main.py --profiles data/participants.csv --sessions data/fitness_sessions.csv --invalid-sessions data/fitness_sessions_invalid_csv --output output

## Output files
the program creates 3 output files which are:
`output/analysis_summary.csv`, `output/analysis_report.txt`, `output/rejected_records.txt`

## Tests

Run the automated tests from the repository root:
    python -m unittest discover -s tests