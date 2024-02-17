import unittest
import pandas as pd
import os
from library import normalize_matrix_round_concat, CommonThings

class TestGetSessionCount(unittest.TestCase):

    def test_csv_paths_are_ok(self):
        isOk = True         
        isOk &= os.path.exists(CommonThings.CSV_TDD)
        isOk &= os.path.exists(CommonThings.ROLLUP_PII_FREE)
        # This one is OK to not exist at first! It will get created by and by
        isOk = os.path.exists(CommonThings.ROLLUP_VECTORIZED)

        self.assertEqual(isOk, True)

      

    # def test_shape_munging(self):
    #     # df = pd.read_csv("tdd_data.csv")
    #     data = {
    #         "sessions": [11, 10],
    #         "tlv": [10, 777],
    #         "a": [133.000, 888.000],
    #         "b": [122.000, 999.000],
    #     }
    #     df = pd.DataFrame(data)
        
    #     df = normalize_matrix(df)
    #     list_of_lists = df.values.tolist()

    #     # [[11.0, 10.0, 11.0, 0.0, 0.0, 0.0], [10.0, 777.0, 10.0, 0.9999999999999999, 1.0, 1.0]]
    #     # print(list_of_lists)
    #     # print('\n')
    #     # for list in list_of_lists:
    #     #     print(list)

    #     isOk = True 
    #     isOk &= list_of_lists[0][0] == 11 
    #     isOk &= list_of_lists[1][0] == 10
    #     isOk &= list_of_lists[0][1] == 10
    #     isOk &= list_of_lists[1][1] == 777

    #     self.assertEqual(isOk, True)

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
if __name__ == '__main__':
    unittest.main()
 