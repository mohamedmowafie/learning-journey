import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # To get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Which city\'s would you like to explore? Chicago, New York City, or Washington?: ')
    while city not in (CITY_DATA.keys()):
        print('Please use the cities I mentioned')
        city = input('Which city\'s would you like to explore? Chicago, New York City, or Washington?: ').lower()
    # To get user input filter (month, day, both)
    filter = input('Do you wish to filter your data by month, day, or both?: ').lower()
    # To get user input for month (all, january, february, ... , june)
    while filter not in ('month', 'day', 'both'):
        print('Invalid input! please try again')
        filter = input('Do you wish to filter your data by month, day, or both?: ').lower() 
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    if filter  == 'month' or filter == 'both':
       month = input('Which month do you wish to choose? eg: january, february...june, all: ').lower()
       while month not in months:
            print('Your input is invalid please choose from months: january through june: ')
            month = input('Which month do you wish to choose? eg: january, february...june, all: ').lower()
    else:
        month = 'all'
    # To get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    if filter == 'day' or filter == 'both' :
        day = input('Which day of the week would you like to choose? monday, tuesday...sunday, all: ')
        while day not in days:
            print('Your input is invalid please check your spelling')
            day = input('Which day of the week would you like to choose? monday, tuesday...sunday, all: ')
    else:
        day = 'all'
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df

    
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # To display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = df['month'].mode()[0]
    print(f'The most common month is {months[month - 1]}')
    # To display the most common day of week
    day = df['day_of_week'].mode()[0]
    print(f'The most common day of week is {day}')
    # To display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    # To find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print(f'The most common hour is {popular_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # To display most commonly used start station
    mostcommon_start_station = df['Start Station'].mode()[0]
    print(f'The most common start station is: {mostcommon_start_station}')
    # To display most commonly used end station
    mostcommon_end_station = df['End Station'].mode()[0]
    print(f'The most common end station is: {mostcommon_end_station}')
    # To display most frequent combination of start station and end station trip
    mostcommon_combination_stations = 'from ' + df['Start Station'] + ' to ' + df['End Station']
    print(f'The most common combination of start and end stations is: { mostcommon_combination_stations.mode()[0]}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    from datetime import timedelta as td
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # To display total travel time
    total_travel_time = (pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])).sum()
    days = total_travel_time.days
    hours = total_travel_time.seconds // (60 * 60) 
    minutes = total_travel_time.seconds % (60 * 60) // 60
    seconds = total_travel_time.seconds % (60 * 60) % 60
    print(f'total travel time is: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds')
    # To display mean travel time
    average_total_travel = (pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])).mean()
    days = total_travel_time.days
    hours = total_travel_time.seconds // (60 * 60) 
    minutes = total_travel_time.seconds % (60 * 60) // 60
    seconds = total_travel_time.seconds % (60 * 60) % 60
    print(f'average total travel is: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # To display counts of user types
    user_types = df['User Type'].value_counts()
    print(f'Counts of user types are: {user_types}')
    # To display counts of gender
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print(f'The gender counts are: {gender_counts}')
    else:
        print('information weren\'t collected')    
    # To display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        birth_earliest = df['Birth Year'].min()
        birth_recent = df['Birth Year'].max()
        birth_common = df['Birth Year'].mode()[0]
        print(f'The youngest rider was born on: {birth_recent}\n The oldest rider was born on: {birth_earliest}\n Riders with the most common age were born on: {birth_common}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def row_data(df):
    row_data =  0
    while True:
        answer = input('Do you want to dispaly the raw data? Yes or No').lower()
        if answer not in ['yes', 'no']:
            answer = input('Invalid input, please try again yes/no?').lower()
        elif answer == 'yes':
            row_data += 5
            print(df.iloc[row_data: row_data +5])
            answer_more = ('Do you want to see more row data? Yes or No').lower()
            if answer_more == 'no':
                break
        elif answer == 'no':
            return answer


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        row_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
