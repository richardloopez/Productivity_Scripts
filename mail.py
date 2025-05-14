#!/usr/bin/env python3

# Author: Richard Lopez Corbalan
# GitHub: github.com/richardloopez
# Citation: If you use this code, please cite Lopez-Corbalan, R

import os
import json
import sys
import subprocess
import time
import smtplib
from email.mime.text import MIMEText
import signal


# Charge de essential data, placed on the .json file (home). Make sure all the needed info is inside of it.

def load_config():
    config_path = os.path.expanduser("~/.mail_config.json")
    try:
        with open (config_path, "r") as archive:
            config = json.load(archive)
            if "lock_dir" not in config:
                config["lock_dir"] = os.path.expanduser("~/tmp/mail_job_locks") # Default value
            return(config)
    except FileNotFoundError:
        print(f"Config file {config_path} not found. Please create.", file = sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Config file {config_path} is not valid JSON.", file = sys.stderr)
        sys.exit(1)

# Capture the arguments on the call.

def parse_args():
    if len(sys.argv) < 4:
        print("Usage: mail <job_id> \"<job_title>\" \"<nice_phrase>\" [optional_emails_comma_separated]", file = sys.stderr)
        sys.exit(1)
    
    job_id = sys.argv[1]
    job_title = sys.argv[2]
    nice_phrase = sys.argv[3]

    # Optional emails sepparated by comma, if exists
    if len(sys.argv) > 4:
        recipients = sys.argv[4].split(",")
    else:
            recipients = None
    return job_id, job_title, nice_phrase, recipients
        

def daemonize ():
    # First fork
    pid = os.fork()
    if pid > 0:
        sys.exit(0) # Finish the "father" process
    
    os.setsid() # Create a new session
    os.umask(0) # Files permissions by default

    # Second fork avoid the daemon to take the control of the terminal) 
    pid = os.fork()
    if pid > 0:
        sys.exit(0)

        # Redirect both outputs (error and standard) to /dev/null
        sys.stdout.flush()
        sys.stderr.flush()
        with open ("/dev/null", "wb", 0) as dev_null:
            os.dup2(dev_null.fileno(), sys.stdout.fileno())
            os.dup2(dev_null.fileno(), sys.stderr.fileno())


def acquire_lock(job_id, lock_dir):
    os.makedirs(lock_dir, exist_ok=True) 
    lockfile = os.path.join(lock_dir, str(job_id))
    if os.path.exists(lockfile):
        print(f"Error: A monitor for this job already exists {job_id}", file=sys.stderr)
        sys.exit(1)
    with open (lockfile, "w") as archive:
        archive.write(str(os.getpid())) # Saves the process PID

def release_lock(job_id, lock_dir):
    lockfile = os.path.join(lock_dir, str(job_id))
    if os.path.exists(lockfile):
        os.remove(lockfile)

def is_job_active(job_id):
    try: # Easy, executes "squeue". If the you does not appear, it is not active
        output = subprocess.check_output(
            ["squeue", "-j", str(job_id), "--noheader"],
            stderr = subprocess.DEVNULL
        )
        return bool(output.strip()) # True if output ; False if NO output
    except subprocess.CalledProcessError:
        return False # If an error took place, we assume the job is not active
 
def send_job_not_found_notification(config, job_id, job_title, recipients):
    body = (
        f"SLURM job NOT FOUND!\n\n"
        f"ID: {job_id}\n"
        f"Title: {job_title}\n"
        f"\nWork could not be consulted. "
        f"Possibly this work ID never existed or it finished before launching the monitor, "
        f"Maybe a consult error ocurred.\n"
        f"\nPlease, make sure the work ID was correct."
    )
    msg = MIMEText(body)
    msg["Subject"] = f"[SLURM][ERROR] Job {job_id} NOT FOUND"
    msg["From"] = config["from_email"]
    msg["To"] = ", ".join(recipients)

    with smtplib.SMTP(config["smtp_server"], config["smtp_port"]) as server:
        server.starttls()
        server.login(config["from_email"], config["smtp_password"])
        server.sendmail(config["from_email"], recipients, msg.as_string())
 
       

def monitor_job(job_id, check_interval=3): # 3 seconds between comprobations
    while True: 
        if not is_job_active(job_id):
            break # The process is finished, go out of the loop
        time.sleep(check_interval)

def send_notification(config, job_id, job_title, nice_phrase, recipients):
    body = (
        f"Your SLURM work has finished!\n\n"
        f"ID: {job_id}\n"
        f"Title: {job_title}\n"
        f"Enjoy: {nice_phrase}\n"
        f"\n¡Happy Computing! :)"
    )
    msg = MIMEText(body)
    msg["Subject"] = f"[SLURM] Job {job_id} - {job_title}"
    msg["From"] = config["from_email"]
    msg["To"] = ", ".join(recipients)

    # Send the message using SMTP
    with smtplib.SMTP(config["smtp_server"], config["smtp_port"]) as server:
        server.starttls()  # TLS encryption active
        server.login(config["from_email"], config["smtp_password"])
        server.sendmail(config["from_email"], recipients, msg.as_string())





def main():
    config = load_config()
    lock_dir = config["lock_dir"]
    job_id, job_title, nice_phrase, recipients = parse_args()
    if recipients is None:
        recipients = config["default_emails"]

    daemonize()
    acquire_lock(job_id, lock_dir)

    def handle_exit(signum, frame):
        release_lock(job_id, lock_dir)
        sys.exit(0)

    signal.signal(signal.SIGTERM, handle_exit)
    signal.signal(signal.SIGINT, handle_exit)

    try:
        activo = is_job_active(job_id)
        if not activo:
            send_job_not_found_notification(config, job_id, job_title, recipients)
        else:
            monitor_job(job_id)
            send_notification(config, job_id, job_title, nice_phrase, recipients)
    except Exception as e:
        print(f"Error sending email: {e}", file=sys.stderr)
    finally:
        release_lock(job_id, lock_dir)


if __name__ == "__main__":
    main()