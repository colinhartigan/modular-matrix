import random

class Cloud:
    def __init__(self, width, height):
        self.shape = []
        for i in range(height):
            if i == height - 1:
                self.shape.append([1 if i != 0 and i != width - 1 else 0  for i in range(width)])
            elif i == height - 2:
                self.shape.append([1 for i in range(width)])
            else:
                self.shape.append([0 for i in range(width)])


        for i in range(len(self.shape)-2, -1, -1): # go from bottom to top
            for j in range(len(self.shape[i])):
                if self.shape[i + 1][j] == 1:
                    r = random.randint(0, 3*(i+1))
                    if r in range(1,(3*(i+1))+1):
                        if i + 1 < width and j - 1 > 0 and j + 1 < width:
                            if self.shape[i+1][j-1] == 1 and self.shape[i+1][j] == 1 and self.shape[i+1][j+1] == 1:
                                self.shape[i][j] = 1

        print("\n".join(" ".join(str(j) for j in i) for i in self.shape))

c = Cloud(16,5)