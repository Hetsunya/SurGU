import gym
from stable_baselines3 import SAC
from stable_baselines3.common.env_checker import check_env

from car_track import Track  # Замените на имя класса

env = Track()
check_env(env)  # Проверка на совместимость со стандартом gym


model = SAC("MlpPolicy", env, verbose=1, learning_rate=0.001,
            buffer_size=1000000, batch_size=256, gamma=0.99)

model.learn(total_timesteps=100000)  # Количество шагов можно корректировать

model = SAC.load("sac_car_track_agent")
obs = env.reset()
for _ in range(1000):
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()

