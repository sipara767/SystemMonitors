import psutil
import logging
import smtplib
import configparser
import sys


# Function to fetch CPU usage
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)


# Function to fetch memory utilization
def get_memory_utilization():
    return psutil.virtual_memory().percent


# Function to log monitoring events
def log_event(message):
    current_cpu_usage = get_cpu_usage()
    current_memory_usage = get_memory_utilization()
    message = f"{message}(cpu: {current_cpu_usage}%, Memory:{current_memory_usage}%)"
    logging.info(message)


# Function to send email notification
def send_email_notification(subject, body):
    config = configparser.ConfigParser()
    config.read('config.ini')

    sender = config['Email']['sender']
    recipient = config['Email']['recipient']
    smtp_server = config['SMTP']['server']
    smtp_port = int(config['SMTP']['port'])
    smtp_username = config['SMTP']['username']
    smtp_password = config['SMTP']['password']

    message = f'Subject: {subject}\n\n{body}'

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as smtp:
            smtp.starttls()
            smtp.login(smtp_username, smtp_password)
            smtp.sendmail(sender, recipient, message)
        print('Email notification sent!')
    except Exception as e:
        print(f'Failed to send email notification: {e}')


# Main function
def main():
    # Load configuration
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Load threshold values from config file
    cpu_threshold = float(config['Thresholds']['cpu'])
    memory_threshold = float(config['Thresholds']['memory'])

    # Fetch system data
    cpu_usage = get_cpu_usage()
    memory_utilization = get_memory_utilization()

    print(f"current cpu usage:{cpu_usage}")
    print(f"current memory utilization:{memory_utilization}")
    # Check thresholds and trigger alarms
    if cpu_usage > cpu_threshold:
        print('Warning: CPU usage is above the threshold!')
        log_event('CPU usage exceeded threshold')
        send_email_notification('Warning: CPU usage exceeded threshold', 'Check the system for high CPU usage.')

    if memory_utilization > memory_threshold:
        print('Warning: Memory utilization is above the threshold!')
        log_event('Memory utilization exceeded threshold')
        send_email_notification('Warning: Memory utilization exceeded threshold',
                                'Check the system for high memory utilization.')


if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(filename='monitor.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Parse command-line arguments
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
        configparser.ConfigParser().read(config_file)

    # Run the main function
    main()
