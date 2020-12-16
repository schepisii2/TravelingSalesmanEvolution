# TravelingSalesmanEvolution
A between semester competition where two students attempt to solve the traveling salesman problem using evolutionary algorithms.

# 1 Objective
Write a program to use Evolutionary Computation to find an approximate solution instances of the
Traveling Salesperson Problem (TSP). Your program must be able take a list of cities and their
intercity costs (an n  n distance matrix, where there are n cities). It should output a “tour” (the
list of cities visited in order), the total distance of the tour, and the number of evaluations needed
to find that solution. There’s more information about this below. The goal is to (in general) be able
to find the lowest cost tour with the fewest number of evaluations. You will be judged using data
sets to which you had access and data sets you have not seen!
We’re going to make the problem easier with a couple of assumptions that do not hold in the
general case. For our purpose, you may assume that the problem is symmetric (it costs the same to
go from A to B as the reverse trip). You may also assume that the initial graph is a complete graph,
that is: there is an edge between every pair of cities in the graph. Without these two assumptions
the problem is much harder.
You may use any kind of evolutionary algorithm you like. Our reference for this problem is
Chapter 16 from A.K. Dewdney’s The New Turing Omnibus:
https://drive.google.com/file/d/1wwM0PfJ-dzpochbbZX22jYAIbOJ7raZ8/view?usp=sharing

# 2 Input File Format
Your program will consider two input files. The first file is called the TSP specification file, and it
will contain two or three sections:
1. A header with key-value pairs, each on its own line and separated by a colon. E.g.,
NAME : att4
COMMENT : 4 capitals of the US
TYPE : TSP
DIMENSION : 4
EDGE_WEIGHT_TYPE : ATT
1
2. A section entitled NODE COORD SECTION, where each line represents a city and contains
an ID and xy coordinates, separated by spaces. E.g.,
NODE_COORD_SECTION
1 6734 1453
2 2233 10
3 5530 1424
4 401 841
3. The third section is optional and is entitled the TOUR SECTION. It contains a list of city IDs
representing the optimal tour (if known). This is for comparison purposes only; you should
not use this information in your program because it may not be given
The second file is called the intercity costs file. Each line represents the rows of the cost matrix,
where the implied order of the cities is given by the city order presented in the second section of
specifications file, and each value represents the cost of traveling from the city. For example, the
cities represented above might have a file with following content:
0 4727 1205 6363
4727 0 3588 2012
1205 3588 0 5163
6363 2012 5163 0
In other words, it costs 4; 727 to go from city 1 to city 2 (or vice-versa). In the simplest
case, this is just the distance between the cities . You can find example sets to play with here:
https://people.sc.fsu.edu/˜jburkardt/datasets/tsp/tsp.html

# 3 Evolutionary Algorithms
Dewdney talks about a “genetic algorithm”, but this term is a bit outdated. The more general turn
for algorithms that use abstract models of Darwinian to optimize are “evolutionary algorithms”
(EAs). Such methods iteratively use a parent population of candidate solutions (e.g., a possible
tour) to generate a child population of candidate solutions. Children are produced by making
slight changes to parents (a kind of “mutation”) and combining information from parents (a kind
of “recombination”). Candidate solutions are evaluated against the problem and assigned a fitness
(objective quality of the solution). There are different ways selection can work, both for picking
who gets to be parents, and by picking who survives into the next generation.
Here’s some very general pseudocode for a variety of evolutionary algorithms:
2
Algorithm 1: Generic EA pseudocode
initialize a population of parents of size ;
evaluate fitness 8x 2 P;
while While condition do
select the subset of parents who will breed;
apply genetic operators to generate population of children of size ;
evaluate fitness 8x 2 C select which individuals survive to become parents;
end
Decisions that algorithm writers typically must make:
• How to encode candidate solutions of the problem (representation)
• How to select parents for breeding (parent selection)
• How children are generated (genetic operators)
• How to decide who becomes parents in the next generation (survival selection)
• How to decide when to stop
For example, a classical “genetic algorithm” (GA) typically uses a binary encoding—individuals
are represented as a fixed-length string of 1’s and 0’s that maps to a solution to the problem in a
particular way. Breeding parents in a GA are often selected by drawing individuals from the parent
population probabilistically proportionate to their fitness. Genetic operators are typically bit-flip
mutation (flip each bit with independent probability 1
n, where n is the length of the binary string)
and 1-point crossover (pick a position c the binary string, then generate a child by taking the first c
bits from one parent and the remaining n 􀀀 c bits from the other). If there are  parents, then GAs
will typically generate  =  children, and all children survive to the next generation.
On the other hand “evolutionary strategies” (ES) work differently. There are two kinds: (; )
and ( + ). In either case, many types of encodings are possible and all parents breed to produce
 >>  children, typically only with some kind of mutation. In a (; )-ES, individuals are strictly
ordered by fitness and the best  of the  children become parents in the next generation, while
in a ( + )-ES, both the children and parents are strictly ordered and the best  of the  + 
individuals survive to become parents in the next generation.
There are many other variations. I’ve given you a few reference, below, for you to explore your
options.
Some advice on encoding and genetic operators for TSP: It’s best to start with operators that
preserve the idea of a tour so you don’t have to worry about “illegal” solutions (a list of cities that
are not a valid tour). For instance:
• Initialize by taking the ordered list of cities and shuffle them. Now every candidate solution
is a valid (though suboptimal) tour.
• Mutate by making some number of random swaps of cities, so the result is still a valid cycle.
3
• Start without recombination at all at first, and introduce it only if/when you think it will
improve things (Dewdney has a suggestion that may help).
Here’s a relatively modern Python library for EAs:
https://www.osti.gov/servlets/purl/1649229

# 4 Judging
You will give a very short presentation of your solution to a panel of faculty members at the start of
Fall term. You don’t need slides, just show us your program and talk about what choices you made
for your EA (representation, parent selection, genetic operators, survival selection, etc.). You’ll
also provide the judges with the code, so that they can run it on several (unknown) test cases, and
a short discussion of the tools you used for programming and communication.
Judges will consider several factors when choosing a solution:
• Does your program work and produce valid results?
• Does your program tend to get the lowest cost tour?
• Does your program tend to find its solution with the fewest evaluations?
• Did your team work well together?
• Did you make an effort to make your code clean, readable, and consistent?
A tour through cities A, B, C, and D might be: A ! C ! D ! B. The total cost of this tour
is the sum of the costs of the (A;C); (C;D); (D;B); and (B;A) edges.
Note that each iteration through an EA is typically called a generation, and though it’s pretty
common for the termination criteria to be a fixed count on the number of generations, your will be
counting the number of times you evaluate candidate solutions for performance purposes, not the
number of generations. So you must count every time you evaluate fitness, for whatever reason.

# 5 References
Some websites that may help:
• https://www.cs.vu.nl/˜gusz/papers/ec-intro-naw.pdf
• https://towardsdatascience.com/evolution-of-a-salesman-a-complete-genetic-algorithm-tutorial-for-python-6fe5d2b3ca35
• https://towardsdatascience.com/introduction-to-genetic-algorithms-including-example-code-e396e98d8bf3
• http://www.evolutionarycomputation.org/home/

