import pandas as pd

def load_properties_from_excel(file_path):
    df = pd.read_excel(file_path)
    properties = df.to_dict(orient='records')
    return properties

def get_valid_input(prompt, valid_types, allow_any=True):
    while True:
        user_input = input(prompt).strip().lower()
        if allow_any and user_input == "any":
            return None
        try:
            value = valid_types(user_input)
            return value
        except ValueError:
            print(f"Invalid input. Please enter a valid {valid_types.__name__}.")

def ask_user_preferences():
    print("Please answer the following questions:")
    preferences = {}

    preferences["property_type"] = get_valid_input("Preferred property type (villa/apartment/any): ", str)
    preferences["city"] = get_valid_input("Preferred city (e.g., Riyadh/any): ", str)
    preferences["district"] = get_valid_input("Preferred district (or 'any'): ", str)
    preferences["facade"] = get_valid_input("Preferred facade (or 'any'): ", str)
    preferences["number_of_rooms"] = get_valid_input("Number of rooms (or 'any'): ", int)
    preferences["number_of_living_rooms"] = get_valid_input("Number of living rooms (or 'any'): ", int)
    preferences["number_of_bathrooms"] = get_valid_input("Number of bathrooms (or 'any'): ", int)
    preferences["area"] = get_valid_input("Area in sq. meters (or 'any'): ", int)
    preferences["kitchen"] = get_valid_input("Do you need a kitchen? (yes/no): ", lambda x: x in ["yes", "no"]) == 'yes'
    preferences["maids_room"] = get_valid_input("Do you need a maids room? (yes/no): ", lambda x: x in ["yes", "no"]) == 'yes'
    preferences["drivers_room"] = get_valid_input("Do you need a drivers room? (yes/no): ", lambda x: x in ["yes", "no"]) == 'yes'
    preferences["annex"] = get_valid_input("Do you need an annex? (yes/no): ", lambda x: x in ["yes", "no"]) == 'yes'
    preferences["yard"] = get_valid_input("Do you want a yard? (yes/no): ", lambda x: x in ["yes", "no"]) == 'yes'
    preferences["pool"] = get_valid_input("Do you want a pool? (yes/no): ", lambda x: x in ["yes", "no"]) == 'yes'
    preferences["basement"] = get_valid_input("Do you need a basement? (yes/no): ", lambda x: x in ["yes", "no"]) == 'yes'
    preferences["garage"] = get_valid_input("Do you need a garage? (yes/no): ", lambda x: x in ["yes", "no"]) == 'yes'
    preferences["elevator"] = get_valid_input("Do you need an elevator? (yes/no): ", lambda x: x in ["yes", "no"]) == 'yes'
    preferences["floor"] = get_valid_input("Preferred floor number (or 'any'): ", int)
    preferences["furnished"] = get_valid_input("Do you want a furnished property? (yes/no): ", lambda x: x in ["yes", "no"]) == 'yes'
    preferences["total_cost"] = get_valid_input("Total cost (in SAR, or 'any'): ", int)

    return preferences

def find_best_match(preferences, database):
    matches = []
    closest_matches = []
    weighted_differences = []
    weights = {
        "property_type": 1, "city": 2, "district": 3, "number_of_rooms": 2,
        "number_of_living_rooms": 2, "number_of_bathrooms": 2, "area": 1, "total_cost": 4
    }

    for property in database:
        difference = 0
        for key in preferences:
            if preferences[key] is not None and key in weights:
                if key == "total_cost":
                    difference += abs(preferences[key] - property[key]) * weights[key]
                elif key == "area":
                    difference += max(0, preferences[key] - property[key]) * weights[key]
                else:
                    difference += (preferences[key] != property[key]) * weights[key]

        if difference == 0:
            matches.append(property)
        else:
            closest_matches.append(property)
            weighted_differences.append((property, difference))

    sorted_closest_matches = sorted(weighted_differences, key=lambda x: x[1])
    top_3_closest_matches = [prop[0] for prop in sorted_closest_matches[:3]]

    return matches, top_3_closest_matches

def display_properties(properties):
    for prop in properties:
        print(f"\nProperty Type: {prop['property_type']}")
        print(f"City: {prop['city']}")
        print(f"District: {prop['district']}")
        print(f"Facade: {prop['facade']}")
        print(f"Number of Rooms: {prop['number_of_rooms']}")
        print(f"Number of Living Rooms: {prop['number_of_living_rooms']}")
        print(f"Number of Bathrooms: {prop['number_of_bathrooms']}")
        print(f"Area: {prop['area']} sq. meters")
        print(f"Kitchen: {'Yes' if prop['kitchen'] else 'No'}")
        print(f"Maids Room: {'Yes' if prop['maids_room'] else 'No'}")
        print(f"Drivers Room: {'Yes' if prop['drivers_room'] else 'No'}")
        print(f"Annex: {'Yes' if prop['annex'] else 'No'}")
        print(f"Yard: {'Yes' if prop['yard'] else 'No'}")
        print(f"Pool: {'Yes' if prop['pool'] else 'No'}")
        print(f"Basement: {'Yes' if prop['basement'] else 'No'}")
        print(f"Garage: {'Yes' if prop['garage'] else 'No'}")
        print(f"Elevator: {'Yes' if prop['elevator'] else 'No'}")
        print(f"Floor: {prop['floor']}")
        print(f"Furnished: {'Yes' if prop['furnished'] else 'No'}")
        print(f"Total Cost: {prop['total_cost']} SAR")

def main():
    file_path = '/Users/falmosllm/Downloads/data_pro.xlsx'

    property_database = load_properties_from_excel(file_path)

    user_preferences = ask_user_preferences()

    matches, closest_matches = find_best_match(user_preferences, property_database)

    if matches:
        print("\nExact Matches Found:")
        display_properties(matches)
    else:
        print("\nNo exact matches found. Here are the top 3 closest matches:")
        display_properties(closest_matches)

if __name__ == "__main__":
    main()
