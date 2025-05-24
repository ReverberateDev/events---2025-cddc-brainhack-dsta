def extended_gcd(a, b):
    """
    Returns (gcd, x, y) such that a*x + b*y = gcd
    """
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def modInverse(a, m):
    """
    Returns modular multiplicative inverse of a under modulus m.
    Assumes a and m are coprime.
    """
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        raise Exception('Modular inverse does not exist')
    return (x % m + m) % m

# SECP256k1 curve order n
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# Given values from the problem
r_val  = 81210355722750344493541519494641458710145722871994877785183554697310523407018
h1_val = 45643200378651069483892104393394606812504455659831083323743202489147422538955
h2_val = 74831345439009646272332597737070016777412939113737083148228963710487431876647
s1_val = 110764343964105699917226529930289538481215574456544978805357332521308340464732
s2_val = 90138993253633063487274662700800979929978777245182171200537527514756442604713

# Calculate k = (h1 - h2) * (s1 - s2)^-1 mod n
h1_minus_h2 = (h1_val - h2_val + n) % n  # Ensure positive result before modulo
s1_minus_s2 = (s1_val - s2_val + n) % n  # Ensure positive result before modulo

if s1_minus_s2 == 0:
    print("Error: s1 and s2 are the same, cannot recover k this way (or h1=h2).")
    exit()

inv_s1_minus_s2 = modInverse(s1_minus_s2, n)
k = (h1_minus_h2 * inv_s1_minus_s2) % n
print(f"Recovered nonce k: {k}")

# Calculate d = (s1*k - h1) * r^-1 mod n
# Or d = (s2*k - h2) * r^-1 mod n  (should give the same result)

inv_r = modInverse(r_val, n)

# Using first signature
term1_s1k = (s1_val * k) % n
val_to_invert_s1 = (term1_s1k - h1_val + n) % n # (s1*k - h1) mod n
private_key_d1 = (val_to_invert_s1 * inv_r) % n
print(f"Calculated private key d (using s1): {private_key_d1}")
print(f"Private key d in hex (using s1): {hex(private_key_d1)}")

# Sanity check using second signature
term1_s2k = (s2_val * k) % n
val_to_invert_s2 = (term1_s2k - h2_val + n) % n # (s2*k - h2) mod n
private_key_d2 = (val_to_invert_s2 * inv_r) % n
print(f"Calculated private key d (using s2): {private_key_d2}")
print(f"Private key d in hex (using s2): {hex(private_key_d2)}")

if private_key_d1 == private_key_d2:
    print("\nBoth calculations for d match.")
    print(f"The recovered private key is: {private_key_d1}")
    print(f"In hexadecimal: {hex(private_key_d1)}")
    # The flag is probably this hex value (possibly without the 0x)
else:
    print("\nError: Calculations for d do not match. Check math or input values.")

# Compare with your friend's key which you confirmed was the solution to the previous (mnemonic) problem
# This might not be relevant if this ECDSA attack is a separate way to get the same key.
# friends_key_hex_str = "9f9068a0cc25f39b9c5fba5bb88d75bc5e4503a8406101a3195dc395194ea690"
# friends_key_int = int(friends_key_hex_str, 16)
# if private_key_d1 == friends_key_int:
#     print(f"SUCCESS! This recovered key {hex(private_key_d1)} matches the key from the mnemonic problem!")
# else:
#     print(f"This recovered key {hex(private_key_d1)} does NOT match the key from the mnemonic problem ({hex(friends_key_int)}).")