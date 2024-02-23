import pyshark

def detect_email(pcap_file):
    # Open pcap file
    capture = pyshark.FileCapture(pcap_file)

    # List to store detected emails
    detected_emails = []

    # Iterate over each packet in the capture
    for packet in capture:
        try:
            # Check if packet contains email content
            if 'email' in packet:
                # Extract email content
                email_content = packet['email']
                # Append to the list of detected emails
                detected_emails.append(email_content)
        except Exception as e:
            # Handle any exceptions that occur during packet parsing
            print(f"Error processing packet: {e}")

    # Close the capture file
    capture.close()

    # Return the list of detected emails
    return detected_emails

# Replace 'example.pcap' with the path to your pcap file
detected_emails = detect_email('Project-NetProbeX/backend/email.pcapng')

# Print detected emails
for email in detected_emails:
    print(email)


