from fuzzy_asteroids.fuzzy_asteroids import AsteroidGame, FuzzyAsteroidGame
from fuzzy_asteroids.util import Scenario

from sample_controller import FuzzyController
from sample_score import SampleScore


if __name__ == "__main__":
    # Available settings
    settings = {
        # "graphics_on": True,
        # "sound_on": False,
        "frequency": 60,
        "real_time_multiplier": 2,
        # "lives": 3,
        "prints": True,
        # "allow_key_presses": False
    }

    # Whether the users controller should be run
    run_with_controller = 1

    # Run with FuzzyController
    if run_with_controller:
        # Instantiate the environment
        game = FuzzyAsteroidGame(settings=settings)
        score = game.run(controller=FuzzyController())

    else:
        # Run the Asteroids game with no ai
        asteroid_states = [
            {"speed": 10, "angle": 30, "position": [200, 200]}
        ]
        myScenario = Scenario(asteroid_states=asteroid_states)

        game = AsteroidGame(settings=settings)
        game.run(scenario=myScenario, score=SampleScore())
        #game.run()
