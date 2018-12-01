import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#lists to index the filters and check if the input is valid
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['monday', 'tuesday', 'wendsday', 'thrusday', 'friday', 'saturday', 'sunday']
cities = ['chicago', 'new york city', 'washington']
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        city = input('Are you from Washington, New York City or Chicago: ').lower()
        if city in cities:
            break
    print('You selected: ', city)
#fixed the missing loop and case sensitivity in 'month' and 'day' input
    while True:
        month = input('Which month would you like to filter, choose "all" if you do not want to filter: ').lower()
        if month in months:
            break
    print('You selected')

    while True:
        day = input('Which day would you like to filter, choose "all" if you do not want to filter: ').lower()
        if day in ['monday', 'tuesday', 'wendsday', 'thrusday', 'friday', 'saturday', 'sunday', 'all']:
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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
#changed 'weekday_name' to just 'weekday' which outputs the weekday as integer
    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['dow'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

# problem with the 'day'-filter,  if a day (not 'all') is applied, the output is not right
    # filter by day of week if applicable
    if day != 'all':

        # filter by day of week to create the new dataframe
        day = days.index(day) + 1
        df = df[df['dow'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    most_common_month = df.loc[:,'month'].mode()
    print('The most common month is: ', most_common_month)

    most_common_dow = df.loc[:,'dow'].mode()
    print('The most common day of the week is: ', most_common_dow)

    most_common_hour = df.loc[:,'hour'].mode()
    print('The most commen hour is: ', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    most_started = df.loc[:,'Start Station'].mode()
    print('The most started location is: ', most_started)

    most_ended = df.loc[:,'End Station'].mode()
    print('The most common used end station is: ',most_ended)

    frequent_combination = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('The most frequent used combination of start and end station is: ',frequent_combination)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    travel_time_total = df['Trip Duration'].sum()
    print('The total travel time is: ',travel_time_total)

    travel_time_mean = df['Trip Duration'].mean()
    print('The average time travelled is: ',travel_time_mean)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    count_user_type = df.groupby('User Type').count()
    print('The distribution of user types is: ',count_user_type)
#used the suggested try except method, because i had difficutlties with an if clause an the variable scope of the 'city' variable - same with the 'birth year'
    try:
        count_gender = df.groupby('Gender').count()
        print('The distribution of genders is: ',count_gender)
    except:
        print('\n No gender-data available in Washington.')

    try:
        earliest_yob = df['Birth Year'].min()
        print('\n The earliest year of bearth is: ', earliest_yob)
        latest_yob = df['Birth Year'].max()
        print('\n The most recent year of birth is: ', latest_yob)
        most_common_yob = df.loc[:,'Birth Year'].mode()
        print('The most common year of birth is: ', most_common_yob)
    except:
        print('\n No birt-year-data available in Washington.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    rows_viewed = 5
    statement = input('Do you want to see raw data? Enter yes or no. ')
    while True:
        if statement.lower() == 'yes':
            print(df.iloc[:(rows_viewed)])
            rows_viewed += 5
            statement = input('Do you want to see more ? Enter yes or no. ')
        else:
            break


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
