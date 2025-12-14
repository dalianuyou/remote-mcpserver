import os

s = os.environ.get("DLAI_LOCAL_URL")
if s:
    print(s.format(port=6277)[:-1])
else:
    print("DLAI_LOCAL_URL not set")
