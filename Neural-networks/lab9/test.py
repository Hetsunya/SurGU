import gym
from gym import spaces
import numpy as np


from car_track import Track

class CarTrackEnv(gym.Env):
    def __init__(self, track: Track):
        super(CarTrackEnv, self).__init__()

        self.track = track

        # Определяем пространство действий (перестроение или ускорение на каждой полосе)
        self.action_space = spaces.Discrete(3)  # 3 действия: двигаться по полосе 1, 2, 3

        # Определяем пространство наблюдений: координаты, скорости, позиции
        # Размерность наблюдения зависит от того, какую информацию вы хотите передать агенту
        # В данном примере это будет список состояний всех автомобилей.
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0]),
            high=np.array([self.track.r, self.track.speed_limit, self.track.r]),
            dtype=np.float32
        )

    def reset(self):
        # Сбрасываем состояние среды
        self.track.reset(self.track.n, self.track.r)
        return self.get_observation()

    def step(self, action):
        # Выполняем шаг симуляции с выбранным действием
        self.track.set_vehicles_type(action)  # Применяем действие (например, перестроение)
        self.track.step()  # Обновляем состояние всех автомобилей

        # Получаем наблюдение
        observation = self.get_observation()

        # Рассчитываем награду
        reward = self.calculate_reward()

        # Проверяем завершение эпизода (например, когда все автомобили пришли к финишу или по времени)
        done = self.is_done()

        return observation, reward, done, {}

    def get_observation(self):
        # Возвращаем наблюдение (например, позиции и скорости всех автомобилей)
        return np.array(self.track.get_vehicles_speed())

    def calculate_reward(self):
        # Здесь можно рассчитать награду для агента
        # Например, награда может быть больше, если агент двигается быстрее или избегает столкновений
        reward = 0.0
        for v in self.track.get_vehicles_speed():
            reward += v / self.track.speed_limit  # Поощрение за скорость
        return reward

    def is_done(self):
        # Условия завершения эпизода
        return False  # Пока не определено, возможно завершение по времени

    def render(self):
        # Если необходимо, можем отобразить текущую ситуацию
        pass

    def close(self):
        pass


from stable_baselines3 import SAC
from stable_baselines3.common.vec_env import DummyVecEnv

# Оборачиваем вашу среду в DummyVecEnv для совместимости с Stable-Baselines3
# Создаём экземпляр Track (например, с 3 автомобилями и радиусом 100 метров)
track = Track(N=6, R=10)
env = DummyVecEnv([lambda: CarTrackEnv(track)])

# Создаём SAC-агента
model = SAC("MlpPolicy", env, verbose=1)

# Обучаем агента
model.learn(total_timesteps=100000)

# Сохраняем модель
model.save("sac_car_track_model")

# Проверяем результат
obs = env.reset()
for _ in range(1000):
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    if done:
        break
