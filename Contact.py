#!/usr/bin/env python3
"""Analyse a vampire infiltration.
   Vampire Hunting v1.4.4

   Student number: 23120221
"""

import sys
import os.path
from format_list import format_list, format_list_or, str_time, is_initial, period_of_time, day_of_time, time_of_day

# Section 2
def file_exists(file_name):
    """ Verify that the file exists.

    Args:
        file_name (str): name of the file

    Returns:
        boolean: returns True if the file exists and False otherwise.
    """
    return os.path.isfile(file_name)

# Section 3        
def parse_file(file_name):
    """Read input file

    Args:
        file_name (str): name of the file

    Returns:
        participants: list of participants.
        days: list of pairs; the first element of a pair is the result of tests
          (dictionary from participants to "H"/"V"); the second is a list of
          contact groups (list of lists of participants).
        or Print Error Message
    """
    with open(file_name, 'r') as file:
        lines = file.readlines()

        # Parse participants
        participants = lines[0].strip().split(', ')
        try:
            num_days = int(lines[1].strip())
        except ValueError:                
            print("Error found in file, aborting.")
            sys.exit()
        
        days = []
        current_line = 2

        for _ in range(num_days):
            test_results = {}
            contact_groups = []

            # Parse test results
            test_line = lines[current_line].strip()
            current_line += 1

            for entry in test_line.split(', '):
               if ':' in entry:  # Check if there's at least one colon
                    name, status = entry.split(':', 1)  # Split at the first colon
                    name = name.strip()
                    status = status.strip()
                    if status in ['H', 'V']:
                        # Convert status to boolean
                        test_results[name] = True if status == 'V' else False

            # Parse number of contact groups
            num_groups = int(lines[current_line].strip())
            current_line += 1

            for _ in range(num_groups):
                group_line = lines[current_line].strip()
                group = group_line.split(', ')
                contact_groups.append(group)
                current_line += 1

            days.append((test_results, contact_groups))

    return (participants,days)

# Section 4
def pretty_print_infiltration_data(data):
    """ Summarises and displays vampire infiltration data
     
    Args:
        Data (tulpe): participants, days 
        participants: list of participants.
        days: list of pairs; the first element of a pair is the result of tests
          (dictionary from participants to "H"/"V"); the second is a list of
          contact groups (list of lists of participants).

    Returns:
        print information about participants and their daily test results
    """
    # Unpack the tuple into participants and days
    participants, days = data

    # Calculate the number of days dynamically
    num_days = len(days)

    # Start of output
    print("Vampire Infiltration Data")
    print(f"{num_days} day{'s' if num_days > 1 else ''} with the following participants: {format_list(participants)}.")

    # Iterate over the days
    for day_number, day in enumerate(days, start=1):
        test_results, groups = day  # Unpack the day's data

        # Print day header
        print(f"Day {day_number} has {len(test_results)} vampire test{'s' if len(test_results) != 1 else ''} and "
              f"{len(groups)} contact group{'s' if len(groups) != 1 else ''}.")
        
        print(f"  {len(test_results)} test{'s' if len(test_results) != 1 else ''}")
        
        # Print tests
        for participant in sorted(test_results.keys()):  # Sort participants alphabetically
            result = test_results[participant]
            print(f"    {participant} is {'a vampire!' if result else 'human.'}")

        # Print groups
        if groups:
            print(f"  {len(groups)} group{'s' if len(groups) != 1 else ''}")
            for group in groups:
                formatted_group = format_list(sorted(group))  # Alphabetize and format group
                print(f"    {formatted_group}")
        else:
            print(f"  0 groups")

    # End of output
    print("End of Days")
    pass

