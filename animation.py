from manim import *
import numpy as np


class WavePacket3D(ThreeDScene):
    def construct(self):
        # --- parameters -------------------------------------------------
        k0 = 4.0        # central wave number (sets the ripple wavelength)
        sigma0 = 1.0    # initial width of the packet
        v_g = 1.0       # group velocity (envelope speed)
        v_p = 0.5       # phase velocity (free particle: v_p = v_g / 2)
        spread = 0.25   # how fast the packet disperses
        x0 = -3.0       # starting position
        T = 6.0         # total simulated time

        # --- axes (no LaTeX: no number labels, Text instead of MathTex) -
        axes = ThreeDAxes(
            x_range=[-6, 6, 2],
            y_range=[-3, 3, 1],
            z_range=[-1.2, 1.2, 0.5],
            x_length=10,
            y_length=5,
            z_length=3,
        )
        self.set_camera_orientation(phi=65 * DEGREES, theta=-55 * DEGREES, zoom=0.9)

        title = Text("Gaussian wave packet", font_size=32).to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)

        t = ValueTracker(0)

        def psi(x, y, time):
            s2 = sigma0**2 + (spread * time) ** 2          # width grows over time
            envelope = (sigma0**2 / s2) * np.exp(
                -((x - x0 - v_g * time) ** 2 + y**2) / (2 * s2)
            )
            return envelope * np.cos(k0 * (x - x0 - v_p * time))

        def make_surface():
            time = t.get_value()
            surf = Surface(
                lambda u, w: axes.c2p(u, w, psi(u, w, time)),
                u_range=[-6, 6],
                v_range=[-3, 3],
                resolution=(64, 32),
            )
            surf.set_style(fill_opacity=0.9, stroke_width=0.3, stroke_color=WHITE)
            surf.set_fill_by_value(
                axes=axes,
                colorscale=[(BLUE_E, -1), (TEAL, 0), (YELLOW, 1)],
                axis=2,
            )
            return surf

        surface = always_redraw(make_surface)

        # --- animation --------------------------------------------------
        self.add(axes, surface)
        self.wait(0.5)
        self.begin_ambient_camera_rotation(rate=0.08)
        self.play(t.animate.set_value(T), run_time=10, rate_func=linear)
        self.stop_ambient_camera_rotation()
        self.wait()