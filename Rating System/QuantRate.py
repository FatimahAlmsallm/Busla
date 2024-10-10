import pandas as pd

file_path = '/Users/falmosllm/Downloads/neighbourhoods.rating.xlsx'
neighbourhoods_df = pd.read_excel(file_path, sheet_name='Sheet1')

neighbourhoods_df.columns = neighbourhoods_df.columns.str.strip().str.lower()

neighbourhoods_df.rename(columns={
    'neighbourhoods': 'neighbourhood',
    'public schools': 'public_schools',
    'private schools': 'private_schools',
    'kindergarten': 'kindergarten',
    'hospitals': 'hospitals',
    'pharmacies': 'pharmacies',
    'mosques': 'mosques',
    'supermarkets': 'supermarkets',
    'laundry': 'laundry',
    'barbers': 'barbers',
    'restaurant': 'restaurants',
    'malls': 'malls',
    'parks': 'parks',
    'sports': 'sports',
    'gas stations': 'gas_stations',
    'water availability': 'water_availability'
}, inplace=True)

new_preference_ratings = [
    8.05, 6.85, 6.84, 8.68, 9.2,
    9.52, 9.49, 8.52, 7.51, 8.18,
    6.88, 8.13, 7.84, 8.38, 9.26
]

preferences_data = {
    'Facility': ['public_schools', 'private_schools', 'kindergarten', 'hospitals', 'pharmacies',
                 'mosques', 'supermarkets', 'laundry', 'barbers', 'restaurants', 'malls',
                 'parks', 'sports', 'gas_stations', 'water_availability'],
    'Preference_Rating': new_preference_ratings,
}

preferences_df = pd.DataFrame(preferences_data)

def calculate_distribution_scores(neighbourhoods_df, preferences_df):
    neighbourhoods_df['Overall_Score'] = 0
    facilities = preferences_df['Facility'].tolist()


    missing_facilities = [facility for facility in facilities if facility not in neighbourhoods_df.columns]
    if missing_facilities:
        print(f"Missing facilities in neighbourhoods_df: {missing_facilities}")
        return neighbourhoods_df

    max_facilities = neighbourhoods_df[facilities].max()

    for facility in facilities:
        max_availability = max_facilities[facility]
        neighbourhoods_df[f'{facility}_availability'] = neighbourhoods_df[facility] / max_availability
        rating = preferences_df.loc[preferences_df['Facility'] == facility, 'Preference_Rating'].values[0] / 10
        neighbourhoods_df['Overall_Score'] += neighbourhoods_df[f'{facility}_availability'] * rating
        neighbourhoods_df[f'{facility}_rating'] = neighbourhoods_df[f'{facility}_availability'] * 5

    max_score = neighbourhoods_df['Overall_Score'].max()
    neighbourhoods_df['Overall_Rating_Out_of_5'] = (neighbourhoods_df['Overall_Score'] / max_score) * 5

    return neighbourhoods_df


rated_neighbourhoods = calculate_distribution_scores(neighbourhoods_df, preferences_df)


print("\nOverall Ratings:")
for idx, row in rated_neighbourhoods.iterrows():
    print(f"{idx + 1}. {row['neighbourhood']}: {row['Overall_Rating_Out_of_5']:.2f}")


selection = input("\nEnter the number of the neighborhood to see detailed ratings: ")

try:
    selection = int(selection)
    if 1 <= selection <= len(rated_neighbourhoods):
        neighbourhood_details = rated_neighbourhoods.iloc[selection - 1]
        print(f"\nDetailed Ratings for {neighbourhood_details['neighbourhood']}:")
        for facility in preferences_df['Facility']:
            print(f"{facility.replace('_', ' ').title()}: {neighbourhood_details[f'{facility}_rating']:.2f}")
    else:
        print("Invalid selection. Please enter a number corresponding to the listed neighbourhoods.")
except ValueError:
    print("Invalid input. Please enter a number.")

