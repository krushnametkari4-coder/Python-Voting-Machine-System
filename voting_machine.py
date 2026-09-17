import os
from PIL import Image, ImageDraw, ImageFont
import random
import qrcode
import pygame as py

arr = []
passw = []
party = []

# ---------------- MUSIC PLAY ----------------
py.mixer.init()
py.mixer.music.load("hariya.mp3")
py.mixer.music.play()

# ---------------- LOAD VOTERS ----------------
try:
    with open("voting machine.txt", "r") as f:
        for line in f:
            ad, name, g, dob, add, vote = line.strip().split(",")
            arr.append({
                "name": name,
                "adhar": ad,
                "gender": g,
                "dob": dob,
                "address": add,
                "vote": vote
            })
except:
    pass

# ---------------- LOAD PIN ----------------
try:
    with open("pin.txt", "r") as f:
        for line in f:
            ad, pin = line.strip().split(",")
            passw.append({
                "adhar": ad,
                "pin": pin
            })
except:
    pass

# ---------------- LOAD PARTY ----------------
def load_party():
    try:
        with open("party.txt", "r", encoding="utf-8") as f:
            for line in f:
                name, symbol, votes = line.strip().split(",")
                party.append({
                    "name": name,
                    "symbol": symbol,
                    "votes": int(votes)
                })
    except:
        pass

load_party()

# ---------------- SAVE FUNCTIONS ----------------
def save_data():
    with open("voting machine.txt", "w") as f:
        for p in arr:
            f.write(f"{p['adhar']},{p['name']},{p['gender']},{p['dob']},{p['address']},{p['vote']}\n")

def save_party():
    with open("party.txt", "w", encoding="utf-8") as f:
        for p in party:
            f.write(f"{p['name']},{p['symbol']},{p['votes']}\n")

def save_pin():
    with open("pin.txt", "w") as f:
        for p in passw:
            f.write(f"{p['adhar']},{p['pin']}\n")

# ---------------- DETAILS ----------------
def details():
    a = input("Enter Aadhaar: ").strip()

    for person in arr:
        if person["adhar"] == a:
            print("\nName:", person["name"])
            print("Gender:", person["gender"])
            print("DOB:", person["dob"])
            print("Address:", person["address"])
            print("Vote:", person["vote"])
            return

    print("Candidate not found ❌")

# ---------------- UPDATE ----------------
def update():
    print("1. Add Candidate\n2. Remove Candidate")
    c = int(input("Enter choice: "))

    if c == 1:
        a = input("Enter Aadhaar: ")

        for person in arr:
            if person["adhar"] == a:
                print("Already exists ❌")
                return

        name = input("Enter name: ")
        gender = input("Enter gender: ")
        dob = input("Enter DOB (DD-MM-YYYY): ")
        address = input("Enter address: ")

        arr.append({
            "name": name,
            "adhar": a,
            "gender": gender,
            "dob": dob,
            "address": address,
            "vote": "no"
        })

        save_data()
        print("Candidate added ✅")

    elif c == 2:
        a = input("Enter Aadhaar: ")

        for person in arr:
            if person["adhar"] == a:
                arr.remove(person)
                save_data()
                print("Removed ✅")
                return

        print("Not found ❌")

# ---------------- SET PIN ----------------
def setp():
    a = input("Enter Aadhaar: ")

    for person in arr:
        if person["adhar"] == a:
            pin = input("Enter 4 PIN: ")

            passw.append({
                "adhar": a,
                "pin": pin
            })

            save_pin()
            print("PIN set ✅")
            return

    print("Aadhaar not found ❌")

# ---------------- LOGIN ----------------
def authentication():
    a = input("Enter Aadhaar: ")
    b = input("Enter PIN: ")

    for p in passw:
        if p["adhar"] == a:
            if p["pin"] == b:
                print("Login successful ✅")
                return True
            else:
                print("Wrong PIN ❌")
                return False

    print("PIN not set ❌")
    return False

# ---------------- PARTY ----------------
def party1():
    k = int(input("Enter number of candidates: "))

    for i in range(k):
        name = input(f"Enter candidate name {i+1}: ")
        symbol = input("Enter symbol (⏰, 🌹, 🐘): ")

        party.append({
            "name": name,
            "symbol": symbol,
            "votes": 0
        })

    save_party()
    print("Party created ✅")

