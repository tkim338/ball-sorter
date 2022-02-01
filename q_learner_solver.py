import numpy
import image_processor
from puzzle_model import PuzzleModel
import copy
import sys

def policy_action(model, policy):
    max_reward = None
    best_action = None
    # for action in range(environment.nA):  # [0, 1, 2, 3, 4, 5]
    options = model.get_options()
    for action in options:
        reward = policy[model.state][action]
        if max_reward is None or reward > max_reward:
            max_reward = reward
            best_action = action
    return best_action


def get_action(model, policy, epsilon):
    if model.state not in policy:
        policy[model.state] = dict()
    for action in model.get_options():
        if action not in policy[model.state]:
            policy[model.state][action] = 0

    a = numpy.random.random()
    if a < epsilon:
        actions = model.get_options()
        return actions[numpy.random.randint(len(actions))]
    else:
        return policy_action(model, policy)


if __name__ == "__main__":
    print(sys.argv[1])
    image_loc = sys.argv[1]

    # input params
    gamma = 0.9
    alpha = 0.5
    epsilon = 0.3
    episodes = 3000

    # setup
    # env = gym.make('Taxi-v3').unwrapped
    tube_dict = image_processor.process(image_loc)
    print(tube_dict)
    model = PuzzleModel(tube_dict)
    # pol = numpy.zeros((env.nS, env.nA))
    policy = dict()

    for e in range(episodes):
        if e % 100 == 0:
            print(e)
        # env.reset()
        model = PuzzleModel(tube_dict)
        
        reward = 0
        next_action = get_action(model, policy, epsilon)
        completed = False
        while not completed: # and reward > -20:
            prev_state = copy.deepcopy(model.state)
            prev_action = copy.deepcopy(next_action)
            # None, reward, completed, None = env.step(next_action)  # act(epsilon, env, next_action)
            model.process_move(next_action)
            if model.win_state:
                reward = 1
            elif model.stuck_state:
                reward = -1
            else:
                reward = 0
            completed = model.win_state or model.stuck_state

            if not completed:
                next_action = get_action(model, policy, epsilon)
                fixed_action = get_action(model, policy, 0.0)
                policy[prev_state][prev_action] += alpha*(reward+gamma*policy[model.state][fixed_action] - policy[prev_state][prev_action])

            else:
                policy[prev_state][prev_action] += alpha*(reward - policy[prev_state][prev_action])

    # show optimal policy
    model = PuzzleModel(tube_dict)
    while not model.win_state or not model.stuck_state:
        action = get_action(model, policy, 0.0)
        print(action)
        model.process_move(action)

    print('done')
