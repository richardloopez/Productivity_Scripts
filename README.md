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

*To make this script work in all the environment, is highly recommemded to follow next steps:
    1. Go to home (∼) and open the .bashrc 
    2. add an alias with the absolute path. i.e: alias rmex="python3 /home/richard/scripts_interesantes/rmex/rmex.py"
    3. Now you can use the script by typing "rmex -rd -rf ..."
    4. Enjoy :)


\
\




**mail: Slurm Job Monitor AND Email Notifier** 

This script allows you to monitor SLURM jobs and send email notifications when a job finishes or if the job ID is not found in the queue. It is ideal for clusters using SLURM job scheduling and helps you stay informed automatically about your job status.

Features
Automatic monitoring: Runs as a background daemon process that watches the status of a SLURM job.

Email notifications: Sends an email when the job finishes or if the job ID does not exist.

Lock files: Prevents multiple monitors from running for the same job using lock files.

Flexible configuration: All email and behavior settings are managed via a JSON config file in your home directory.

Easy integration: Add the script to your PATH or create an alias to run it as a simple command.

Installation and Setup
1. Clone this repository
bash
git clone https://github.com/yourusername/slurm-job-email-notifier.git
cd slurm-job-email-notifier
2. Create the configuration file
Create a .mail_config.json file in your home directory with the following structure (adjust values to your SMTP server and emails):

{
    "smtp_server": "smtp.yourserver.com",
    "smtp_port": 587,
    "from_email": "youremail@domain.com",
    "smtp_password": "your_password",
    "default_emails": ["recipient1@domain.com", "recipient2@domain.com"],
    "lock_dir": "/tmp/mail_job_locks"
}
smtp_server, smtp_port, from_email, smtp_password: Your SMTP server details.

default_emails: List of default email recipients for notifications.

lock_dir: Directory for lock files (default is /tmp/mail_job_locks).

3. Make the script executable
chmod +x mail.py
4. (Optional) Add the directory to your PATH
To run the script from anywhere, add its folder to your PATH in your .bashrc or .zshrc:

export PATH="$PATH:/home/richard/nicest_scripts/mail"
(Change the path to your actual script location)

5. (Optional) Create an alias for convenience
Create an alias to run the script simply as mail:

bash
alias mail="python3 /home/richard/nicest_scripts/mail/mail.py"
Add this line to your .bashrc or .zshrc to make it permanent.

Usage
Run the script with the job_id, job title, and a custom message.
Optionally, specify a comma-separated list of emails to notify additional recipients:

bash
mail <job_id> "<job_title>" "<nice_phrase>" [email1,email2,...]

Example:

mail 12345 "Protein Simulation" "Your simulation has finished!"

If the job exists, you will receive an email when it finishes.

If the job does not exist, you will receive an email alert indicating the job status could not be checked.

Notes
The script requires a Linux environment with the squeue command available (SLURM).

It runs as a daemon, so no need to use nohup or &.

For SMTP configuration help, consult your system administrator or email provider.

If you want me to help with anything else, just ask!




