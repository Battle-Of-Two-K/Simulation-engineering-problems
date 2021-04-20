from math import e, cos, sin


class DiffEqSecKind:
    """
    Неоднородное дифференциальное уравнение 2-го порядка.
    Вид: x'' + px' + qx = f(x)

    Данный класс решает только частный случай
    данного уравнения, когда f(x) - это число
    и это НЕ единственное упрощение! Данный
    класс решает уравнение только в рамках
    поставленной задачи.
    """

    def __init__(self, p, q, f_x, initial_condition: tuple):
        """
        Args:
            p: средний коэффициент характеристического уравнения.
            q: свободный коэффициент характеристического уравнения.
            f_x: функция, стоящая справа от = (в общем виде ДУ 2-го порядка)
            initial_condition: начальные условия (кортеж с двумя значениями)
                               Первое: x(0) = <число>, второе: x'(0) = 0 (в
                               нашей задаче всегда 0). Так вот начальные усло-
                               вия в данном случае initial_condition = (<число>, 0).
        """
        self.middle_coeff = p
        self.free_coeff = q
        self.function = f_x
        self.first_condition = initial_condition[0]  # x(0) = <число>
        self.second_condition = initial_condition[1]  # x'(0) = 0

    def create_equation(self, time, time_factor):
        eq_roots = self.solve_characteristic_equation()

        # D = 0:
        if eq_roots[0] == eq_roots[1]:
            C_1 = self.first_condition - self.particular_solution_equation()
            C_2 = self.second_condition - C_1 * eq_roots[0]
            return (e ** (eq_roots[0] * time / time_factor) * (C_1 + C_2 * time / time_factor)) + \
                self.particular_solution_equation()

        # D < 0:
        elif isinstance(eq_roots[0], complex) or isinstance(eq_roots[1], complex):
            C_1 = self.first_condition - self.particular_solution_equation()
            C_2 = (self.second_condition - eq_roots[0].real * C_1) / eq_roots[0].imag
            return (e ** (eq_roots[0].real * time / time_factor)) * \
                   (C_1 * cos(eq_roots[0].imag * time / time_factor) +
                    C_2 * sin(eq_roots[0].imag * time / time_factor)) \
                + self.particular_solution_equation()

        # D > 0:
        else:
            C_1 = ((self.first_condition - self.particular_solution_equation()) -
                   (1 * self.second_condition / eq_roots[1])) / (1 - (1 * eq_roots[0] / eq_roots[1]))

            C_2 = (self.second_condition - eq_roots[0] * C_1) / eq_roots[1]

            return (C_1 * e ** (eq_roots[0] * time / time_factor) +
                    C_2 * e ** (eq_roots[1] * time / time_factor)) \
                + self.particular_solution_equation()

    def solve_characteristic_equation(self):
        """
        Решение характеристического уравнения
        Returns: корни характеристического уравнения
        """
        if self._calculate_discriminant() == 0:
            return -self.middle_coeff, -self.middle_coeff
        elif self._calculate_discriminant() > 0:
            return (-self.middle_coeff - (self._calculate_discriminant()) ** .5) / 2, \
                   (-self.middle_coeff + (self._calculate_discriminant()) ** .5) / 2
        else:
            return complex((-self.middle_coeff / 2), (self._calculate_discriminant() / 2)), \
                   complex((-self.middle_coeff / 2), -(self._calculate_discriminant() / 2))

    def particular_solution_equation(self):
        """
        Частное решение неоднородного уравнения.
        Добавляется к общему в конце расчёта.
        Возникает за счёт функции f(x), стоящей
        справа от =.
        Returns: частное решение неоднородного уравнения
        """
        return self.function / self.free_coeff

    def _calculate_discriminant(self):
        """
        Расчёт дискриминанта характеристического уравнения
        Returns: дискриминант характеристического уравнения
        """
        return self.middle_coeff ** 2 - 4 * self.free_coeff
