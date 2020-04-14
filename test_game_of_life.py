import unittest
import numpy as np
from game_of_life import Life

class TestGameOfLife(unittest.TestCase):

    def test_boundary_additions(self):
        L = Life(3, 0.8)
        L.state = np.array([[1, 1, 0], [0, 1, 1], [0, 0, 1]])
        expected_state = np.array([[1, 0, 0, 1, 0], [0, 1, 1, 0, 1],
                                   [1, 0, 1, 1, 0], [1, 0, 0, 1, 0],
                                   [0, 1, 1, 0, 1]])
        L.add_boundary()
        self.assertEqual(L.state.shape, expected_state.shape)
        self.assertTrue((L.state == expected_state).all())
