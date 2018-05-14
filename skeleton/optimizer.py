from building import *

# speed test - use "python optimizer.py" to run
if __name__ == "__main__":
    import timeit
    test_size = 20 # set to 100 to check time for speed race
    t1 = timeit.repeat(stmt="optimizer.max_food(b)", setup="import gc, building, optimizer; b = building.random_building({0}, True); gc.collect()".format(test_size), repeat=3, number=1)
    t2 = timeit.repeat(stmt="optimizer.max_supplies(b)", setup="import gc, building, optimizer; b = building.random_building({0}, False); gc.collect()".format(test_size), repeat=3, number=1)
    # some calculation that takes ~1 sec on my machine
    tref = timeit.repeat(stmt="for i in range(1000000): a=i^2", setup="import gc; gc.collect()", repeat=3, number=19)
    print("max_food(n={0}) = {1} ({3} normalized), max_supplies(n={0}) = {2} ({4} normalized)".format(test_size, min(t1), min(t2), min(t1) / min(tref), min(t2) / min(tref)))

def max_food(building):
    """returns the maximum number of food that can be collected from given building"""
    return building.size * 10 # dummy implementation - replace

def max_supplies(building):
    """returns the maximum of min(food,water) that can be collected from given building"""
    return building.size * 5 # dummy implementation - replace
