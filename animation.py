from manim import *
import numpy as np

class MovingGaussian(Scene):
    def construct(self):
        axes = Axes(x_range=[-5, 5, 1], y_range=[0, 1.2, 0.5], x_length=10, y_length=4)
        x0 = ValueTracker(-3)  # center of the Gaussian

        curve = always_redraw(lambda: axes.plot(
            lambda x: np.exp(-(x - x0.get_value())**2 / 0.5),
            color=YELLOW,
        ))

        self.add(axes, curve)
        self.play(x0.animate.set_value(3), run_time=2, rate_func=linear)
        self.wait()