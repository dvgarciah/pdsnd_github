# These are the sources from which I obtained information:
    # https://github.com/NidalShater/Udacity-My-Bike-share-Project/blob/master/bikeshare_2.py
    # https://stackoverflow.com/questions/50848454/pulling-most-frequent-combination-from-csv-columns
    # https://github.com/khaledimad/Explore-US-Bikeshare-Data/blob/master/bikeshare_2.py
    # https://es.acervolima.com/programa-python-para-convertir-segundos-en-horas-minutos-y-segundos/
    # https://github.com/pss2138/Udacity-Programming-for-Data-Science-with-Python-Project2/blob/master/bikeshare.py

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = ['all', 'january', 'february', 'march', 'april','may', 'june']

DAYS_DATA = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Select a city from the following: chicago, new york city, washington \n>').lower()
        if city not in CITY_DATA:
            print("Sorry, the data is incorrect. Please try again")
            continue
        else:
            break
    
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Select a month between january and june \n>').lower()
        if month not in MONTH_DATA:
            print("Sorry, the data is incorrect. Please try again")
            continue
        else:
            break
  
# get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Select a day of week \n>').lower()
        if day not in DAYS_DATA:
            print("Sorry, the data is incorrect. Please try again")
            continue
        else:
            break
        
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
    # Load data files into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # Convert the Start Time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Extract months, days and hours from Start Time
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    
    # Filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # Filter by month to create the new dataframe
        df = df[df['month'] == month]

    # Filter by day of week if applicable 
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print('Most common month: ' + MONTH_DATA[most_common_month].title())
    
    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print('Most common day of week:', most_common_day_of_week)

    # display the most common start hour
    most_common_start_hour = df['hour'].mode()[0]
    print('Most common start time:', most_common_start_hour)

    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts()
    print('Most common start station:\n', most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].value_counts()
    print('Most common end station:\n', most_common_end_station)
    

    # display most frequent combination of start station and end station trip
    popular_combination_station = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print('Most frequent combination of start station and end station:\n', popular_combination_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    def convert(seconds):
        return time.strftime("%H:%M:%S", time.gmtime(total_travel_time))
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel display:', convert(total_travel_time))

    # display mean travel time
    def convert(seconds):
        return time.strftime("%H:%M:%S", time.gmtime(mean_travel_time))
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel display:', convert(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_types = df['User Type'].value_counts()
    print('Count of user type:\n',count_user_types)
       
    # Display counts and of gender
    try:
        count_gender_types = df['Gender'].value_counts()
        print('Gender Types:\n', count_gender_types)
    except KeyError:
        print("\n Gender Types:\n No data avaliable in this city")

    # Display earliest, most recent, and most common year of birth
    
    # Earliest year of birth
    try:
        most_earliest_year = df['Birth Year'].min()
        print('Most earliest year:', most_earliest_year)
    except KeyError:
        print("\n Most recent year:\n No data avaliable in this city")
    
    # Latest year of birth
    try:
        most_latest_year = df['Birth Year'].max()
        print('Most latest year:', most_latest_year)
    except KeyError:
        print("\n Most latest year:\n No data avaliable in this city")
         
    # Common year of birth
    try:
        most_common_year = df['Birth Year'].mode()[0]
        print('Most common year:',most_common_year)
    except KeyError:
        print("\n Most common year:\n No data avaliable in this city")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
""" Ask if the user wants to see the next 5 rows of data and more """

def display_data (df):
    raw_data = 0
    while True:
        answer = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n>').lower()
        if answer not in ['yes', 'no']:
            answer = input("Sorry, check your data and try again").lower()
        elif answer == 'yes':
            raw_data += 5
            print(df.iloc[raw_data : raw_data + 5])
            again = input("Do you wish to continue?: yes or no\n>").lower()
            if again == 'no':
                break
            elif answer == 'no':
                return
                

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
