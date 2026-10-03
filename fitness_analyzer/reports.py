from pathlib import Path
import csv

def create_output_directory(output_path):
    output_directory = Path(output_path)
    output_directory.mkdir(parents=True, exist_ok=True)

    return output_directory

def write_analysis_summary(results, output_directory):
    file_path = output_directory / "analysis_summary.csv"

    with open(file_path, "w", encoding="utf-8", newline="") as file:
        fieldnames = [
            "session_id",
            "participant_id",
            "classification",
            "reason"
        ]
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for result in results:
            writer.writerow({
                "session_id": result["session_id"],
                "participant_id": result["participant_id"],
                "classification": result["classification"],
                "reason": result["reason"]
            })

def write_analysis_report(results, output_directory):
    file_path = output_directory / "analysis_report.txt"

    with open(file_path, "w", encoding="utf-8") as file:
        for result in results:
            file.write(
                f"Session: {result["session_id"]}\n"
                f"Participant: {result["participant_id"]}\n"
                f"Classification: {result["classification"]}\n"
                f"Reason: {result["reason"]}\n"
                "\n"
            )

def write_rejected_records(rejected_records, output_directory):
    file_path = output_directory / "rejected_records.txt"

    with open(file_path, "w", encoding="utf-8") as file:
        for record in rejected_records:
            file.write(
                f"Source: {record['source']}\n"
                f"Row: {record['row']}\n"
                f"Field: {record['field']}"
                f"Reason: {record['reason']}"
                "\n"

            )