# Section 5
def contacts_by_time(participant, time, contacts_daily):
    """ Retrive contact groups for participant
     
    Args:
        participant (str): Name of the participant.
        time (int): A time value (e.g., day index or similar) used to find the correct day.
        contacts_daily (list): A list of daily contact groups, where each element is a list
            of contact groups for a specific day, and each contact group is itself a list
            of participants.
    
    Returns:
        list: The contact group contianing the specified participant on the given day
    """
    # Handle of day 0
    if is_initial(time):
        return[]
    
    # Convert time to day index
    day = day_of_time(time) - 1

    # Ensure the day index is within the valid range    
    if day < 0 or day >= len(contacts_daily):
        return []

    # Retrieve the list of contacts for the specific day
    daily_contacts = contacts_daily[day]

    # Check if the participant is part of any contact group on this day
    for group in daily_contacts:
        if participant in group:
            return group  # Return the group containing the participant

    # If the participant is not found in any group, return an empty list
    return []

# Section 6
def create_initial_vk(participants):
    """ Creates and returns a vampire knowledge dictionary 
    
    Args:
        participant (str): Name of the participant.
    
    Returns:
        Dict: The key which are partcipants marked with value U
    """
    # 
    dict = {}
    for participant in participants:
        dict[participant]= 'U'
    return dict

def pretty_print_vampire_knowledge(vk):
    """ Pretty print vampire knoweldge structure
    
    Args:
        VK(dict): The key which are participnats and values are their status 
    """
    
    # Sort the lists alphabetically
    humans = sorted([name for name, status in vk.items() if status == 'H'])
    unclear = sorted([name for name, status in vk.items() if status == 'U'])
    vampires = sorted([name for name, status in vk.items() if status == 'V'])
    

    # Print the categories with proper formatting
    print(f"  Human{'s' if len(humans) != 1 else ''}:", format_list(humans))
    print(f"  Unclear individual{'s' if len(unclear) != 1 else ''}:", format_list(unclear))
    print(f"  Vampire{'s' if len(vampires) != 1 else ''}:", format_list(vampires))
    pass

# Done by professors
def pretty_print_vks(vks):
    print(f'Vampire Knowledge Tables')
    for i in range(len(vks)):
        print(f'Day {str_time(i)}:')
        pretty_print_vampire_knowledge(vks[i])
    print(f'End Vampire Knowledge Tables')

# Section 7
def update_vk_with_tests(vk, tests):
    """ Updates Vampire knowledge table with test results
     
    Args:
        Vk (dict): The key which are participnats and values are their test status
         
    Returns:
        Dict: updated vampire table with test reuslts
        or Prints Error Message
    """
    for participant, result in tests.items():
        # Check if the participant is in vk
        if participant not in vk:
            print("Error found in data: test subject is not a participant; aborting.")
            sys.exit()

        # Get the current status of the participant
        current_status = vk[participant]

        # Handle unclear individuals (U)
        if current_status == "U":
            vk[participant] = "V" if result else "H"

        # Handle humans (H) testing positive for vampires
        elif current_status == "H" and result:
            print("Error found in data: humans cannot be vampires; aborting.")
            sys.exit()

        # Handle vampires (V) testing negative for vampires
        elif current_status == "V" and not result:
            print("Error found in data: vampires cannot be humans; aborting.")
            sys.exit()
    return vk

# Section 8
def update_vk_with_vampires_forward(vk_pre, vk_post):
    """ Propagates vampire knowledge forward 
    
    Args:
        vk_pre(dict): Dictionary of participants and status earlier
        vk_post(dict): Dicitonary of participants and status later
        
    Returns:
        Updates vampire knoweledge table
        or Print Error Message
    """

    for participant, status_pre in vk_pre.items():
        status_post = vk_post.get(participant, "U")

        if status_pre == "V":
            # If the person was a vampire, they must remain a vampire in vk_post.
            if status_post == "H":
                print("Error found in data: vampires cannot be humans; aborting.")
                sys.exit()
            
            vk_post[participant] = "V"
        
        elif status_pre == "H":
            #humans can become vampire, remain human or become unkown
            if status_post == "V":
                print("Error found in data: vampires cannot be humans; aborting.")
                sys.exit()
            elif status_post == "H":
                vk_post[participant] = "H" #Remians human

        # Otherwise, leave their status or unchanged if it's unknown.
        elif status_pre == "U":
            vk_post[participant] = status_post
    return vk_post

