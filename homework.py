from abc import ABC


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Возвращает нформационное сообщение."""

        message = (f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {self.duration:.3f} ч.; '
                   f'Дистанция: {self.distance:.3f} км; '
                   f'Ср. скорость: {self.speed:.3f} км/ч; '
                   f'Потрачено ккал: {self.calories:.3f}.')
        return message


class Training(ABC):
    """Базовый класс тренировки."""

    M_IN_KM: float = 1000  # Константа
    LEN_STEP: float = 0.65  # Константа

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float, ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

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

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        training_type = self.__class__.__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(training_type, duration, distance, speed, calories)


class Running(Training):
    """Тренировка: бег."""

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float, ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        coeff_calorie_1: float = 18
        coeff_calorie_2: float = 20
        mean_speed = self.get_mean_speed()
        weight = self.weight
        duration = self.duration * 60  # время тренировки в минутах
        spent_calories = (coeff_calorie_1 * mean_speed - coeff_calorie_2
                          ) * weight / self.M_IN_KM * duration
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super(SportsWalking, self).__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        coeff_calorie_1: float = 0.035
        mean_speed = self.get_mean_speed()
        coeff_calorie_2: float = 0.029
        coeff_calorie_3: float = 2
        weight = self.weight
        duration = self.duration * 60  # время тренировки в минутах
        height = self.height
        spent_calories = (coeff_calorie_1 * weight +
                          (mean_speed ** coeff_calorie_3 // height)
                          * coeff_calorie_2 * weight) * duration
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38  # Константа

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

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
        coeff_calorie_1: float = 1.1
        coeff_calorie_2: float = 2
        weight = self.weight
        spent_calories = (mean_speed
                          + coeff_calorie_1) * coeff_calorie_2 * weight
        return spent_calories


def read_package(_workout_type: str, _data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    package_foo = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    result_package_foo = package_foo[_workout_type](*_data)
    return result_package_foo


def main(_training: Training) -> None:
    """Главная функция."""

    info = _training.show_training_info()
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
