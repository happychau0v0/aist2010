import pandas as pd

# Load the dataset
df = pd.read_csv('dataset2.csv')

# General list of common Indian names (first, last) and song-related keywords
indian_keywords = [
    # Popular Indian first and last names, keywords in song titles
    "a.r.", "arijit", "alka", "udit", "sonu", "kishore", "mohammed", "lata", "shreya", "sunidhi",
    "palak", "neha", "badshah", "yo yo", "jubin", "ankit", "kanika", "vishal", "shekhar", 
    "amit", "armaan", "atif", "mika", "rahat", "sukhwinder", "ashok", "daler", "shankar",
    "ilayaraja", "anirudh", "sid", "yuvan", "harris", "devi", "ajay", "rochak", "guru", "darshan",
    "amitabh", "bappi", "asha", "salim", "anju", "anuradha", "antara", "bhuvan", "bhavya", "bhupinder",
    "lalit", "jatin", "vishal", "shantanu", "pankaj", "salman", "shraddha", "sukhbir", "jeet",
    "ali", "atif", "arjun", "divya", "harshdeep", "hardy", "honey", "himesh", "inder", "jasleen",
    "jasbir", "jaspreet", "jassie", "kamal", "kailash", "karan", "kavita", "keerthi", "manoj", 
    "mannat", "niti", "nidhi", "priya", "prasoon", "prateek", "ranjit", "rahul", "raj", "ram", 
    "reshma", "sanjeev", "santosh", "shiv", "shivani", "shruti", "sonal", "sonam", "sukhwinder", 
    "tanishk", "tulsi", "udit", "udit narayan", "yo yo honey singh", "zubeen", "yash", "shankar", 
    "rahman", "rehman", "aamir", "singh", "mangeshkar", "rafi", "yagnik", "nigam", "chauhan", 
    "malik", "kapoor", "mahadevan", "dosanjh", "maan", "gill", "grewal", "sandhu", "ravichander", 
    "kumar", "kakkar", "bhosle", "khan", "yadav", "jha", "tiwari", "verma", "desai", "narayan", 
    "mehta", "patel", "modi", "agarwal", "bhatt", "chopra", "das", "dey", "ganguly", "ghosh", 
    "iyer", "kaur", "khanna", "pandey", "rao", "reddy", "sehgal", "sharma", "sinha", "solanki", 
    "tagore", "thakur", "vaid", "wadhwa",
    
    # Common Indian song-related words
    "zindagi", "dil", "jaan", "pyar", "mohabbat", "hawa", "sapna", "ishq", "yaad", "mausam", 
    "shaadi", "dosti", "meri", "tere", "tum", "hai", "ho", "kya", "hindustani", "bollywood", 
    "desi", "aashiqui", "jung", "bharat", "hindustan", "watan", "aman", "jashn", "balam", 
    "chahat", "raat", "jai", "mahi", "diwana", "saath", "babu", "chal", "saajan", "sanam", 
    "raja", "rani", "mast", "jalwa", "rab", "chand", "sitare", "dard", "mehfil", "aankh", 
    "naina", "suno", "deewana", "pagal", "jai ho", "yaara", "sajna", "mahiya", "lag ja", 
    "gale", "zara", "sathiya", "bheegi", "dilwale", "chhupana", "roop", "prem", "leela", 
    "teri", "bachna", "ae", "haseeno", "chura", "dhoom", "masti", "badtameez", "besharam", 
    "munni", "sheila", "jawani", "chikni", "chameli", "jigar", "janeman"
    # Add more as needed...
]

# Convert keywords to lowercase for case-insensitive matching
indian_keywords_lower = [keyword.lower() for keyword in indian_keywords]

# Function to check if an artist's name or track name matches any Indian keywords
def contains_indian_keyword(text):
    if pd.isnull(text):
        return False  # Consider NaN as no match
    text_lower = str(text).lower()
    return any(keyword in text_lower for keyword in indian_keywords_lower)

# Apply the function to filter out Indian songs or artists
filtered_df = df[~df['artists'].apply(contains_indian_keyword) & ~df['track_name'].apply(contains_indian_keyword)]

# Save the filtered dataset to a new CSV file
filtered_df.to_csv('dataset3.csv', index=False)

print(f"Filtered dataset saved as 'dataset3.csv'. Original dataset had {len(df)} rows, filtered dataset has {len(filtered_df)} rows.")