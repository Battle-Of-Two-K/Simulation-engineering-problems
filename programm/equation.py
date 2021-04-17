
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

    def __init__(self, p, q, f_x):
        """
        Args:
            p: средний коэффициент
            q: свободный коэффициент
            f_x: функция, стоящая справа от = (в общем виде ДУ 2-го порядка)
        """
        self.middle_coeff = p
        self.free_coeff = q
        self.function = f_x

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