# Section 9
def update_vk_with_humans_backward(vk_pre, vk_post):
    """ Propagates vampire knowledge forward 
    
    Args:
        vk_pre(dict): Dictionary of participants and status earlier
        vk_post(dict): Dicitonary of participants and status later
        
    Returns:
        Updates vampire knoweledge table
        or Print Error Message
    """
    for participant, status_post in vk_post.items():
        status_pre = vk_pre.get(participant, "U")

        if status_post == "H":
            # If the person was a vampire, they must remain a vampire in vk_post.
            if status_pre == "V":
                print("Error found in data: humans cannot be vampires; aborting.")
                sys.exit()
            
            vk_pre[participant] = "H"
            
        elif status_post == "V":
            #humans can become vampire or remain human
            if status_pre == "H":
                vk_post[participant] = "H" #Was vampire
            elif status_pre == "V":
                vk_post[participant] = "V" #Was human  

        # Otherwise, leave their status as-is or unchanged if it's unknown.
        elif status_post == "U":
            vk_pre[participant] = status_pre   
    
    return vk_pre

# Section 10
def update_vk_overnight(vk_pre, vk_post):
    """ Propagates vampire knowledge forward 
    
    Args:
        vk_pre(dict): Dictionary of participants and status previous day
        vk_post(dict): Dicitonary of participants and status next Am
        
    Returns:
        Updates vampire knoweledge table
        or Print Error Message
    """
    for participant, status_pre in vk_pre.items():
        status_post = vk_post.get(participant, "U")  # Default to "U" if not explicitly stated in vk_post

        if status_pre == "H":
            # Humans cannot become vampires overnight, remain human or become unknown.
            if status_post == "V":
                print("Error found in data: humans cannot be vampires; aborting.")
                sys.exit()
            vk_post[participant] = "H"  # Remain human

        elif status_pre == "V":
            # If the person was a vampire, they must remain a vampire in vk_post.
            if status_post == "H":
                print("Error found in data: vampires cannot be humans; aborting.")
                sys.exit()
            vk_post[participant] = "V"  # Remain vampire

        elif status_pre == "U":
            # If status is unknown in the evening, propagate as unknown.
            if status_post not in {"H", "V", "U"}:
                print("Error found in data: invalid status; aborting.")
                sys.exit()
            vk_post[participant] = status_post
    return vk_post

# Section 11
def update_vk_with_contact_group(vk_pre, contacts, vk_post):
    """ Updates vampire knowledge structure (vk_post) using contact group data

    Args:
        vk_pre (dict): Dictionary of participants and status before contacts
        contacts (list): A list of contact groups (each a list of participants)
        vk_post (dict): Dictionary of participants and status after contacts

    Returns:
        Updated vk_post structure
        or Print Error Message
    """
    # Validate all participants exist and check vampire-human contradictions
    all_participants = set(vk_pre.keys())
    
    # Check if all participants in contacts exist in vk_pre
    for group in contacts:
        for participant in group:
            if participant not in all_participants:
                print("Error found in data: contact subject is not a participant; aborting.")
                sys.exit()
    
    # Initial propagation and validation
    for participant, pre_status in vk_pre.items():
        if participant in vk_post:
            post_status = vk_post[participant]
            
            # Check vampire to human contradiction
            if pre_status == "V" and post_status == "H":
                print("Error found in data: vampires cannot be human; aborting.")
                sys.exit()
            
            # Propagate vampire status forward
            if pre_status == "V" and post_status == "U":
                vk_post[participant] = "V"
            
            # Check human to vampire contradiction
            if pre_status == "H" and post_status == "V":
                print("Error found in data: humans cannot be vampires; aborting.")
                sys.exit()
    
    # Handle uncontacted participants
    contacted = set()
    for group in contacts:
        contacted.update(group)
    
    uncontacted = all_participants - contacted
    
    for participant in uncontacted:
        pre_status = vk_pre[participant]
        # Propagate status for uncontacted participants
        if pre_status in ["H", "V"]:
            if participant in vk_post:
                post_status = vk_post[participant]
                if pre_status == "H" and post_status == "V":
                    print("Error found in data: humans cannot be vampires; aborting.")
                    sys.exit()
            vk_post[participant] = pre_status
    
    #  Process contact groups
    for group in contacts:
        # Get pre-contact statuses for the group
        group_pre_statuses = [vk_pre[p] for p in group]
        
        # Only propagate humanness if all members were definitely human
        if all(status == "H" for status in group_pre_statuses):
            for participant in group:
                if participant in vk_post and vk_post[participant] == "V":
                    print("Error found in data: humans cannot be vampires; aborting.")
                    sys.exit()
                vk_post[participant] = "H"
    
    return vk_post

