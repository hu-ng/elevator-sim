## Elevator simulation in Python

This project codify fundamental aspects of how an elevator works using Python objects. Three strategies are implemented and tested for efficency.

- Strategy 1: Prioritize people in the elevator first, while picking up people on the way if there is space.
- Strategy 2: Simply going up and down the building until there are no passengers left to transport.
- [Strategy 3](https://www.popularmechanics.com/technology/infrastructure/a20986/the-hidden-science-of-elevators/): As long as there’s someone inside or ahead of the elevator who wants to go in the current direction, keep heading in that direction. Once the elevator has exhausted the requests in its current direction, switch directions if there’s a request in the other direction. Otherwise, stop and wait for a call.

Efficiency is measured with two metrics: total distance traveled and average passenger waiting time. We'll see that there is trade-off between these two metrics. In terms of total distance traveled, Strategy 1 is the worst as expected, while Strategy 2 and 3 have similar performance.

| With increasing # of passengers | With increasing # of floors |
| --- | --- |
| ![increasing passengers](https://github.com/hu-ng/elevator-sim/blob/master/images/average_steps_people.png)  | ![increasing floors](https://github.com/hu-ng/elevator-sim/blob/master/images/average_steps_floors.png)  |

In terms of average waiting time, Strategy 1 is the best, which is expected because passengers are prioritized at the cost of distance traveled. On the other hand, Strategy 2 and 3 are worst with this metric for the exact opposite reason, they trade waiting time for distance traveled.

| With increasing # of passengers | With increasing # of floors |
| --- | --- |
| ![increasing passengers](https://github.com/hu-ng/elevator-sim/blob/master/images/average_wait_time_people.png)  | ![increasing floors](https://github.com/hu-ng/elevator-sim/blob/master/images/average_wait_time_floors.png)  |
