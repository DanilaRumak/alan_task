# Box task

Основной файл - box.py, в нем реализация нужного класса Box. Теперь к деталям реализации

Нам нужно генерировать шары с нужными вероятностями. Для этого мы сначала сгенерируем
с искомыми веротяностями характеристики, а затем выберем равномерно любой обьект удовлетворяющий
условию. В первом приближении, без доп-памяти это будет очень долго, так как нам надо
какждый раз генерировать в pandas табличке возможные строчки через предикат (self.data["color"] == color) & (self.data["texture"] == texture)],
следовательно в дальнейшем мы хотим предподсчитывать индексы, чтобы быстро находить
те шары, у которых сгенерированный нами цвет и форма.

Далее идет перебор способов, в изначальном приближении решения с предподсчетом индексов и 
конвертом шаров в pandas таблицу получаем 1.6 секунды на 10000 генераций (пример - закоменченый класс PandasBox).
Ботлнек в данном случае - использование пандас таблички, она уже не нужна, так как мы исчем
не по предикату, а по индексам, и второй, самый важный - долгое вычисление numpy.random.choice - 
нам придется пре-аллоцировать генерацию по батчам, так же мы можем в генерации индекса шара (после генерации цвета и текстуры)
использовать numpy.random.randint, который в разы быстрее. Получаем 0.112 секунды для 10000 запросов (итоговая реализация),
так же по результатам подсчетов видно, что при увеличении выборки доля шаров по характеристикам
сходится к заданым вероятностям:

```commandline
Execution took 0.053690792999987025 seconds
==================================================
green encountered in 0.3020 cases
red encountered in 0.4983 cases
blue encountered in 0.1997 cases
==================================================
==================================================
non-smooth encountered in 0.6522 cases
smooth encountered in 0.3478 cases
==================================================
```

Интересный факт здесь в том, что при увеличении количества шаров, время на выборку
фиксированного количества шаров не увеличивается.  Так же уменьшить время можно, грамотно подбирая размер
пре-аллокационного батча. Генерация по батчам выглядит как:

```python
    def _allocate_random_vars(self):
        self.pointer = 0
        self.alloc_colors = np.random.choice(self.colors, size=self.alloc_size, p=self.c_probs)
        self.alloc_textures = np.random.choice(self.textures, size=self.alloc_size, p=self.t_probs)
        # np.random.choice(self.joint_indexes[self.alloc_colors[i]][self.alloc_textures[i]])
        self.alloc_idx = [self.joint_indexes[self.alloc_colors[i]][self.alloc_textures[i]][np.random.randint(0, len(
            self.joint_indexes[self.alloc_colors[i]][self.alloc_textures[i]]))] for i in
                          range(self.alloc_size)]

    def get_ball(self):

        idx = self.alloc_idx[self.pointer]

        self.pointer += 1

        if self.pointer >= self.alloc_size:
            self._allocate_random_vars()

        return self.data[idx]
```

В строчке с присвоением alloc_idx очень большое выражение, но его никак не упростить, не увеличив время исполнения.
