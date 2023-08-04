import numpy as np
import time
from timeit import default_timer as timer

from collections import defaultdict
from box import Box

NUM_CALLS = 10000


def generate_balls(n=10000):
    result = []

    for i in range(n):
        color = np.random.choice(["red", "green", "blue"])
        texture = np.random.choice(["non-smooth", "smooth"])
        result.append({"unique_id": i, "color": color, "texture": texture})

    return result


def show_result(count_dict):
    print("=" * 50)

    for k, v in count_dict.items():
        print(f"{k} encountered in {v / NUM_CALLS:.4f} cases")

    print("=" * 50)


if __name__ == "__main__":
    balls = generate_balls()

    testing_box = Box(balls)

    color_count = defaultdict(int)
    texture_count = defaultdict(int)

    start = timer()

    for _ in range(NUM_CALLS):
        testing_box.get_ball()
        # cur_ball = testing_box.get_ball()
        #
        # color_count[cur_ball["color"]] += 1
        # texture_count[cur_ball["texture"]] += 1

    print(f"Execution took {timer() - start} seconds")

    for _ in range(NUM_CALLS):
        cur_ball = testing_box.get_ball()

        color_count[cur_ball["color"]] += 1
        texture_count[cur_ball["texture"]] += 1

    show_result(color_count)

    show_result(texture_count)


