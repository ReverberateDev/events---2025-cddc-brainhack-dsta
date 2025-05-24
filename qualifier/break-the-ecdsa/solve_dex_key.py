import itertools
from mnemonic import Mnemonic
from bip32 import BIP32 
import sys 
import os 

def deleetspeak(word):
    word = word.lower() 
    word = word.replace("1", "i").replace("!", "i")
    word = word.replace("3", "e")
    word = word.replace("4", "a")
    word = word.replace("5", "s")
    word = word.replace("7", "t")
    word = word.replace("0", "o")
    if word == "skybiue": return "sky"
    if word == "iionkin": return "lion" 
    if word == "padocoin": return ["pad", "coin"] 
    return word

def solve():
    bip39_official_list_path = "bip39_english.txt"
    bip39_official_list = set()
    if not os.path.exists(bip39_official_list_path):
        print(f"Error: {bip39_official_list_path} not found. Please download it from")
        print("https://github.com/bitcoin/bips/blob/master/bip-0039/english.txt")
        print("and place it in the same directory as this script.")
        return
    
    try:
        with open(bip39_official_list_path, "r") as f:
            for line in f:
                bip39_official_list.add(line.strip().lower())
    except Exception as e:
        print(f"Error reading {bip39_official_list_path}: {e}")
        return

    dex_dict_raw = [
        "v1ew", "5tr0ng", "app1e", "fr13nd", "7hank5", "sch00l", "c0d3", "kn0w1edg3",
        "g00d", "b4d", "dr34m", "r1v3r", "mou7a1n", "f0r3st", "5kyb1u3", "p14n3t",
        "c4r", "b1k3", "b00k", "5tor3", "l4ugh", "sm1l3", "v1ct0ry", "p0w3r",
        "3n3rgy", "7r4v3l", "p3ac3", "f1gh7", "h0p3", "4n7", "1i0nkin9", "7ig3r",
        "p4d0c0in", "0c34n", "w4v3", "5h0r3", "c4v3", "m00n", "5un", "5tar",
        "7r33", "fl0w3r", "5e3d", "gr455", "b3", "4ir", "c10ud", "r41n",
        "5n0w", "5t0rm"
    ]

    valid_dex_bip39_words = set()
    for raw_word in dex_dict_raw:
        deleet_candidates = deleetspeak(raw_word)
        if isinstance(deleet_candidates, list):
            for candidate in deleet_candidates:
                if candidate in bip39_official_list:
                    valid_dex_bip39_words.add(candidate)
        else: 
            if deleet_candidates in bip39_official_list:
                valid_dex_bip39_words.add(deleet_candidates)
    
    valid_dex_bip39_words = sorted(list(valid_dex_bip39_words))

    if not valid_dex_bip39_words:
        print("No valid BIP-39 words found from Dex's dictionary.")
        return

    print(f"Valid BIP-39 candidate words from Dex's dictionary ({len(valid_dex_bip39_words)}):")
    print(valid_dex_bip39_words)
    sys.stdout.flush()

    # Mapped words for the fixed slots
    mapped_5eed = "seed"
    mapped_r4nd0m = "random"
    mapped_g00d = "good"
    mapped_5olve = "solve"
    mapped_c0ffe = "coffee"
    mapped_pe4nut = "peanut"
    mapped_5mart = "smart"

    # Candidates for P1 (from "BIP-39") and P2 (from "SECP256k1")
    # Added a few more plausible mappings
    p1_candidates = ["trip", "tip", "rib", "tiny", "hip", "pipe", "pink", "lip", "skip"] 
    p2_candidates = ["secret", "curve", "key", "seek", "scan", "safe", "second", "keep"]

    # Filter to ensure p1/p2 candidates are valid BIP-39 words
    p1_candidates = sorted(list(set(w for w in p1_candidates if w in bip39_official_list)))
    p2_candidates = sorted(list(set(w for w in p2_candidates if w in bip39_official_list)))

    if not p1_candidates or not p2_candidates:
        print("Error: No valid BIP-39 mappings found for P1 or P2. Check candidate lists.")
        return

    print(f"P1 candidates (for BIP-39): {p1_candidates}")
    print(f"P2 candidates (for SECP256k1): {p2_candidates}")
    sys.stdout.flush()

    mnemo = Mnemonic("english")
    target_priv_key_hex = "9f9068a0cc25f39b9c5fba5bb88d75bc5e4503a8406101a3195dc395194ea690"
    
    total_combinations = len(p1_candidates) * len(p2_candidates) * (len(valid_dex_bip39_words) ** 3)
    
    print(f"Target Private Key: {target_priv_key_hex}")
    print(f"Total combinations to check: {total_combinations}")
    if total_combinations == 0:
        print("No combinations to check based on candidate lists. Exiting.")
        return
    sys.stdout.flush()

    checked_count = 0
    
    for p1_actual in p1_candidates:
        for p2_actual in p2_candidates:
            for d1_word1_val in valid_dex_bip39_words: # Corresponds to {word1}
                for d2_word2_val in valid_dex_bip39_words: # Corresponds to {word2}
                    for d3_word3_val in valid_dex_bip39_words: # Corresponds to {word3}
                        checked_count += 1
                        if checked_count % 10000 == 0:  # Adjusted reporting frequency
                            print(f"Progress: {checked_count}/{total_combinations} combinations checked...")
                            sys.stdout.flush()

                        current_mnemonic_list = [
                            p1_actual, p2_actual, d1_word1_val, mapped_5eed, mapped_r4nd0m,
                            d2_word2_val, mapped_g00d, mapped_5olve, mapped_c0ffe, d3_word3_val,
                            mapped_pe4nut, mapped_5mart
                        ]
                        current_mnemonic_str = " ".join(current_mnemonic_list)
                        
                        if mnemo.check(current_mnemonic_str):
                            seed = mnemo.to_seed(current_mnemonic_str, passphrase="")
                            bip32_master_key = BIP32.from_seed(seed)
                            
                            master_priv_key_bytes = None
                            if hasattr(bip32_master_key, 'privkey') and bip32_master_key.privkey is not None:
                                master_priv_key_bytes = bip32_master_key.privkey
                            elif hasattr(bip32_master_key, 'secret'): 
                                master_priv_key_bytes = bip32_master_key.secret
                            else:
                                print(f"Warning: Could not extract private key for: {current_mnemonic_str}")
                                continue

                            master_priv_key_hex = ""
                            if isinstance(master_priv_key_bytes, str): # Should be bytes
                                master_priv_key_hex = master_priv_key_bytes.lstrip('0x')
                            elif isinstance(master_priv_key_bytes, bytes):
                                master_priv_key_hex = master_priv_key_bytes.hex()
                            
                            if master_priv_key_hex == target_priv_key_hex:
                                print(f"\n!!! MATCH FOUND !!!")
                                print(f"Mnemonic: {current_mnemonic_str}")
                                print(f"P1 (mapped from 'BIP-39'): {p1_actual}")
                                print(f"P2 (mapped from 'SECP256k1'): {p2_actual}")
                                print(f"word1 (P3 from Dex_dict): {d1_word1_val}")
                                print(f"word2 (P6 from Dex_dict): {d2_word2_val}")
                                print(f"word3 (P10 from Dex_dict): {d3_word3_val}")
                                print(f"Derived Key: {master_priv_key_hex}")
                                
                                flag_word1 = d1_word1_val
                                flag_word2 = d2_word2_val
                                flag_word3 = d3_word3_val

                                final_flag_part = f"{flag_word1}_{flag_word2}_{flag_word3}_{master_priv_key_hex}"
                                print(f"FLAG: CDDC2025{{{final_flag_part}}}")
                                sys.stdout.flush()
                                return 

    print(f"\nFinished checking all combinations. No mnemonic found that derives the target private key.")

if __name__ == "__main__":
    solve()