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
    # convert csv file to a list of objects, 
    # return the first object
    with open(csv_path) as s:
        settings = list(DictReader(s))[0]
        return settings
    