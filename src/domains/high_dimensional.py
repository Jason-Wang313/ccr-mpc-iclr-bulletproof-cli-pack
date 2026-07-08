"""Higher-dimensional CPU domain prototypes for CCR-MPC max-out work."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Tuple

import numpy as np


Array = np.ndarray


@dataclass(frozen=True)
class HighDimDomain:
    name: str
    label: str
    state_dim: int
    action_dim: int
    dt: float
    horizon: int
    shift_names: Tuple[str, ...]
    action_low: Tuple[float, ...]
    action_high: Tuple[float, ...]
    initial_state: Tuple[float, ...]
    step: Callable[[Array, Array, float], Array]
    constraint_margin: Callable[[Array], float]


def _clip_action(action: Array, low: Tuple[float, ...], high: Tuple[float, ...]) -> Array:
    return np.clip(np.asarray(action, dtype=float), np.asarray(low, dtype=float), np.asarray(high, dtype=float))


def cartpole_step(state: Array, action: Array, severity: float) -> Array:
    x, x_dot, theta, theta_dot = [float(v) for v in state]
    force = float(_clip_action(action, (-10.0,), (10.0,))[0])
    gravity = 9.81
    mass_cart = 1.0 + 0.15 * severity
    mass_pole = 0.1 + 0.05 * severity
    length = 0.5
    friction = 0.03 + 0.08 * severity
    total_mass = mass_cart + mass_pole
    polemass_length = mass_pole * length
    temp = (force + polemass_length * theta_dot**2 * np.sin(theta) - friction * x_dot) / total_mass
    theta_acc = (gravity * np.sin(theta) - np.cos(theta) * temp) / (
        length * (4.0 / 3.0 - mass_pole * np.cos(theta) ** 2 / total_mass)
    )
    x_acc = temp - polemass_length * theta_acc * np.cos(theta) / total_mass
    dt = 0.02
    return np.array([x + dt * x_dot, x_dot + dt * x_acc, theta + dt * theta_dot, theta_dot + dt * theta_acc])


def bicycle_step(state: Array, action: Array, severity: float) -> Array:
    px, py, yaw, v = [float(v) for v in state]
    accel, steer = _clip_action(action, (-2.0, -0.45), (2.0, 0.45))
    dt = 0.08
    wheelbase = 0.32
    friction = 1.0 - 0.18 * severity
    steer_bias = 0.06 * severity
    delay_gain = 1.0 - 0.10 * severity
    steer_eff = delay_gain * (float(steer) + steer_bias)
    accel_eff = friction * float(accel)
    v_new = np.clip(v + dt * accel_eff, 0.0, 4.0)
    yaw_rate = v_new / wheelbase * np.tan(steer_eff)
    yaw_new = yaw + dt * yaw_rate
    return np.array([px + dt * v_new * np.cos(yaw_new), py + dt * v_new * np.sin(yaw_new), yaw_new, v_new])


def quadrotor_step(state: Array, action: Array, severity: float) -> Array:
    x, z, vx, vz, theta, omega = [float(v) for v in state]
    thrust, torque = _clip_action(action, (0.0, -1.0), (18.0, 1.0))
    dt = 0.04
    mass = 1.0 + 0.25 * severity
    inertia = 0.025 * (1.0 + 0.15 * severity)
    wind = 0.8 * severity
    motor = 1.0 - 0.10 * severity
    g = 9.81
    thrust_eff = motor * float(thrust)
    ax = -thrust_eff * np.sin(theta) / mass + wind
    az = thrust_eff * np.cos(theta) / mass - g
    omega_new = omega + dt * float(torque) / inertia
    theta_new = theta + dt * omega_new
    vx_new = vx + dt * ax
    vz_new = vz + dt * az
    return np.array([x + dt * vx_new, z + dt * vz_new, vx_new, vz_new, theta_new, omega_new])


def pushing_step(state: Array, action: Array, severity: float) -> Array:
    ox, oy, theta, speed = [float(v) for v in state]
    push_mag, push_angle = _clip_action(action, (0.0, -np.pi), (1.0, np.pi))
    dt = 0.08
    friction = 0.7 + 0.35 * severity
    mass = 1.0 + 0.30 * severity
    contact_bias = 0.20 * severity
    direction = float(push_angle) + contact_bias
    accel = float(push_mag) / mass - friction * speed
    speed_new = max(0.0, speed + dt * accel)
    theta_new = theta + dt * 0.15 * float(push_mag) * np.sin(direction - theta)
    return np.array([
        ox + dt * speed_new * np.cos(direction),
        oy + dt * speed_new * np.sin(direction),
        theta_new,
        speed_new,
    ])


def domains() -> Dict[str, HighDimDomain]:
    return {
        "cartpole_safety": HighDimDomain(
            name="cartpole_safety",
            label="D1b cartpole safety envelope",
            state_dim=4,
            action_dim=1,
            dt=0.02,
            horizon=80,
            shift_names=("cart_mass", "pole_mass", "friction"),
            action_low=(-10.0,),
            action_high=(10.0,),
            initial_state=(0.0, 0.0, 0.08, 0.0),
            step=cartpole_step,
            constraint_margin=lambda s: min(2.4 - abs(float(s[0])), 0.55 - abs(float(s[2]))),
        ),
        "dynamic_bicycle_4d": HighDimDomain(
            name="dynamic_bicycle_4d",
            label="D2 4D dynamic bicycle",
            state_dim=4,
            action_dim=2,
            dt=0.08,
            horizon=55,
            shift_names=("friction", "steering_bias", "actuator_delay"),
            action_low=(-2.0, -0.45),
            action_high=(2.0, 0.45),
            initial_state=(0.0, 0.35, 0.02, 1.2),
            step=bicycle_step,
            constraint_margin=lambda s: min(1.0 - abs(float(s[1])), 0.8 - abs(float(s[2]))),
        ),
        "planar_quadrotor_6d": HighDimDomain(
            name="planar_quadrotor_6d",
            label="D3 6D planar quadrotor",
            state_dim=6,
            action_dim=2,
            dt=0.04,
            horizon=70,
            shift_names=("wind", "payload_mass", "motor_strength"),
            action_low=(0.0, -1.0),
            action_high=(18.0, 1.0),
            initial_state=(0.0, 1.0, 0.0, 0.0, 0.04, 0.0),
            step=quadrotor_step,
            constraint_margin=lambda s: min(float(s[1]) - 0.25, 2.2 - float(s[1]), 0.7 - abs(float(s[4]))),
        ),
        "pushing_contact_4d": HighDimDomain(
            name="pushing_contact_4d",
            label="D4 quasi-static pushing/contact",
            state_dim=4,
            action_dim=2,
            dt=0.08,
            horizon=50,
            shift_names=("object_mass", "table_friction", "contact_point_bias"),
            action_low=(0.0, -np.pi),
            action_high=(1.0, np.pi),
            initial_state=(0.0, 0.0, 0.0, 0.0),
            step=pushing_step,
            constraint_margin=lambda s: min(1.2 - abs(float(s[0])), 1.2 - abs(float(s[1])), 1.0 - abs(float(s[2]))),
        ),
    }
