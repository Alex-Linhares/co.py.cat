import unittest
from pprint import pprint

from copycat import Copycat

# TODO: update test cases to use entropy

# CHI2 values for n degrees freedom
_chiSquared_table = {
        1:3.841,
        2:5.991,
        3:7.815,
        4:9.488,
        5:11.071,
        6:12.592,
        7:14.067,
        8:15.507,
        9:16.919,
        10:18.307
        }

class TestCopycat(unittest.TestCase):

    def setUp(self):
        self.longMessage = True  # new in Python 2.7

    def assertProbabilitiesLookRoughlyLike(self, actual, expected, iterations):

        answerKeys = set(list(actual.keys()) + list(expected.keys()))
        degreesFreedom = len(answerKeys)
        chiSquared = 0

        get_count = lambda k, d : d[k]['count'] if k in d else 0

        for k in answerKeys:
            E = get_count(k, expected)
            O = get_count(k, actual)
            if E == 0:
                print('Warning! Expected 0 counts of {}, but got {}'.format(k, O))
            else:
                chiSquared += (O - E) ** 2 / E

        if chiSquared >= _chiSquared_table[degreesFreedom]:
            self.fail('Significant different between expected and actual answer distributions: \n' +
                'Chi2 value: {} with {} degrees of freedom'.format(chiSquared, degreesFreedom))

    def run_testcase(self, initial, modified, target, iterations, expected):
        print('expected:')
        pprint(expected)
        actual = Copycat().run(initial, modified, target, iterations)
        print('actual:')
        pprint(actual)
        self.assertEqual(sum(a['count'] for a in list(actual.values())), iterations)
        self.assertProbabilitiesLookRoughlyLike(actual, expected, iterations)

    def test_simple_cases(self):
        self.run_testcase('abc', 'abd', 'efg', 30, 
	    {'dfg': {'avgtemp': 72.37092377767368, 'avgtime': 475.0, 'count': 1},
	     'efd': {'avgtemp': 49.421147725239024, 'avgtime': 410.5, 'count': 2},
	     'efh': {'avgtemp': 19.381658717913258,
		     'avgtime': 757.1851851851852,
		     'count': 27}})
        self.run_testcase('abc', 'abd', 'ijk', 30, 
            {'ijd': {'avgtemp': 14.691978036611559, 'avgtime': 453.0, 'count': 1},
             'ijl': {'avgtemp': 22.344023091153964,
                              'avgtime': 742.1428571428571,
                                       'count': 28},
             'jjk': {'avgtemp': 11.233344554288019, 'avgtime': 595.0, 'count': 1}})


    def test_abc_xyz(self):
        self.run_testcase('abc', 'abd', 'xyz', 100, 
	    {'dyz': {'avgtemp': 26.143509984937367, 'avgtime': 9866.625, 'count': 8},
	     'wyz': {'avgtemp': 12.249539212574128,
		     'avgtime': 9520.666666666666,
		     'count': 18},
	     'xyd': {'avgtemp': 38.73402068486291, 'avgtime': 7439.225, 'count': 40},
	     'xyy': {'avgtemp': 24.614440709519627, 'avgtime': 3522.625, 'count': 8},
	     'xyz': {'avgtemp': 57.674822842028945, 'avgtime': 8315.2, 'count': 5},
	     'yyz': {'avgtemp': 26.874886217740315,
		     'avgtime': 8493.142857142857,
		     'count': 21}})

    def test_ambiguous_case(self):
        self.run_testcase('abc', 'abd', 'ijkk', 100, 
	    {'ijd': {'avgtemp': 55.6767488926397, 'avgtime': 948.0, 'count': 1},
	     'ijkd': {'avgtemp': 78.09357723857647, 'avgtime': 424.5, 'count': 2},
	     'ijkk': {'avgtemp': 68.54252699118226, 'avgtime': 905.5, 'count': 2},
	     'ijkkk': {'avgtemp': 21.75444235750483,
		       'avgtime': 2250.3333333333335,
		       'count': 3},
	     'ijkl': {'avgtemp': 38.079858245918466,
		      'avgtime': 1410.2391304347825,
		      'count': 46},
	     'ijll': {'avgtemp': 27.53845719945872,
		      'avgtime': 1711.8863636363637,
		      'count': 44},
	     'jjkk': {'avgtemp': 75.76606718990365, 'avgtime': 925.0, 'count': 2}})

    def test_mrrjjj(self):
        self.run_testcase('abc', 'abd', 'mrrjjj', 30, 
	    {'drrjjj': {'avgtemp': 47.3961, 'avgtime': 1538.0, 'count': 1},
	     'mrrjjd': {'avgtemp': 70.5363, 'avgtime': 681.0, 'count': 1},
	     'mrrjjjj': {'avgtemp': 19.1294, 'avgtime': 2075.0, 'count': 1},
	     'mrrjjk': {'avgtemp': 48.0952,
			'avgtime': 2203.5714,
			'count': 14},
	     'mrrkkk': {'avgtemp': 43.6931,
			'avgtime': 2251.4615,
			'count': 13}})

    '''
    Below are examples of improvements that could be made to copycat.

    def test_elongation(self):
        # This isn't remotely what a human would say.
        self.run_testcase('abc', 'aabbcc', 'milk', 30, 
	    {'lilk': {'avgtemp': 68.18128407669258,
		      'avgtime': 1200.6666666666667,
		      'count': 3},
	     'mikj': {'avgtemp': 57.96973195905564,
		      'avgtime': 1236.888888888889,
		      'count': 9},
	     'milb': {'avgtemp': 79.98413990245763, 'avgtime': 255.0, 'count': 1},
	     'milj': {'avgtemp': 64.95289549955349, 'avgtime': 1192.4, 'count': 15},
	     'milk': {'avgtemp': 66.11387816293755, 'avgtime': 1891.5, 'count': 2}})
    def test_repairing_successor_sequence(self):
        # This isn't remotely what a human would say.
        self.run_testcase('aba', 'abc', 'xyx', 30, 
	    {'cyx': {'avgtemp': 82.10555880340601, 'avgtime': 2637.0, 'count': 2},
	     'xc': {'avgtemp': 73.98845045179358, 'avgtime': 5459.5, 'count': 2},
	     'xyc': {'avgtemp': 77.1384941639991,
		     'avgtime': 4617.434782608696,
		     'count': 23},
	     'xyx': {'avgtemp': 74.39287653046891, 'avgtime': 3420.0, 'count': 3}})
    def test_nonsense(self):
        self.run_testcase('cat', 'dog', 'cake', 10, {
            'cakg': {'count': 99, 'avgtemp': 70},
            'gake': {'count': 1, 'avgtemp': 59},
        })
        self.run_testcase('cat', 'dog', 'kitten', 10, {
            'kitteg': {'count': 96, 'avgtemp': 66},
            'kitten': {'count': 4, 'avgtemp': 68},
        })
    '''


if __name__ == '__main__':
    unittest.main()
