# Graph Colouring Based Register Allocation
## Introduction
Programs are written as if there are only two kinds of memory: main memory and disk. Programmer is responsible for moving data from disk to memory (e.g., file I/O). Hardware is responsible for moving data between memory and caches. Compiler is responsible for moving data between memory and registers. Compilers are good at managing registers, and here we choose to implement a method to improve it further, to manage the registers more efficiently and quickly.

An intermediate code uses as many temporaries as necessary. This complicates final translation to assembly, but simplifies code generation and optimization. A typical intermediate code uses too many temporaries.

for further details look up the report attached.
## Packages Used
* Networkx
* numpy
* matplotlib
