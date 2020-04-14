
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation

np.random.seed(42)
class Board(object):
    def __init__(self, size: int, prob: float):
        self.size = size
        self.prob = prob
        self.set_state(self.size, self.prob)

    def set_state(self, size: int, prob: float):
        self.state = np.random.choice(2, (size, size),
                                      True, [1 - prob, prob])
                                      
    def change_state(self, prob: float):
        self.set_state(self.size, prob)
                                    
    def pretty_print(self, state):
        print("-" * self.size * 4)
        for row in range(len(state)):
            temp = []
            for col in range(len(state[row])):
                if state[row][col] == 1:
                    temp.append(" # ")
                else:
                    temp.append("   ")
            print(f"   | {''.join(temp)} |   ")
        print("-" * self.size * 4)

class Life(Board):
    def __init__(self, size: int, prob: float):
        super().__init__(size, prob)
        self.window = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])

    def add_boundary(self):
        self.empty_state = np.zeros((self.size+2, self.size+2))

        # adding last element to first element
        self.empty_state[0, 0] = self.state[-1, -1]
        # adding first element to last element
        self.empty_state[-1, -1] = self.state[0, 0]
        # adding first element of last row to last element of first row
        self.empty_state[0, -1] = self.state[-1, 0]
        # adding last element of first row to first element of last row
        self.empty_state[-1, 0] = self.state[0, -1]
        # adding last row to first row
        self.empty_state[0, 1:-1] = self.state[-1,:]
        # adding first row to last row
        self.empty_state[-1, 1:-1] = self.state[0,:]
        # adding first column to last column
        self.empty_state[1:-1, -1] = self.state[:, 0]
        # adding last column to first column
        self.empty_state[1:-1, 0] = self.state[:, -1]
        # adding matrix to remaining places
        self.empty_state[1:-1, 1:-1] = self.state
        
        self.state = self.empty_state


    def change_state(self, total: int):
        if total == 0 or total == 1:
            return 0
        elif total == 2 or total == 3:
            return 1
        elif total > 3:
            return 0
        elif total == 3:
            return 1
        else:
            raise ValueError(f"Total of {total} not expected.")

    def update_board_state(self):
        self.new_state = np.zeros((self.size, self.size))
        height, width = self.state.shape
        for rowIDX in range(1, height - 1):
            for colIDX in range(1, width - 1):
                self.new_state[rowIDX - 1, colIDX - 1] = self.change_state(
                                                         np.sum(self.state[rowIDX - 1:rowIDX + 2,
                                                         colIDX - 1: colIDX + 2]*self.window))
        self.state = self.new_state.copy()
        self.add_boundary()          
        return self.new_state

    def save_series(self, iterations: int):
        self.series = []
        self.add_boundary()
        self.series.append(self.state[1:-1, 1:-1])
        for i in range(iterations):
            self.update_board_state()
            self.series.append(self.state[1:-1, 1:-1])
        


L = Life(30, 0.1)
# toad
# L.state = np.array([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 0], [0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
# # diagonal
# L.state = np.array([[1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1]])
# i
# L.state = np.array([[0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0]])

L.save_series(100)
# print(L.state.shape)
# L.add_boundary()
# print(L.state)
# print(L.state[1:-1, 1:-1])
# im = plt.imshow(L.series[0], interpolation='none', aspect='auto', vmin=0, vmax=1)
# fps = 30
# nSeconds = 5
# fig = plt.figure(figsize=(8,8))
fig = plt.figure()
images = []
for image in L.series:
    im=plt.imshow(image, animated=True)
    images.append([im])

ani = animation.ArtistAnimation(fig, images, interval=500, blit=True,
                                repeat_delay=1000)
plt.show()