import subprocess
import json


def run_nmap_scan(target_ip, output_file):
    nmap_command = f"nmap -F -A -vv -sV  {target_ip} --script ssl-enum-ciphers -oN {output_file}"
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


def interpret_cipher_findings(cipher_results):
    findings = {
        "strong": [],
        "moderate": [],
        "weak": [],
        "unknown": []
    }

    for result in cipher_results:
        cipher = result['cipher']
        strength = result['strength']

        interpretation = interpret_cipher_strength(strength)
        findings[interpretation].append(cipher)

    return findings


def interpret_cipher_strength(strength):
    if strength == "A":
        return "strong"
    elif strength == "B":
        return "moderate"
    elif strength == "C":
        return "weak"
    else:
        return "unknown"

# Main script


target_ip = input("Enter target IP: ")
output_file = input("Enter output file name: ")+".txt"

run_nmap_scan(target_ip, output_file)
results = process_nmap_output(output_file)
cipher_findings = interpret_cipher_findings(results)
json_output = json.dumps(cipher_findings, indent=4)
print(json_output)