# ---------------- VOTE ----------------
def vote():
    a = input("Enter Aadhaar: ")

    for person in arr:
        if person["adhar"] == a:

            if person["vote"] == "no":

                print("\nCandidates:")
                for i, p in enumerate(party, 1):
                    print(i, p["name"], p["symbol"])

                choice = int(input("Choose candidate: "))

                if 1 <= choice <= len(party):
                    party[choice - 1]["votes"] += 1
                    person["vote"] = "yes"

                    save_party()
                    save_data()

                    print("Vote recorded ✅")
                else:
                    print("Invalid choice ❌")

            else:
                print("Already voted ❌")

            return   # stop after match

    print("Aadhaar not found ❌")

    

# ---------------- RESULT ----------------
def result():
    print("\nResults:")
    
    for p in party:
        print(f"{p['name']} ({p['symbol']}) -> {p['votes']} votes")

    if len(party) == 0:
        print("No candidates available ❌")
        return

    max_votes = max(p["votes"] for p in party)

    winners = [p for p in party if p["votes"] == max_votes]

    if len(winners) > 1:
        print("\n⚖️ It's a Tie between:")
        for w in winners:
            print(f"{w['name']} ({w['symbol']}) with {w['votes']} votes")
    else:
        winner = winners[0]
        os.system('msg * "🏆 Winner:"')
        os.system(f'msg * "{winner['name']} ({winner['symbol']}) with {winner['votes']} votes 🎉"')

# ----------------  VOTER ID ----------------

def create_voter_card(person):
    bg_color = (
        random.randint(150, 255),
        random.randint(150, 255),
        random.randint(150, 255)
    )

    img = Image.new('RGB', (500, 300), color=bg_color)
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except:
        font = ImageFont.load_default()

    voter_id = "VID" + str(random.randint(100000, 999999))

    draw.text((140, 10), "VOTER ID CARD", fill="black", font=font)

    draw.rectangle([0, 0, 499, 299], outline="black", width=3)

    draw.text((20, 60), f"Name: {person['name']}", fill="black", font=font)
    draw.text((20, 100), f"Aadhaar: {person['adhar']}", fill="black", font=font)
    draw.text((20, 140), f"Gender: {person['gender']}", fill="black", font=font)
    draw.text((20, 180), f"DOB: {person['dob']}", fill="black", font=font)
    draw.text((20, 220), f"ID: {voter_id}", fill="black", font=font)

    filename = f"{person['adhar']}_card.png"

    qr = qrcode.QRCode()
    qr.add_data(filename)
    draw.qr.make_image(fill_color = "black", back_color = "white")
    img.save(filename)
    img = qr.make_image(fill_color = "black", back_color = "white")
    img.save(f"{name}.png")

    print("...QR code generated successfully!...")
    os.system(f'msg * "...voter card created ✅... → {filename}"')

# ---------------- Reset System ----------------

def reset():
    print("\n...Reset the system...\n")
    c = input("\nYes or No : ").lower()

    if c == "yes" or c=="y":
        # Reset votes
        for p in party:
            p["votes"] = 0

        for person in arr:
            person["vote"] = "no"
   
        save_party()
        save_data()

        print("System reset successfully ✅")

    else:
        print("Reset cancelled ❌")
    py.mixer.music.stop()

# ---------------- MAIN MENU ----------------
def main():
    print("\n...Election Commition of India...")

    while True:
        print("\n1. Details\n2. Update\n3. Set PIN\n4. Login\n5. Party\n6. Vote\n7. Result\n 8. Voter Card\n 9.Reset the All the System\n")
        c = int(input("Enter choice: "))

        if c == 1:
            details()
        elif c == 2:
            update()
        elif c == 3:
            setp()
        elif c == 4:
            authentication()
        elif c == 5:
            party1()
        elif c == 6:
            vote()
        elif c == 7:
            result()
            break
        elif c == 8:
           a = input("Enter Aadhaar: ")
           for person in arr:
             if person["adhar"] == a:
               create_voter_card(person)
             
           else:
             print("Aadhaar not found ❌")
           break
        elif c==9:
                   reset()
                   break
        else:
            print("Invalid choice")

# ---------------- RUN ----------------
main()