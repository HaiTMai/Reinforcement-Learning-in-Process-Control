from models.tank_model.tank import Tank
from visualize.window import Window
import matplotlib.pyplot as plt
from drawnow import drawnow


class Environment:
    "Parameters are set in the params.py file"

    def __init__(self, TANK_PARAMS, TANK_DIST, MAIN_PARAMS):

        self.model = Tank(
            height=TANK_PARAMS["height"],
            radius=TANK_PARAMS["width"],
            max_level=TANK_PARAMS["max_level"],
            min_level=TANK_PARAMS["min_level"],
            pipe_radius=TANK_PARAMS["pipe_radius"],
            init_level=TANK_PARAMS["init_level"],
            dist=TANK_DIST,
        )

        self.running = True
        self.episode = 0
        self.all_rewards = []
        self.terminated = False

        self.show_rendering = MAIN_PARAMS["RENDER"]
        self.live_plot = MAIN_PARAMS["LIVE_REWARD_PLOT"]

        if self.show_rendering:
            self.window = Window(self.model)
        if self.live_plot:
            plt.ion()  # enable interactivity
            plt.figure(num="Rewards per episode")  # make a figure

    def get_next_state(self, z, t):
        """
        Calculates the dynamics of the agents action and
        gives back the next state
        """

        dldt = self.model.get_dhdt(z, t)
        self.model.change_level(dldt)
        # Check terminate state
        if self.model.level < self.model.min:
            self.terminated = True
            self.model.level = self.model.min
        elif self.model.level > self.model.max:
            self.terminated = True
            self.model.level = self.model.max
        return self.model.level

    def render(self, action):
        "Draw the water level of the tank in pygame"

        if self.render:
            running = self.window.Draw(action)
            if not running:
                self.running = False

    def plot_rewards(self):
        "drawnow plot of the reward"

        plt.plot(
            self.all_rewards,
            label="Exploration rate: {} %".format(self.epsilon * 100),
        )
        plt.legend()

    def plot(self, all_rewards, epsilon):
        "Live plot of the reward"
        self.all_rewards = all_rewards
        self.epsilon = round(epsilon, 4)
        try:
            drawnow(self.plot_rewards)
        except KeyboardInterrupt:
            print("Break")
