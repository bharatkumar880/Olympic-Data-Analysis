import numpy as np
import pandas as pd

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal']).copy()
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    elif year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    else:
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year', as_index=False).sum(numeric_only=True)[['Year', 'Gold', 'Silver', 'Bronze']]
    else:
        x = temp_df.groupby('region', as_index=False).sum(numeric_only=True)[['region', 'Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False)

    x['total'] = x[['Gold', 'Silver', 'Bronze']].sum(axis=1)

    return x.astype({'Gold': 'int', 'Silver': 'int', 'Bronze': 'int', 'total': 'int'})


def country_year_list(df):
    years = sorted(df['Year'].unique().tolist())
    years.insert(0, 'Overall')

    country = sorted(df['region'].dropna().unique().tolist())
    country.insert(0, 'Overall')

    return years, country


def data_over_time(df, col):
    nations_over_time = df.drop_duplicates(['Year', col]).groupby('Year', as_index=False).size()
    nations_over_time.columns = ['Edition', 'Count']
    return nations_over_time.sort_values('Edition')


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal']).copy()

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    top_athletes = temp_df['Name'].value_counts().reset_index()
    top_athletes.columns = ['Athlete', 'Medals']

    x = top_athletes.head(15).merge(df, left_on='Athlete', right_on='Name', how='left')[['Athlete', 'Medals', 'Sport', 'region']].drop_duplicates('Athlete')
    return x


def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal']).drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal']).copy()
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year', as_index=False).count()[['Year', 'Medal']]
    return final_df


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal']).drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal']).copy()
    new_df = temp_df[temp_df['region'] == country]
    return new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal']).copy()
    temp_df = temp_df[temp_df['region'] == country]

    top_athletes = temp_df['Name'].value_counts().reset_index()
    top_athletes.columns = ['Athlete', 'Medals']

    x = top_athletes.head(10).merge(df, left_on='Athlete', right_on='Name', how='left')[['Athlete', 'Medals', 'Sport']].drop_duplicates('Athlete')
    return x


def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region']).copy()
    athlete_df['Medal'].fillna('No Medal', inplace=True)

    if sport != 'Overall':
        return athlete_df[athlete_df['Sport'] == sport]
    return athlete_df


def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region']).copy()

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year', as_index=False).count()[['Year', 'Name']]
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year', as_index=False).count()[['Year', 'Name']]

    final = men.merge(women, on='Year', how='left').fillna(0)
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    return final
