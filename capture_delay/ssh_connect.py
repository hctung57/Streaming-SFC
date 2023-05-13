def run():
    import paramiko
    ssh = paramiko.SSHClient()
    # Auto add host to known hosts
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Connect to server
    ssh.connect("192.168.101.9", username="fil", password="1")
    service_name_1 = 'tung'
    service_name_2 = 'tung1'
    service_ip_1 = 1
    service_ip_2 = 2

    command = f'cd /home/fil/tung/delay/ && python3 capture.py -name1 {service_name_1} -name2 {service_name_2} -s1 {service_ip_1}:1936 -s2 {service_ip_2}:1936'
    # Do command
    (ssh_stdin, ssh_stdout, ssh_stderr) = ssh.exec_command("cd /home/fil/tung/delay/ && python3 capture.py -name1 tung -name2 tung1 -s1 10.233.41.198:1936 -s2 10.233.49.57:1936")
    # Get status code of command
    exit_status = ssh_stdout.channel.recv_exit_status()
    # Print status code
    print ("exit status: %s" % exit_status)
    # Print content
    for line in ssh_stdout.readlines():
        print(line.rstrip())
    # Close ssh connect
    ssh.close()