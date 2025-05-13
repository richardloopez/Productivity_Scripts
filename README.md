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

    Here you have some examples:

    1. rmex("-rd alonso.txt") -> destroy all documents [except alonso.txt] (folders remain untouched)
    2. rmex("-rd -rf schumacher.txt") -> destroy all documents [except schumacher.txt] and all folders
    3. rmex("-rf hamilton.txt") -> destroy all folders (documents remain untouched). Yeah, it makes no sense adding "hamilton.txt" because no "rd" was added...

    4. rmex("-rf renault)-> destroy all folders [except renault] (documents remain untouched)
    5. rmex("-rd -rf ferrari") -> destroy all documents and all folders [except ferrari.txt]
    6. rmex("-rd mercedes") -> destroy all documents (folders remain untouched). Yeah, it makes no sense adding "mercedes" because no "rf" was added...

    7. rmex("-rd -rf alonso.txt renault") -> MAXIMUN POWER!! destroy all documents [except alonso.txt] and all folders [except renault]



This script is useful for quickly cleaning up directories while preserving important files or folders.



\
\




**mail: Slurm Job Monitor (not working now)** 
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