# Section 12
def find_infection_windows(vks):
    """ find infection window of participants
    
    Args:
        vks(dict): Dictionary of participants and status
    
    Returns:
        windows(tulpe): last time they were confirmed human = earlist human time,
        first time they were vampire = last human time
    """
    windows = {}

    # Itereare over each time unit
    for time_unit in range (len(vks)):
        snapshot = vks[time_unit]

        # Check each participant's status at current time 
        for participant, status in snapshot.items():
            if status == 'V':
                if participant not in windows:
                    # Initialize start to the last possible human state (0 if no prior status)
                    last_human_time = time_unit - 1
                    while last_human_time >= 0 and vks[last_human_time].get(participant) not in {"H"}:
                        last_human_time -= 1
                    
                    # If not found defalut to 0
                    if last_human_time < 0:
                        last_human_time=0

                    windows[participant] = (last_human_time, time_unit)

    return windows

def pretty_print_infection_windows(iw):
    """Pretty print infection windows
    
    Args:
        iw(dcit): Dictionary where participant and value (last human time, time unit) 
        last time they were confirmed human = earlist human time,
        first time they were vampire = last human time 
        
    """
    for participant, (last_human_time, time_unit) in sorted(iw.items()):
        print(f"  {participant} was turned between day {str_time(max(0, last_human_time))} and day {str_time(time_unit)}.")
    pass

# Section 13
def find_potential_sires(iw, groups):
    """ Find potential sires
    
    Args:
        iw(dict): Dictionary where participants and value tulpe (last human time, time unit)
        groups(list): List of daily contact infotmation
          
    Returns:
        sires(dict): Dictionary where vampire and value tulpe(group)  
    """
    sires = {}

    for vampire, (last_human_time, time_unit) in iw.items(): 
        sires[vampire] = []

        for time in range(last_human_time,time_unit + 1): #convert am to pm
            if not period_of_time(time): #check for pm
                day = day_of_time(time) - 1 #index correction

                if 0 <= day < len(groups):
                    contacts =sorted(groups[day])
                    matched_groups = [small_group for small_group in contacts if vampire in small_group]

                    # If no group was found, mark with ["(None)"]
                    if matched_groups:
                        for mg in matched_groups:
                            sires[vampire].append((time, mg))
                    else:
                        sires[vampire].append((time, ["(None)"]))
                else:
                    # Day index out of range — no data for this time
                    sires[vampire].append((time, ["(None)"]))

                # Sorted vampire alphabetically 
                sires[vampire] = sorted(sires[vampire])

    return sires

