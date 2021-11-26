from dataclasses import dataclass
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        result = (f'Тип тренировки: {self.training_type}; '
                  f'Длительность: {self.duration:.3f} ч.; '
                  f'Дистанция: {self.distance:.3f} км; '
                  f'Ср. скорость: {self.speed:.3f} км/ч; '
                  f'Потрачено ккал: {self.calories:.3f}.')

        return result


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: float
    duration: float
    weight: float
    M_IN_KM: ClassVar[float] = 1000
    LEN_STEP: ClassVar[float] = 0.65
    MIN_IN_HOUR: ClassVar[float] = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        distance = self.get_distance()
        duration = self.duration
        mean_speed = distance / duration
        return mean_speed

    def get_spent_calories(self) -> float or Exception:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(type(self).__name__
                                  + 'Функция не поддерживается')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        training_type = type(self).__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(training_type, duration,
                           distance, speed, calories)


@dataclass
class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1: ClassVar[float] = 18
    COEFF_CALORIE_2: ClassVar[float] = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        mean_speed = self.get_mean_speed()
        weight = self.weight
        duration = self.duration * self.MIN_IN_HOUR
        spent_calories = ((self.COEFF_CALORIE_1 * mean_speed
                           - self.COEFF_CALORIE_2)
                          * weight / self.M_IN_KM * duration)
        return spent_calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    COEFF_CALORIE_1: ClassVar[float] = 0.035
    COEFF_CALORIE_2: ClassVar[float] = 0.029
    COEFF_CALORIE_3: ClassVar[float] = 2

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        mean_speed = self.get_mean_speed()
        weight = self.weight
        duration = self.duration * self.MIN_IN_HOUR
        height = self.height
        spent_calories = ((self.COEFF_CALORIE_1 * weight
                           + (mean_speed ** self.COEFF_CALORIE_3 // height)
                           * self.COEFF_CALORIE_2 * weight) * duration)
        return spent_calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    length_pool: float
    count_pool: float
    LEN_STEP: ClassVar[float] = 1.38
    COEFF_CALORIE_1: ClassVar[float] = 1.1
    COEFF_CALORIE_2: ClassVar[float] = 2

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        length_pool = self.length_pool
        count_pool = self.count_pool
        duration = self.duration
        mean_speed = length_pool * count_pool / self.M_IN_KM / duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        mean_speed = self.get_mean_speed()
        weight = self.weight
        spent_calories = ((mean_speed + self.COEFF_CALORIE_1)
                          * self.COEFF_CALORIE_2 * weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    package_training = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in package_training:
        raise ValueError(f'{workout_type} не поддерживается')
    result = package_training[workout_type](*data)
    return result


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
