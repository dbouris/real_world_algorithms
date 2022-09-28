# Samuel Beckett and Gray Codes
View the assignment instructions [here](https://louridas.github.io/rwa/assignments/samuel-beckett-and-gray-codes/)

## Running the code
`python beckett_gray.py [-a | -b | -u | -c | -p] [-r] [-f] [-m] number_of_bits`

- `-a`: find all codes (cycles and paths)
- `-b`: find Beckett-Gray codes
- `-u`: find Beckett-Gray paths (not cyles)
- `-c`: find cyclical codes
- `-p`: find Gray paths
- `-r`: find reverse isomorphisms
- `-f`: show the full binary representation of each code
- `-m`: show each code with a tabular representation
- `number_of_bits`: the number of bits of the code

### Examples
`python beckett_gray.py -a 3` <br>
`python beckett_gray.py -b 5` <br>
`python beckett_gray.py -b 5 -r` <br>
`python beckett_gray.py -b -f 5`