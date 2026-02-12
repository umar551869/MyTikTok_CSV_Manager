import re

def extract_usernames_from_text(text):
    """
    Extract usernames using smart heuristics (PPS anchor) and fallback to regex.
    Returns: (list of usernames, list of debug strings)
    """
    debug_log = []
    
    if not text:
        return [], ["No text provided"]
        
    lines = [L.strip() for L in text.split('\n') if L.strip()]
    debug_log.append(f"Found {len(lines)} non-empty lines")
    
    smart_matches = []
    
    # Strategy 1: PPS Anchor
    # Pattern: Username is 2 lines above "PPS:"
    pps_found = False
    for i, line in enumerate(lines):
        # Case insensitive check for PPS
        if "PPS:" in line.upper():
            pps_found = True
            if i >= 2:
                candidate = lines[i-2]
                # Basic validation: no spaces, decent length, not a number
                if ' ' not in candidate and len(candidate) >= 3:
                    smart_matches.append(candidate)
                    debug_log.append(f"Line {i} PPS found -> Accepted candidate '{candidate}'")
                else:
                    debug_log.append(f"Line {i} PPS found -> Rejected candidate '{candidate}' (invalid format)")
            else:
                debug_log.append(f"Line {i} PPS found -> No candidate (index < 2)")
                
    if smart_matches:
        debug_log.append(f"Strategy 1 (PPS) Success: {len(smart_matches)} matches")
        return sorted(list(set(smart_matches))), debug_log
        
    debug_log.append("Strategy 1 (PPS) returned 0 valid matches. Falling back to regex.")
        
    # Strategy 2: Fallback Regex with Stronger Filtering
    pattern = r'@?([a-zA-Z0-9_.]+)'
    raw_matches = re.findall(pattern, text)
    debug_log.append(f"Regex found {len(raw_matches)} raw matches")
    
    # Expanded blacklist (lowercase for comparison)
    blacklist_set = {
        'health', 'male', 'female', 'previously', 'invited', 'fast', 'growing', 
        'pps:', 'pps', 'womenswear', 'underwear', 'beauty', 'personal', 'care',
        'sports', 'outdoor', 'ugc', 'level', 'deals', 'next', 'locked', 'mindset',
        'midlifemomgrace', 'soberafjoe', 
        'chenbo', 'unknown', 'creator', 'video', 'views', 'follower', 'sale', 'revenue'
    }
    
    cleaned_matches = []
    for m in raw_matches:
        clean = m.strip()
        clean_lower = clean.lower()
        
        # 1. Length Check
        if len(clean) < 3:
            continue
            
        # 2. Character Check (Must have at least one letter)
        if not any(c.isalpha() for c in clean):
            continue
            
        # 3. Blacklist Check (Case Insensitive)
        if clean_lower in blacklist_set:
            continue
            
        # 4. Symbol Check
        if any(x in clean for x in ['/', '%', '$', ',']):
            continue
            
        # 5. Number/Stat Check (e.g. 1.4K, 4.1, 5.0)
        if clean[0].isdigit():
            if re.match(r'^[\d.]+[KMBkmb]?$', clean):
                continue
                
        cleaned_matches.append(clean)
            
    debug_log.append(f"Strategy 2 (Regex) Final: {len(cleaned_matches)} matches")
    return sorted(list(set(cleaned_matches))), debug_log

# Test Data from user's last message (partial sample for speed)
data = """
guadalupejaimes
Lupita jaimes💜
PPS: 4.1/5.0
Health
, +2
5.9K, Female 56%, 35-44
Previously invited
Previously invited

$1,262.34
100
109
4.6%


shwa2021
shwa2021
PPS: 3.6/5.0
Health
, +2
6.8K, Male 47%, 35-44
Previously invited
Fast growing
Previously invited
Fast growing

$40.4K
1.4K
1.8K
0.4%
"""

result, logs = extract_usernames_from_text(data)
print("DEBUG LOGS:")
for l in logs:
    print(l)
print("\nFINAL RESULT:")
for r in result:
    print(r)
