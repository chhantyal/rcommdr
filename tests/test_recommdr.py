import json
import unittest

from recommdr.app import (build_lists, get_cosine_similarity,
                          get_movie_from_id, get_similar_users,
                          recommend)


with open('tests/movies.json') as data_file:
    data = json.load(data_file)


class MainTestCase(unittest.TestCase):

    def test_build_lists(self):
        """
        Does it return two lists with same length and without
        changing order of items?

        Eg. with inputs,
         lst1 = [1, 2, 6]
         lst2 = [3, 4]
        it should return:
         lst3 = [1, 2, 0, 0, 6]
         lst4 = [0, 0, 3, 4, 0]
        """
        lst1 = [1, 2, 6]
        lst2 = [3, 4]

        expected_lst1 = [1, 2, 0, 0, 6]
        expected_lst2 = [0, 0, 3, 4, 0]

        returned_lst1, returned_lst2 = build_lists(lst1, lst2)

        self.assertEqual(expected_lst1, returned_lst1)
        self.assertEqual(expected_lst2, returned_lst2)

    def test_get_cosine_similarity(self):
        """
        Should return list of tuples with users and highest cosine similarity,
        ordered by higher cosine similarity.
        """
        movie_list = [2, 6, 28]

        result = get_cosine_similarity(movie_list, data)
        self.assertTrue(type(result[0]), tuple)
        # cosine similarity of first item should be
        # greater than or equal to second and so on.
        self.assertTrue(result[0][1] >= result[1][1] >= result[2][1])
        # value of cosine similarity should be between 1 and -1
        cosine_similarity_list = dict(result).values()
        # sort from higher to lower
        cosine_similarity_list.sort(reverse=True)
        self.assertTrue(cosine_similarity_list[0] <= 1)
        self.assertTrue(cosine_similarity_list.pop() >= -1)

    def test_get_movie_from_id(self):
        """
        Should return movie name from id
        """
        # ID 23 is Pulp Fiction (1994) on movies.json file
        movie_name = 'Pulp Fiction (1994)'
        returned_movie_name = get_movie_from_id(str(23), data)
        self.assertEqual(movie_name, returned_movie_name)

    def test_get_similar_users(self):
        """
        Should return list of users who have similar
        preference as given movie list
        """
        movie_list = [2, 6, 28]
        users = get_similar_users(movie_list, data)

        # users should be from given data
        for user in users:
            self.assertTrue(user in xrange(1, 807))
        # should return stated number of users
        users = get_similar_users(movie_list, data, number=4)
        self.assertEqual(len(users), 4)

    def test_recommend(self):
        """
        Should return list of recommended movie names
        """
        movie_list = [2, 6, 28]

        recommended_list = recommend(movie_list, data)

        all_movie_names = data['movies'].values()

        for item in recommended_list:
            self.assertTrue(item in all_movie_names)
        # should return stated number of movies
        recommended_list = recommend(movie_list, data, number=3)
        self.assertEqual(len(recommended_list), 3)

if __name__ == '__main__':
    unittest.main()