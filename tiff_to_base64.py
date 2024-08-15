import base64


def tiff_to_base64(file_path):
    with open(file_path, "rb") as tiff_file:
        encoded_string = base64.b64encode(tiff_file.read()).decode("utf-8")
    return encoded_string


# Replace 'path/to/your/file.tiff' with the actual path to your TIFF file
tiff_path = "tests/test_data/freeperson_text_vol1_Page_032.tiff"
base64_string = tiff_to_base64(tiff_path)

print(f"Base64 encoded string (first 100 characters):\n{base64_string[:100]}...")

# Save the full base64 string to a file
with open("tiff_base64.txt", "w") as f:
    f.write(base64_string)

print(f"\nFull base64 string saved to 'tiff_base64.txt'")
