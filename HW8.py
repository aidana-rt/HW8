# Your name: Aidana Tuyakbayeva
# Your student id: 19994247
# Your email: aidana@umich.edu
# List who you have worked with on this homework:

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database,
    and each inner key is a dictionary, where the key:value pairs should be the category,
    building, and rating for the restaurant.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    rest_dict = {}
    cur.execute("SELECT name, category, building, rating FROM restaurants JOIN categories ON category_id = categories.id JOIN buildings ON building_id = buildings.id")
    for row in cur:
        inner_dict = {}
        rest_name = row[0]
        rest_cat = row[1]
        rest_build = row[2]
        rest_rating = row[3]
        inner_dict['category'] = rest_cat
        inner_dict['building'] = rest_build
        inner_dict['rating'] = rest_rating
        rest_dict[rest_name] = inner_dict
    return rest_dict

def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    cat_dict = {}
    cur.execute("SELECT category, COUNT(name) FROM restaurants JOIN categories ON category_id = categories.id GROUP BY category ORDER BY COUNT(name) ASC")
    for row in cur:
        cat_dict[row[0]] = row[1]
    plt.figure(figsize=(8,8))
    plt.barh(list(cat_dict.keys()), list(cat_dict.values()))
    plt.xlabel("Number of Restaurants")
    plt.ylabel("Restaurant Categories")
    plt.title('Types of Restaurants on South U Ave')
    plt.tight_layout()
    plt.savefig("Task2.png")
    plt.show()
    return cat_dict

def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants
    should be sorted by their rating from highest to lowest.
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    rest_list = []
    cur.execute("SELECT name, building, rating FROM restaurants JOIN buildings ON building_id = buildings.id WHERE (building = ?) ORDER BY rating DESC", (building_num, ))
    for row in cur:
        rest_list.append(row[0])
    return rest_list

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    pass

#Try calling your functions here
def main():
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
