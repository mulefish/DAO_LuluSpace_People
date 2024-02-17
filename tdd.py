import unittest
import pandas as pd
import os
from library import normalize_matrix_round_concat, find_most_common_vectors, CommonThings

class TestGetSessionCount(unittest.TestCase):
    def setUp(self):
        # Sample DataFrame
        self.filtered_df = pd.DataFrame({
            'tlv': [100, 200, 300],
            'sessions': [50, 70, 80],
            'ORIGINAL_TLV': [1000, 2000, 3000],  # Additional columns for testing
            'ORIGINAL_SESSIONS': [500, 700, 800]
        })
        self.group = 'Example Group'
        self.n = 5
        self.precision = 3

    def test_csv_paths_are_ok(self):


        isOk = True         
        isOk &= os.path.exists(CommonThings.CSV_TDD)
        isOk &= os.path.exists(CommonThings.ROLLUP_PII_FREE)
        # This one is OK to not exist at first! It will get created by and by
        isOk = os.path.exists(CommonThings.ROLLUP_VECTORIZED)

        self.assertEqual(isOk, True)

    def test_dataframe_normalization(self):
        given = {
            'sessions': [2, 3, 4],
            'tlv': [80, 70, 60],
            'a': [1000, 2000, 500],
            'b': [100, 200, 50],
            'c': [10, 20, 5]
        }
        df = pd.DataFrame(given)

        PRECISION = 5
        normalized_df = normalize_matrix_round_concat(df, PRECISION)
        list_of_lists = normalized_df.values.tolist()
        # for list in list_of_lists:
        #     print(list)
        expected = [
            [2, 80, '0', '1', '0.33333', '0.33333', '0.33333'],
            [3, 70, '0.5', '0.5', '1', '1', '1'],
            [4, 60, '1', '0', '0', '0', '0']
        ]

        isOk = expected == list_of_lists
        self.assertEqual(isOk, True)


    def test_find_most_common_vectors(self):
        # Call the function
        actual_df = find_most_common_vectors(self.filtered_df, self.group, self.n, self.precision)
        list_of_lists = actual_df.values.tolist()
        expected = [[0, 200.0, 0, 1, 'Example Group', 5, 200.0], [1, 300.0, 0, 1, 'Example Group', 5, 300.0], [2, 100.0, 0, 1, 'Example Group', 5, 100.0]]
        print(list_of_lists)
        isOk = expected == list_of_lists
        self.assertEqual(isOk, True)



if __name__ == '__main__':
    unittest.main()
 