def pretty_print_potential_sires(ps):
    """ Pretty print potential sires
     
    Args: 
        ps(dict): potential sires structure where keys are vampires and values are lists of tuples 
        (time unit, list of contacts)  
    """
    for vampire, groups in sorted(ps.items()):
        print(f"  {vampire}:")
        if not groups or groups == ["(None)"]:
            print("    (None)")
        else:
            for time_unit, contacts in groups:
                if contacts == '(None)':
                    print(f"    On day {str_time(time_unit)}, met with (None).")
                else:
                    print(f"    On day {str_time(time_unit)}, met with {format_list(contacts)}.")
    pass

# Section 14
def trim_potential_sires(ps,vks):
    """ Trim potential sires 
    
    Args: 
        ps(dict): potential sires structure where keys are vampires and values are lists of tuples 
        (time unit, list of contacts)
        vks(dict): list of dictionary for each time unit matching participants to status
        
    Returns:
        ps(dict): potential sires structure where keys are vampires and values are lists of tuples 
        (time unit, list of contacts)
    """

    # delete empty contact day and themself
    for key in ps.keys():
        contact = ps[key]
        if contact:
            new_contact = []
            for con in contact:
                if "(None)" not in con[1]:
                    new_c = []
                    for c in con[1]:
                        if c != key and vks[con[0]][c] != 'H':
                            new_c.append(c)
                    if new_c:
                        new_contact.append((con[0],new_c))
            contact = new_contact
        ps[key] = contact

    return ps

# Section 15
def trim_infection_windows(iw, ps):
    """ Trim infection windows
    Args:
        iw(dict): Dictionary where participants and value tulpe (last human time, time unit)
        ps(dict): potential sires structure where keys are vampires and values are lists of tuples 
        (time unit, list of contacts)
    
    Returns:
        iw(dict): Dictionary where participants and value tulpe (last human time, time unit)
    """

    for vampire, (start, end) in iw.items():
        # Default case for first day
        if start == 0 and end == 1:
            iw[vampire] = (start, start)
        else:
            candidate = [item for item in ps.get(vampire, []) if start <= item[0] <= end]

            if not candidate:
                iw[vampire] = (start, start)
            elif len(candidate) == 1:
                meet_time, _ = candidate[0]
                iw[vampire] = (0, meet_time) if start == 0 else (meet_time, meet_time)
            else:
                # Collect and deduplicate meeting times
                candidate_meet_times = list({item[0] for item in candidate})
                iw[vampire] = ((0, max(candidate_meet_times)) if start == 0 else (min(candidate_meet_times), max(candidate_meet_times)))
    return iw

# Section 16
def update_vks_with_windows(vks,iw):
    """ Update vampire knwoledge structure with infection window
    
    Args:
        vks(dict): list of dictionary for each time unit matching participants to status
        iw(dict): Dictionary where participants and value tulpe (last human time, time unit)
    
    Returns:
        tulpe of vks and change
        or Print Error Message
    """
    changes = 0
    
    for participant, (start, end) in iw.items():
        # Update statuses before the start of the infection window
        for time in range(len(vks)):
            current_status = vks[time][participant]

            # Before the infection window
            if time < start:
                if current_status == 'V':
                    print("Error found in data: humans cannot be vampires; aborting.")
                    sys.exit()
                elif current_status == 'U':
                    vks[time][participant] = 'H'
                    changes += 1

            # After the infection window
            elif time >= end:
                if current_status == 'H':
                    print("Error found in data: vampires cannot be humans; aborting.")
                    sys.exit()
                elif current_status == 'U':
                    vks[time][participant] = 'V'
                    changes += 1

    return (vks,changes)

# Section 17; done by professors
def cyclic_analysis(vks,iw,ps):
    count = 0
    changes = 1
    while(changes != 0):
        ps = trim_potential_sires(ps,vks)
        iw = trim_infection_windows(iw,ps)
        (vks,changes) = update_vks_with_windows(vks,iw)
        count = count + 1
    return (vks,iw,ps,count)

