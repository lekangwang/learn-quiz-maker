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
