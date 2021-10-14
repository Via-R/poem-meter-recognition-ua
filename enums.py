class StressType:
    '''Types of stresses in words for pattern generation.'''

    UNKNOWN = 0
    UNSTRESSED = 1
    ONE_SYLLABLE = 2
    TWO_SYLLABLES_FIRST_STRESSED = 3
    TWO_SYLLABLES_SECOND_STRESSED = 4
    MORE_THAN_TWO_SYLLABLES = 5

class MeterType:
    '''Types of metrical feet.'''

    IAMB = "ямб"
    CHOREE = "хорей"
    DACTYL = "дактиль"
    AMPHIBRACH = "амфібрахій"
    ANAPEST = "анапест"
    UNKNOWN = "невизначений"
