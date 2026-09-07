# A simple list to hold all the study sessions
sessions_list = []

# load from the text file when program starts
def load_sessions():
    try:
        # reading the file line by line
        file = open("study_log.txt", "r")
        for line in file:
            # remove the hidden enter key at the end and split by comma
            clean_line = line.strip()
            if clean_line != "":
                parts = clean_line.split(",")
                new_session = {
                    "subject": parts[0],
                    "topic": parts[1],
                    "date": parts[2],
                    # turn the duration back into a number
                    "duration": int(parts[3]) 
                }
                sessions_list.append(new_session)
        file.close()
    except FileNotFoundError:
        # if the file is not there, just ignore it so it doesn't crash on the first run
        pass

# save everything to the text file when closing
def save_sessions():
    file = open("study_log.txt", "w")
    for session in sessions_list:
        # putting commas between the things so it is easy to split later
        line = session["subject"] + "," + session["topic"] + "," + session["date"] + "," + str(session["duration"])
        file.write(line + "\n")
    file.close()

# figure out if the study time is short, medium, or long
def classify_session(duration):
    if duration < 30:
        return "Short"
    elif duration >= 30 and duration <= 90:
        return "Medium"
    else:
        return "Long"

# add a new study time to the list
def add_session():
    subject_name = input("Type the subject name: ")
    topic_covered = input("What was the topic? ")
    date_or_day = input("Enter the date or day: ")

    # loop until they type a good number for the minutes
    while True:
        time_input = input("How many minutes did you study? ")
        try:
            session_duration = int(time_input)
            if session_duration > 0:
                break
            else:
                print("Try again with a positive number!")
        except ValueError:
            print("That is not a number. Type a real number.")
    
    # making a dictionary to group the session details
    new_session = {
        "subject": subject_name,
        "topic": topic_covered,
        "date": date_or_day,
        "duration": session_duration
    }
    sessions_list.append(new_session)
    print("Session added successfully!")

# show all the sessions on the screen
def view_sessions():
    # checking if the list has nothing in it
    if len(sessions_list) == 0:
        print("No sessions logged yet.")
        return
    
    print("Subject | Topic | Duration | Category")
    print("---------------------------------------")
    for session in sessions_list:
        # get the category string from our other function
        cat = classify_session(session["duration"])
        print(session["subject"] + " | " + session["topic"] + " | " + str(session["duration"]) + " mins | " + cat)

# search for a specific subject
def search_by_subject():
    target_subject = input("Which subject do you want to find? ")
    found_count = 0
    total_time = 0
    
    print("Subject | Topic | Duration | Category")
    print("---------------------------------------")
    
    for session in sessions_list:
        # making both strings lower case so it matches even if typing is messy
        if session["subject"].lower() == target_subject.lower():
            cat = classify_session(session["duration"])
            print(session["subject"] + " | " + session["topic"] + " | " + str(session["duration"]) + " mins | " + cat)
            total_time = total_time + session["duration"]
            found_count = found_count + 1
            
    if found_count == 0:
        print("Could not find any sessions for: " + target_subject)
    else:
        print("Total time spent on " + target_subject + " is " + str(total_time) + " minutes.")

# do some math and find the longest and weakest subjects
def study_statistics():
    if len(sessions_list) == 0:
        print("Not enough data to show statistics.")
        return
        
    total_overall_mins = 0
    subject_totals = {}
    longest_session = None
    
    for session in sessions_list:
        # 1. add up all the time
        total_overall_mins = total_overall_mins + session["duration"]
        
        # 2. figure out time per subject
        if session["subject"] in subject_totals:
            subject_totals[session["subject"]] = subject_totals[session["subject"]] + session["duration"]
        else:
            subject_totals[session["subject"]] = session["duration"]
            
        # 3. keep track of the longest session
        if longest_session == None:
            longest_session = session
        elif session["duration"] > longest_session["duration"]:
            longest_session = session
            
    # doing some math to get hours
    total_hours = total_overall_mins / 60
    print("Total hours studied overall: " + str(total_hours))
    
    print("Total hours per subject:")
    weakest_subject = ""
    # putting a really big number so it gets replaced immediately
    minimum_time = 9999999 
    
    for sub in subject_totals:
        hours = subject_totals[sub] / 60
        print(sub + " - " + str(hours) + " hours")
        # checking if this subject is the new lowest
        if subject_totals[sub] < minimum_time:
            minimum_time = subject_totals[sub]
            weakest_subject = sub
            
    print("Weakest area (least time studied): " + weakest_subject)
    print("Longest single session was " + str(longest_session["duration"]) + " minutes on " + longest_session["subject"])

# the main menu that keeps showing up until you quit
def main():
    load_sessions() # load stuff first from the file
    
    while True:
        print("")
        print("___ Smart Study Planner Menu ___")
        print("1. Add a study session")
        print("2. View all sessions")
        print("3. Search sessions by subject")
        print("4. View statistics")
        print("5. Save and exit")
        
        choice = input("Pick a number: ")
        
        if choice == "1":
            add_session()
        elif choice == "2":
            view_sessions()
        elif choice == "3":
            search_by_subject()
        elif choice == "4":
            study_statistics()
        elif choice == "5":
            save_sessions()
            print("Data saved. Bye!")
            break
        else:
            print("That is not a valid choice. Pick 1, 2, 3, 4, or 5.")

# python trick to make sure the program starts here
if __name__ == "__main__":
    main()