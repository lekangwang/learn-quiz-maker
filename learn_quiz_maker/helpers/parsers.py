from csv import DictReader

# Helper function to parse the first section of the full title
# before the comma (i.e. long_title format: "true_title, other_stuff")
def parse_course_title(long_title):
    title_arr = long_title.split(",")
    true_title = title_arr[0]
    return true_title

# Parse CSV settings file to list of Python dicts
def parse_settings(path, csv_filename):
    # Locate the settings.csv file
    csv_path = path + csv_filename

    # Open the csv file, 
    # convert csv file to a list of objects
    with open(csv_path, encoding="utf-8", errors="ignore") as s:
        settings = list(DictReader(s))
        return settings

# Generate a list of unique section names from learn-quiz-template.csv file
def parse_section_names(quiz_questions):
    section_names = set()

    # Add each question name to the set to remove duplicate section names
    # as sets discard duplicate values
    for question in quiz_questions:
        section_names.add(question["Section"])
    
    # Return the unique section names as an array
    return list(section_names)

# For questions.py: used to convert csv options data (Format: (stuff) (more stuff)) 
# into a list of separated options
# I refer to a string using round braces "(Text 1) (Text 2)" from the quiz csv
# file as rounded_str 
def parse_csv_round_braces(rounded_str):
    parsed_list = rounded_str.split("-")

    # Iterate and remove the rounded braces from each item
    for (i, item) in enumerate(parsed_list):
        parsed_list[i] = item[1:-1]

    print(f"parse_csv_round_braces: {parsed_list}")
    return parsed_list
