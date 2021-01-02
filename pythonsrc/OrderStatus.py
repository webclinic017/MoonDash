import enum
# Using enum class create enumerations

class OrderStatus(enum.Enum):
    NO_ORDER = 1
    LONG = 2
    SHORT = 3
    SQUARE_OFF = 4
    NEXT_ORDER = 5