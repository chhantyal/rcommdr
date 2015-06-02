# -*- coding: utf-8 -*-

import sys
import json
import copy
import operator
import argparse

from sklearn.metrics.pairwise import cosine_similarity

from recommdr import __version__

# load json data
with open('data/movies.json') as data_file:
    data = json.load(data_file)


def get_cosine_similarity(movie_list):
    """
    :param movie_list:
    :return: list of tuples made of user_id and cosine_similarity of given movie list.
    """

    cosine_similarity_dict = {}

    for user_preference in data['users']:
        formatted_list1, formatted_list2 = build_lists(movie_list, user_preference['movies'])
        cos_similarity = cosine_similarity(formatted_list1, formatted_list2)
        cosine_similarity_dict[user_preference['user_id']] = cos_similarity

    sorted_cosine_similarity = sorted(cosine_similarity_dict.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_cosine_similarity


def build_lists(lst1, lst2):
    """
    :param lst1:
    :param lst2:
    :return: two lists with same length and order adding 0 to expand shorter list.
    Two collections need to have same length in order to be able to calculate
    cosine similarity.

    eg:
    lst1 = [1, 2]
    lst2 = [1, 4, 6]

    will be transformed to:
    lst1 = [1, 2, 0, 0]
    lst2 = [1, 0, 4, 6]
    """
    lst = copy.deepcopy(lst1)
    lst.extend(lst2)
    lst = list(set(lst))
    lst.sort()

    # first define list with 0 values
    lst3 = [0] * len(lst)
    lst4 = [0] * len(lst)

    for index, item in enumerate(lst):
        if item in lst1:
            lst3[index] = item

        if item in lst2:
            lst4[index] = item

    return lst3, lst4


def get_movie_from_id(id):
    """
    :param id:
    :return: Movie name from given id
    """
    return data['movies'][id]


def get_similar_users(movie_list, number=3):
    """
    :param movie_list:
    :return: list of users who have similar movie preference
    """
    # get top three tuples of cosine similarity
    highest_cos_similarity = get_cosine_similarity(movie_list)[:number]
    # get users from tuples.
    similar_users = dict(highest_cos_similarity).keys()
    return similar_users


def recommend(movie_list, number=None):
    """
    :param movie_list:
    :return: List of recommended movies
    """
    similar_users = get_similar_users(movie_list)
    movies = []
    for user in similar_users:
        index = user - 1
        movies.extend(data['users'][index]['movies'])
    # remove movies taken as input
    [movies.remove(x) for x in movie_list if x in movies]
    # remove duplicates
    movies = list(set(movies))
    movies = [get_movie_from_id(str(x)) for x in movies]
    if number and len(movies) > number:
        movies = movies[:number]
    return movies


def cli_options(args):
    description = 'Find movies based on your past preference.'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--version', action='version', version=__version__,
                        help='show current version of this tool.')
    parser.add_argument('--movies', type=list,
                        help="list of movies you like eg. [1, 7, 20].")
    parser.add_argument('--number', type=int,
                        help="optional: number of movies to be recommended.")
    return parser.parse_args()


def main(argv=sys.argv):
    """
    Args:
        argv (list): List of arguments
    """
    args = cli_options(argv)
    print args
    if not args.movies:
        print "Please use -h or --help option to learn how to use recommdr."
        sys.exit()
    return recommend(args.movies, number=args.number)

if __name__ == "__main__":
    main()

