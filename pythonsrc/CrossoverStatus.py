import enum
# Using enum class create enumerations

class CrossoverStatus(enum.Enum):
    CROSSOVER = 0
    CROSSUNDER = 1
    NOCROSSOVER = 2