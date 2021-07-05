import os


def is_production():
    return os.getenv("PRODUCTION") == "1"

# 1. Fetch & Pull van github
# 2. Bot afsluiten
# de requirements.txt downloaden => "pip3 install -r requirements.txt"
# 3. niets dat is 't

# bash script:
# download requirements.txt
# start bot => moet hier stoppen tot dat de bot afsluit
# exit