import gdown

# ID file dari Google Drive
file_id = "1GcGw86QIsxa8UFPHXsqIMaUdVsgu5YAz"

# URL unduhan langsung
url = f"https://drive.google.com/file/d/1GcGw86QIsxa8UFPHXsqIMaUdVsgu5YAz/view?usp=drive_link"

# Nama file output
output = "fer2013.csv"

# Unduh file
gdown.download(url, output, quiet=False)
