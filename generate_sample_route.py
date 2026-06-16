import cv2
import numpy as np
import project
import functions

START = (262, 99)
GOAL = (178, 158)
OUTPUT = "sample_astar_route.png"

ZC_MAP = np.ndarray.tolist(project.new)
problem = project.Map(ZC_MAP, START, GOAL)
actions, cost = functions.A_star(problem)

states = [START]
state = START
for action in actions:
    state = problem.result(state, action)
    states.append(state)

image = cv2.imread("image.png", cv2.IMREAD_COLOR)
for index in range(len(states) - 1):
    first_point = (states[index][1] * 2, states[index][0] * 2)
    second_point = (states[index + 1][1] * 2, states[index + 1][0] * 2)
    cv2.line(image, first_point, second_point, (255, 0, 0), 4)

cv2.circle(image, (START[1] * 2, START[0] * 2), 9, (0, 255, 0), -1)
cv2.circle(image, (GOAL[1] * 2, GOAL[0] * 2), 9, (0, 0, 255), -1)
cv2.imwrite(OUTPUT, image)

print(f"A* actions: {actions}")
print(f"A* path cost: {cost}")
print(f"Route image saved to {OUTPUT}")