# Section 18: vampire strata
def vampire_strata(iw):
    """ Categorise vampires into strata based on windows
    
    Args:
        iw(dict): Dictionary where participants and value tulpe (last human time, time unit)
    
    Returns:
        tuple of orginals, unclear_vamps, newborns
    """

    originals = set()
    unclear_vamps = set()
    newborns = set()

    for name,(start,end) in iw.items():
        if start == 0:
            if end == 0:
                originals.add(name)
            else:
                unclear_vamps.add(name)
        else:
            newborns.add(name)

    return (originals,unclear_vamps,newborns)
 
def pretty_print_vampire_strata(originals, unclear_vamps, newborns):
    """ Pretty print vampire strata
    
    Args:
        orginails: Collection of participants identified as orginal vampires
        unclear_vamps: Collection of participants identified as unclear origins
        newborns:Collection of participants identified as new vampires
    """
    print(f"  Original vampires: {format_list(list(originals))}")
    print(f"  Unknown strata vampires: {format_list(list(unclear_vamps))}")
    print(f"  Newborn vampires: {format_list(list(newborns))}")

    pass

# Section 19: vampire sire sets
def calculate_sire_sets(ps):
    """ Calculate sires of participants into one set
     
    Args:
        ps(dict): potential sires structure where keys are vampires and values are lists of tuples 
        (time unit, list of contacts)
    
    Returns:
        ss(dict): potential sires structure where keys are vampires and values are potential sires
    """
    ss = {}

    for vampire, encounters in ps.items():
        # If vampire has contacts
        if encounters:
            vamp_encounters = [] 
            for contact in encounters:
                vamp_encounters += contact[1]
            ss[vampire]=set(vamp_encounters)
        else:
            ss[vampire]=set()

    return ss

def pretty_print_sire_sets(ss,iw,vamps,newb):
    """ Pretty print sire sets 

    Args:
        ss(dict): potential sires structure where keys are vampires and values are potential sires
        iw(dict): Dictionary where participants and value tulpe (last human time, time unit)
        vamps(list): list of vampires
        newb (bool): Flag to see if vampires are newborns(True) or unclear (False)
    """
    # Print the header based on the strata type
    if newb:
        print("Newborn vampires:")
    else:
        print("Vampires of unknown strata:")

    # Handle empty vampire set
    if not vamps:
        print("  (None)")
        return

    # Process each vampire
    for vampire in sorted(vamps):
        candidate_sires = ss[vampire]
        start, end = iw.get(vampire, (0, 0))

        # Filter sires whose infection windows conflict with the vampire's infection window
        valid_sires = [sire for sire in candidate_sires if sire not in iw or iw[sire][1] > start or iw[sire][0] < end]

        # Create descriptions for time and sires
        if start == end:
            time_desc = f"on day {str_time(start)}"
        else:
            time_desc = f"between day {str_time(start)} and day {str_time(end)}"

        if len(valid_sires) == 1:
            sire_desc = valid_sires[0]
        else:
            sire_desc = format_list_or(valid_sires)

        # Print the formatted output with proper phrasing
        if newb:
            print(f"  {vampire} was sired by {sire_desc} {time_desc}.")
        else:
            print(f"  {vampire} could have been sired by {sire_desc} {time_desc}.")
    pass

# Section 20: vampire sire sets
def find_hidden_vampires(ss,iw,vamps,vks):
    """ Find hiiden vampires

    Args:
        ss(dict): potential sires structure where keys are vampires and values are potential sires
        iw(dict): Dictionary where participants and value tulpe (last human time, time unit)
        vamps(list): list of vampires
        newb (bool): Flag to see if vampires are newborns(True) or unclear (False)

    Returns:
        tulpe of vks and changes
        or Error Message
     """
    changes = 0

    for vampire in vamps:  # Iterate through all vampires (not just newborns)
        if len(ss[vampire]) != 1:  # Only process vampires with one sire
            continue

        # Get the sire and infection window
        sire = list(ss[vampire])[0] 
        (start, end) = iw.get(vampire, (0, 0))  # Get infection window (default: (0, 0))

        # Update sire's status after the infection window
        for time in range(end, len(vks)):
            if vks[time][sire] == 'H':  
                print("Error found in data: vampires cannot be humans; aborting.")
                sys.exit()
            elif vks[time][sire] == 'U':  
                vks[time][sire] = 'V'
                changes += 1

        # Update sire's status before the infection window (if applicable)
        if start != 0 and start % 2 == 0:
            previous_status = vks[start - 1][sire]
            if previous_status == 'H':  
                print("Error found in data: vampires cannot be humans; aborting.")
                sys.exit()
            elif previous_status == 'U': 
                vks[start - 1][sire] = 'V'
                changes += 1

    return (vks,changes)

