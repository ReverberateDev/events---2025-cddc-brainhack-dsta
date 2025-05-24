import base64
encoded_string = "MEi4xJpC4pI+FiJuAn4i2o7hpfHVCavRpfkzp18rX99jwWdodAA0wHQAYtKO9noGdBJ2sg=="
decoded_bytes = base64.b64decode(encoded_string)
print(decoded_bytes)
# To see it as hex, which can be useful for non-printable characters:
# print(decoded_bytes.hex())