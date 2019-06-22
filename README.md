# Solve-TSP-with-GA
Solve the traveling salesman problem (TSP) using a genetic algorithm.
This time, we have converted the problem of visiting each prefecture of Kyushu in Japan into TSP.
This program finds the minimum cost of the TSP and plots it on a graph. It also shows the lowest cost routes on the OpenStreetMap.



## Requirements
- Python 3.6+

Install python libraries:

```bash
$ pip install numpy
$ pip install matplotlib
$ pip install folium
$ pip install pandas
```

## Usage
```bash
$ git clone https://github.com/yhayashi34884/Solve-TSP-with-GA
$ cd Solve-TSP-with-GA
```

Execute following command.

```bash
$ python GA_TSP.py
```

result (for example).

```bash
************************ Number of generations : 1 *************************
Fitness = [2.76075, 3.067, 5.78709, 4.35582, 0.90195, 0.90195, 1.08273, 3.18657, 4.49656, 0.0]
Minimum Cost = 40590
Route = [46, 44, 43, 45, 47, 40, 41, 42]
************************ Number of generations : 2 *************************
Fitness = [3.66413, 6.9138, 5.20387, 3.80697, 5.37201, 6.37571, 0.0, 2.9611, 1.76176]
Minimum Cost = 40590
Route = [46, 44, 43, 45, 47, 40, 41, 42]
・
・
・
************************ Number of generations : 100 *************************
Fitness = [11.94901, 11.94901, 11.94901, 11.94901, 11.94901, 11.94901, 11.94901, 0.05424, 0.0]
Minimum Cost = 33900
Route = [46, 47, 40, 41, 42, 43, 44, 45]
```
![Figure_ex_tsp](https://i.imgur.com/3sxjo9P.png)

After execution, an HTML file "map.html" is generated.

![OSM](https://i.imgur.com/9QveivI.png)



## Contributing
Contributions, issues and feature requests are welcome.

## Author
- Github: [yhayashi34884](https://github.com/yhayashi34884)

## Show your support
Please STAR this repository if this software helped you!

## License
This software is released under the MIT License.
<div lang="en" dir="ltr">
<p>OpenStreetMap<sup><a href="#trademarks">&reg;</a></sup> is <i>open data</i>, licensed under the <a href="https://opendatacommons.org/licenses/odbl/">Open Data Commons Open Database License</a> (ODbL) by the  <a href="https://osmfoundation.org/">OpenStreetMap Foundation</a> (OSMF). </p>
</div>
