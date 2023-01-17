import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Enter The City Name: (chicago, new york city, or washington): ').lower()
        if city not in CITY_DATA.keys():
            print('Please, Enter the city correctly!')
        else:
            break

    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    
    while True:
        month = input('Choose Month: (january, february, march, april, may, june, Or all): ').lower()
        if month in months:
            break
        else:
            print('Please, Enter a valid month!')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['sunday', 'monday', 'tuesday', 'wednesday', ', thursday', 'friday', 'saturday', 'all']
    
    while True:
        day = input('Choose The Day: ').lower()
        if day in days:
            break
        else:
            print('Please, Enter a valid day!')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    """
    # reading the data from files csv
    df = pd.read_csv(CITY_DATA[city])

    # convert the column to date time for extracting months and days easily
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # make new columns for extracting specific data
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # make condition for matching month
    if month != 'all':
        months = months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1   # to make it appear in Number
        df = df[df['month'] == month]
        
    # filter by day to create a new df, using the title for making the first letter is capital
    if day != 'all':
        df = df[df['day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print(f'The most common Month is: {df.month.mode()[0]}')

    # display the most common day of week
    print(f'The most common Day is: {df.day.mode()[0]}')

    # display the most common start hour
    print(f'The most common Hour is: {df.hour.mode()[0]}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most common start station is: {}'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('The most common end station is: {}'.format(df['End Station'].mode()[0]))

    # Two ways for display most frequent combination of start station and end station trip 
    df['st&en combination'] = df['Start Station']+ ',' + df['End Station']
    print('The most common combination is: {}'.format(df['st&en combination'].mode()[0]))

    print('-'*20)

    comm_station = df.groupby(['Start Station','End Station']).size().sort_values(ascending=False)
    print(comm_station.head(1).to_frame())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Travel Time is: ', df['Trip Duration'].sum().round())

    # display mean travel time
    print('Average Travel Time is: ', df['Trip Duration'].mean().round())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of User: ', df['User Type'].value_counts().to_frame())

    # Display counts of gender
    if city != 'washington':
        print(f'\nCounts of Gender: {df.Gender.value_counts().to_frame()}\n')
        
        # Display earliest, most recent, and most common year of birth
        print(f"The Earliest Year of Birth is: {int(df['Birth Year'].min())}")
        print(f"The Most Recent Year of Birth is: {int(df['Birth Year'].max())}")
        print(f"The Common Year of Birth is: {int(df['Birth Year'].mode()[0])}")
    else:
        print('No (gender or birth year) for This City, Enter the Correct City.')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('Thanks!')
            break


if __name__ == "__main__":
	main()
