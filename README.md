# Productivity_Scripts

A collection of Python scripts for managing files and documents, enhancing productivity and workflow efficiency.





**rmex: Remove Except**

Purpose:
rmex is a Python script designed to simplify file and directory management by allowing users to delete all files or directories in a given path, except for specified exceptions.

Functionality:

Flags:

-rf: Delete folders except those specified.

-rd: Delete files except those specified.

Usage:

Specify files or directories to keep as arguments after flags.

The script will prompt for confirmation before deleting any items.

Safety Features:

Preview of changes before deletion.

Manual confirmation required.

Supports self-deletion if not excluded.

Example Usage:
rmex -rf -rd folder1 file1.txt
This script is useful for quickly cleaning up directories while preserving important files or folders.



\
\
/
/




**mail: Slurm Job Monitor**
Purpose:
A Python script to monitor Slurm jobs and send email notifications upon completion.

Functionality:

Job Monitoring: Continuously checks the status of a specified Slurm job.

Email Notifications: Sends an email when the job completes, including job details.

Background Execution: Runs in the background, allowing uninterrupted terminal use.

Usage:

mail <job_id> "<job_title>" "<nice_phrase>" "<email1>,<email2>,..."

Configuration:

Email sender credentials are expected to be set as environment variables (SLURM_NOTIFY_EMAIL and SLURM_NOTIFY_PASSWORD) in your .bashrc file for secure configuration.

Features:

Configurable email sender and recipients.

Automatic background execution.

Supports multiple recipient emails.




