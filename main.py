import subprocess


def run_nmap_scan(target_ip, output_file):
    nmap_command = f"nmap -F -A -vv -sV --script ssl-enum-ciphers -oN {output_file}.txt {target_ip}"
    subprocess.run(nmap_command, shell=True)

# Main script


target_ip = input("Enter target IP: ")
output_file = input("Enter output file name: ")


run_nmap_scan(target_ip, output_file)
