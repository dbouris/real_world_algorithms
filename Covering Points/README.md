# Covering Points
View the assignment instructions [here](https://louridas.github.io/rwa/assignments/covering-points/)

## Running the code
`python points_cover.py [-f] [-g] points_file`
- The argument `-f`(full exploration), if given, instructs the program to find the best solution, examining as many subsets as needed. If the argument `-f` is not given, the program will execute the greedy algorithm.
- The argument `-g` (grid), if given, instructs the program to find only lines that are horizontal or vertical. If it is not given, the program may use any lines that pass through the points.
- The argument `points_file` is the name of the file that contains the points we want to cover. (x,y) coordinates are separated by a space. Each point is on a separate line.

### Examples
`python points_cover.py example_1.txt` <br>
`python points_cover.py -f -g example_1.txt` <br>
`python points_cover.py -g example_2.txt`<br>
`python points_cover.py -f -g example_2.txt`