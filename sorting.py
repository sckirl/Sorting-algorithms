import pygame
import random
import sys
import time
import winsound

pygame.init()

win = pygame.display.set_mode((504, 400))
pygame.display.set_caption("Sorting Algorithm Visualization")

clock = pygame.time.Clock()

class Algorithm(object):
    def __init__(self):
        self.value = self.li = self.res = []
        self.not_sorted = True
        self.count = 0

    def getValue(self, length=40, minimum=200, steps=2):
        for i in random.sample(range(minimum, (minimum+(length * steps)), steps), length):
            self.value.append(i)

    def bubbleSort(self):
        if len(self.value) > 1:
            pygame.display.set_caption("Bubble Sort Algorithm")
            for i in range(1, len(self.value)):
                # self.update(i, 0)
                for j in range((len(self.value)-i)):
                    self.update(j, j+1)
                    if self.value[j] > self.value[j + 1]:
                        self.value[j], self.value[j + 1] = self.value[j + 1], self.value[j]
                        self.update(j, j+1)
            self.sorted()

    def quickSort(self, li, lo, hi):
        if lo < hi and len(self.value) > 1:
            val = self.partition(li, lo, hi)
            if self.value == self.res:
                self.sorted()
                return None
            self.quickSort(li, lo, val-1)
            self.quickSort(li, val+1, hi)

    def partition(self, li, left, right):
        pygame.display.set_caption("Quicksort Algorithm")
        pivot = li[right]
        i = left - 1
        for j in range(left, right):
            self.update(j, i, right)
            if li[j] <= pivot:
                i += 1
                li[j], li[i] = li[i], li[j]
        li[i+1], li[right] = li[right], li[i+1]
        return (i+1)

    def sorted(self):
        self.not_sorted = False
        for i in range(len(self.value)):
            self.update(i, i)

    def update(self, pointer, swap, pivot=None):
        self.draw()

        pygame.draw.rect(win, [66, 127, 140], (pointer * 12, 0, 10, self.value[pointer]))
        winsound.Beep(self.value[pointer] * 5, 60)
        pygame.draw.rect(win, [45, 95, 115], (swap * 12, 0, 10, self.value[swap]))
        
        if pivot is not None:
            pygame.draw.rect(win, [38, 38, 38], (pivot * 12, 0, 10, self.value[pivot]))

        pygame.display.update()
        win.fill((242, 224, 189))

    def restart(self):
        self.count = 0
        self.value = []
        self.pointer = self.swap = None

    def draw(self):
        x, y = 0, 0
        for height in self.value:
            pygame.draw.rect(win, [191, 169, 142], (x, y, 10, height))
            x += 12

sort = Algorithm()

while True:
    clock.tick(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                sort.restart()
                sort.getValue(length=42, minimum=10, steps=7)
                sort.res = sorted(sort.value)
                sort.not_sorted = True
            if event.key == pygame.K_1 and sort.not_sorted:
                sort.bubbleSort()
            if event.key == pygame.K_2 and sort.not_sorted:
                sort.quickSort(sort.value, 0, len(sort.value)-1)

    # redraw stuff
    win.fill((242, 224, 189))
    sort.draw()
    pygame.display.update()