import subprocess
import json


def run_nmap_scan(target_ip, output_file):
    nmap_command = f"nmap -F -A -vv -sV  {target_ip} --script ssl-enum-ciphers -oN {output_file}.txt"
    subprocess.run(nmap_command, shell=True)


def process_nmap_output(output_file):
    results = []

    with open(output_file, 'r') as file:
        output = file.read()

    start_index = output.find("| ssl-enum-ciphers:")
    end_index = output.find("|_  least strength:")

    cipher_section = output[start_index:end_index]

    lines = cipher_section.strip().split("\n")

    for line in lines:

        if line.strip() == "" or line.startswith("|_"):
            continue

        parts = line.strip().split()

        if len(parts) >= 3 and "cipher" not in line:
            cipher = parts[1]
            strength = parts[-1]
            results.append({"cipher": cipher, "strength": strength})

    return results

# Main script


# target_ip = input("Enter target IP: ")
# output_file = input("Enter output file name: ")
# run_nmap_scan(target_ip, output_file)
output_file = "test1.txt"
results = process_nmap_output(output_file)
json_output = json.dumps(results, indent=4)
print(json_output)
