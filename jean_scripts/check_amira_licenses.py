#!/usr/bin/env python

# retrieve the output from the command 'license-status-amira'
import subprocess

def get_license_status():
    try:
        output = subprocess.check_output(['license-status-amira'], stderr=subprocess.STDOUT)
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving license status: {e.output.decode('utf-8')}")
        return None
    
def format_status(status):
    # this function only keep the information of interest
    lines = status.splitlines()
    formatted_dict = {}
 
    for line in lines:

        if "RESERVATIONs for HOST_GROUP MARS" in line:
            formatted_dict['HOST_GROUP_MARS'] = line
        elif "RESERVATIONs for HOST_GROUP VENUS" in line:
            formatted_dict['HOST_GROUP_VENUS'] = line
 
    record_line = False
    first_blank_line = True
    for line in lines:

        if record_line:
            if ", start " in line:
                formatted_dict['AvizoSubMains'].append(line)
            elif (line.strip() == "") and (first_blank_line):
                first_blank_line = False
            elif "floating license" in line:
                continue
            elif "RESERVATION" in line:
                continue
            else:
                break
                
            continue
      
        if line.strip().startswith('"AvizoSubMains"'):
            record_line = True
            formatted_dict['AvizoSubMains'] = []

    return formatted_dict

def main():
    status = get_license_status()

    if status:
        formatted_dict = format_status(status)
        print(f"STATUS OF AMIRA LICENSES:\n")
        print(f"HOST_GROUP_MARS: {formatted_dict.get('HOST_GROUP_MARS', 'Not found')}")
        print(f"HOST_GROUP_VENUS: {formatted_dict.get('HOST_GROUP_VENUS', 'Not found')}")
        print("")
        print(f"WHO IS USING THE LICENSES (and WHERE)?\n")
        for line in formatted_dict.get('AvizoSubMains', []):
            print(line.strip())
        print("\n")

    else:
        print("Failed to retrieve license status.")
        print("Exiting...")
        exit(1)


if __name__ == "__main__":
    main()