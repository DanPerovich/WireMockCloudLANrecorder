import requests

print("")

# Ask user for WireMock Cloud API key
api_key = input("Enter your WireMock Cloud API key: ")
headers = {"Authorization": "Token " + api_key}

# Ask user for WireMock Cloud API name
api_name = input("Enter your WireMock Cloud API name: ")

# Check if MockAPI exists
mockapi_url = f"https://{api_name}.wiremockapi.cloud/__admin/requests"

try:
    mockapi_response = requests.get(mockapi_url, headers=headers)
except requests.exceptions.RequestException as e:
    print("There was a connection error to WMC. Please make sure the WireMock Cloud Mock API already exists in your account.")
    raise SystemExit(e)

if mockapi_response.status_code == 200:
    print("MockAPI already exists in WireMock Cloud.")
else:
    # <TODO> if not 200 check if WMC unreachable OR MockAPI does not exist
    print("Failed to reach WireMock Cloud. Response code was " + str(mockapi_response.status_code) + ". Exiting.")
    exit()

# Ask user if they want to keep or clear existing mappings
clear_mappings = input("Do you want to erase all existing stubs in this APIs ( y or [n] )? ") or 'n'
if clear_mappings.lower() == 'y':
    confirm_clear = input("*** Are you sure ( y or [n] )? *** ") or 'n'
    if confirm_clear.lower() == 'y':
        delete_url = f"https://{api_name}.wiremockapi.cloud/__admin/mappings"
        delete_response = requests.delete(delete_url, headers=headers)
        if delete_response.status_code == 200:
            print("All existing stubs have been deleted from the WireMock Cloud mock API.")
        else:
            print("Failed to delete existing stubs in WireMock Cloud. Exiting.")
            exit()
    else:
        print("Existing stubs will NOT be removed.")
else:
    print("Existing stubs will NOT be removed.")

# Ask user for the target URL prefix to record
target_url_prefix = input("Enter the target URL prefix to record (ex: https://api.github.com): ")

# Reset all mappings in local recorder
reset_mappings_url = f"http://localhost:8080/__admin/mappings"
reset_response = requests.delete(reset_mappings_url)

if reset_response.status_code == 200:
    print("Local recorder mappings have been reset.")
else:
    print("Failed to reset local recorders mappings. Exiting.")
    exit()

# Call the WireMock API to start the recorder
start_recorder_url = f"http://localhost:8080/__admin/recordings/start"
start_response = requests.post(start_recorder_url, headers=headers, json={"targetBaseUrl": target_url_prefix, "persist": False})

if start_response.status_code == 200:
    print("Recorder started successfully.")
else:
    print("Failed to start the recorder. Exiting.")
    exit()

# Wait for the user to type STOP
input("Recorder started. Press Enter to stop recording...")

# Call the WireMock API to stop the recorder
stop_recorder_url = f"http://localhost:8080/__admin/recordings/stop"
stop_response = requests.post(stop_recorder_url, headers=headers)

if stop_response.status_code == 200:
    print("Recorder stopped successfully.")
else:
    print("Failed to stop the recorder. Exiting.")
    exit()

# Export recorded stubs to a file named recorded-stubs.json
export_stubs_url = f"http://localhost:8080/__admin/mappings"
export_response = requests.get(export_stubs_url, headers=headers)

if export_response.status_code == 200:
    # with open("recorded-stubs.json", "w") as outfile:
    #     json.dump(export_response.json(), outfile)
    print("Recorded stubs exported successfully.")
else:
    print("Failed to export recorded stubs. Response code was " + str(export_response.status_code) + ". Exiting.")
    exit()

# Import mock api into WMC
import_url = f"https://{api_name}.wiremockapi.cloud/__admin/mappings/import"
import_response = requests.post(import_url, headers=headers, json=export_response.json())

if import_response.status_code == 200:
    print("Recorded stubs imported to WireMock Cloud successfully.")
    print("Exiting...")
    print("")
else:
    print("Failed to import recorded stubs. Response code was " + str(import_response.status_code) + ". Exiting.")
    exit()