# Section 21; done by professor
def cyclic_analysis2(vks,groups):
    count = 0
    changes = 1
    while(changes != 0):
        iw = find_infection_windows(vks)
        ps = find_potential_sires(iw, groups)
        vks,iw,ps,countz = cyclic_analysis(vks,iw,ps)
        o,u,n = vampire_strata(iw)
        ss = calculate_sire_sets(ps)
        vks,changes = find_hidden_vampires(ss,iw,n,vks)        
        count = count + 1
    return (vks,iw,ps,ss,o,u,n,count)

def main():
    """Main logic for the program.  Do not change this (although if 
       you do so for debugging purposes that's ok if you later change 
       it back...)
    """
    filename = ""
    # Get the file name from the command line or ask the user for a file name
    args = sys.argv[1:]
    if len(args) == 0:
        filename = input("Please enter the name of the file: ")
    elif len(args) == 1:
        filename = args[0]
    else:
        print("""\n\nUsage\n\tTo run the program type:
        \tpython contact.py infile
        where infile is the name of the file containing the data.\n""")
        sys.exit()

    # Section 2. Check that the file exists
    if not file_exists(filename):
        print("File does not exist, ending program.")
        sys.exit()

    # Section 3. Create contacts dictionary from the file
    # Complete function parse_file().
    data = parse_file(filename)
    participants, days = data
    tests_by_day = [d[0] for d in days]
    groups_by_day = [d[1] for d in days]

    # Section 4. Print contact records
    pretty_print_infiltration_data(data)

    # Section 5. Create helper function for time analysis.
    print("********\nSection 5: Lookup helper function")
    if len(participants) == 0:
        print("  No participants.")
    else:
        p = participants[0]
        if len(days) > 1:
            d = 2
        elif len(days) == 1:
            d = 1
        else:
            d = 0
        t = time_of_day(d,True)
        t2 = time_of_day(d,False)
        print(f"  {p}'s contacts for time unit {t} (day {day_of_time(t)}) are {format_list(contacts_by_time(p,t,groups_by_day))}.")
        print(f"  {p}'s contacts for time unit {t2} (day {day_of_time(t2)}) are {format_list(contacts_by_time(p,t2,groups_by_day))}.")

    # Section 6.  Create the initial data structure and pretty-print it.
    print("********\nSection 6: create initial vampire knowledge tables")
    vks = [create_initial_vk(participants) for i in range(1 + (2 * len(days)))]
    pretty_print_vks(vks)

    # Section 7.  Update the VKs with test results.
    print("********\nSection 7: update the vampire knowledge tables with test results")
    for t in range(1,len(vks),2):
        vks[t] = update_vk_with_tests(vks[t],tests_by_day[day_of_time(t)-1])
    pretty_print_vks(vks)

    # Section 8.  Update the VKs to push vampirism forwards in time.
    print("********\nSection 8: update the vampire knowledge tables by forward propagation of vampire status")
    for t in range(1,len(vks)):
        vks[t] = update_vk_with_vampires_forward(vks[t-1],vks[t])
    pretty_print_vks(vks)

    # Section 9.  Update the VKs to push humanism backwards in time.
    print("********\nSection 9: update the vampire knowledge tables by backward propagation of human status")
    for t in range(len(vks)-1, 0, -1):
        vks[t-1] = update_vk_with_humans_backward(vks[t-1],vks[t])
    pretty_print_vks(vks)

    # Sections 10 and 11.  Update the VKs to account for contact groups and safety at night.
    print("********\nSections 10 and 11: update the vampire knowledge tables by forward propagation of contact results and overnight")
    for t in range(1, len(vks), 2):
        vks[t+1] = update_vk_with_contact_group(vks[t],groups_by_day[day_of_time(t)-1],vks[t+1])
        if t + 2 < len(vks):
            vks[t+2] = update_vk_overnight(vks[t+1],vks[t+2])
    pretty_print_vks(vks)

    # Section 12. Find infection windows for vampires.
    print("********\nSection 12: Vampire infection windows")
    iw = find_infection_windows(vks)
    pretty_print_infection_windows(iw)

    # Section 13. Find possible vampire sires.
    print("********\nSection 13: Find possible vampire sires")
    ps = find_potential_sires(iw, groups_by_day)
    pretty_print_potential_sires(ps)

    # Section 14. Trim the potential sire structure.
    print("********\nSection 14: Trim potential sire structure")
    ps = trim_potential_sires(ps,vks)
    pretty_print_potential_sires(ps)

    # Section 15. Trim the infection windows.
    print("********\nSection 15: Trim infection windows")
    iw = trim_infection_windows(iw,ps)
    pretty_print_infection_windows(iw)

    # Section 16. Update the vk structures with infection windows.
    print("********\nSection 16: Update vampire information tables with infection window data")
    (vks,changes) = update_vks_with_windows(vks,iw)
    pretty_print_vks(vks)
    str_s = "" if changes == 1 else "s"
    print(f'({changes} change{str_s})')

    # Section 17.  Cyclic analysis for sections 14-16 
    print("********\nSection 17: Cyclic analysis for sections 14-16")
    vks,iw,ps,count = cyclic_analysis(vks,iw,ps)
    str_s = "" if count == 1 else "s"    
    print(f'Detected fixed point after {count} iteration{str_s}.')
    print('Potential sires:')
    pretty_print_potential_sires(ps)
    print('Infection windows:')
    pretty_print_infection_windows(iw)
    pretty_print_vks(vks)       

    # Section 18.  Calculate vampire strata
    print("********\nSection 18: Calculate vampire strata")
    (origs,unkns,newbs) = vampire_strata(iw)
    pretty_print_vampire_strata(origs,unkns,newbs)

    # Section 19.  Calculate definite sires
    print("********\nSection 19: Calculate definite vampire sires")
    ss = calculate_sire_sets(ps)
    pretty_print_sire_sets(ss,iw,unkns,False)
    pretty_print_sire_sets(ss,iw,newbs,True)    

    # Section 20.  Find hidden vampires
    print("********\nSection 20: Find hidden vampires")
    (vks, changes) = find_hidden_vampires(ss,iw,newbs,vks)
    pretty_print_vks(vks)           
    str_s = "" if changes == 1 else "s"
    print(f'({changes} change{str_s})')

    # Section 21.  Cyclic analysis for sections 14-20
    print("********\nSection 21: Cyclic analysis for sections 14-20")
    (vks,iw,ps,ss,o,u,n,count) = cyclic_analysis2(vks,groups_by_day)
    str_s = "" if count == 1 else "s"    
    print(f'Detected fixed point after {count} iteration{str_s}.')
    print("Infection windows:")
    pretty_print_infection_windows(iw)
    print("Vampire potential sires:")
    pretty_print_potential_sires(ps)
    print("Vampire strata:")
    pretty_print_vampire_strata(o,u,n)
    print("Vampire sire sets:")    
    pretty_print_sire_sets(ss,iw,u,False)
    pretty_print_sire_sets(ss,iw,n,True)
    pretty_print_vks(vks)       
    
if __name__ == "__main__":
    main()
