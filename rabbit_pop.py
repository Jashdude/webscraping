import numpy as np

# 1. Review the documentation for the np.loadtext() constructor. Load the csv data into an NumPy array using np.loadtext().
data = np.loadtxt('rabbit_population_1900_2019.csv',skiprows=1, delimiter=',', dtype=int)
populations = data[:, 1:]
year, Beveren, Havana, Lopear = data.T
# 2. What is the mean population for each breed?
mn = populations.mean(axis=0)
print(f"Q2. Mean for breeds Beveren:\n{mn[0]}, Havana:{mn[1]}, Lopear:{mn[2]}")
# 3. What is the standard deviation of the population for each breed?
sd = populations.std(axis=0)
print(f"Q3. Standard Deviation for breeds Beveren:\n{sd[0]}, Havana:{sd[1]}, Lopear:{sd[2]}")
# 4. In which year did each breed experience their maximum populations?
print(f"Q4. Year with largest population (Beveren, Havana, Lopear):\n{year[np.argmax(populations, axis=0)]}")
# 5. Which breed has the largest population for each year?
breed = ['Beveren', 'Havana', 'Lopear']
largest_each_year = zip(year,np.take(breed, np.argmax(populations, axis=1)))
print(f"Q5. Largest Population for each Year by Breed:\n{[i for i in largest_each_year]}")
# 6. In which years are any of the populations greater than 50000
print(f"Q6. Population > 50000:\n{year[np.any(populations > 50000, axis=1)]}")
# 7. In which 2 years did each breed experience their minimum population levels. ( Hint: consider np.argsort and fancy indexing)
print(f"Q7. 2 Year Minimum Population:\n{year[np.argsort(populations, axis=0)[:2]]}")
# 8. Rely on broadcasting to mean center all of the population columns.
# Your solution should simultaneously center all 3 columns. Print the resulting array.
pmean =  populations.mean(0)
pcentered = populations - pmean
print(f"Q8. Mean Centered - Broadcasting\n{pcentered.astype(int)}")
#9. Rely on broadcasting to normalize the population columns to the number of standard deviations from the mean.
# Your solution should simultaneously normalize all 3 columns. Print the resulting array.
np.set_printoptions(precision=2)
pstd = populations.std(0)
pnormalize = (populations - pmean)/pstd
print(f"Q9. Standard Deviation - Normalized Broadcasting:\n{pnormalize}")
