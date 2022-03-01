# Automated Warehouse Planning System
#### Description
A simplified version of automated planning done in Amazon warehouses, this project is an extension of one of the [ASP Challenges](https://sites.google.com/view/aspcomp2019/) from 2019. Finds optimal planning solutions for robot actions with the aim of fulfilling orders in a grid-based warehouse containing shelves (with products) and delivery points. Instances are configured using a GUI implemented with Python (feature currently incomplete) and solved with API calls to clingo.

<br/>
#### Usage
Requires installation of the [clingo solver](https://potassco.org/clingo/). Currently, the GUI is incomplete and the file *warehouse.lp* must be run through command line. The input file should be in the same format as described in the ASP [challenge](http://www.mat.unical.it/~dodaro/aspchallenge2019/automated-warehouse-scenario.package.zip) description document. The clingo file can be run through the command line using the following command:

`clingo warehouse.lp -c m=<number_of_time_steps> <max_number_of_solutions_to_show>`

<br/>
Where:

-`<number_of_time_steps>` is the number of time steps to allow for finding a solution (optimization code is not included at the moment)

-`<max_number_of_solutions_to_show>` is the maximum solutions the solver will output. A value of '0' here will force the solver to output every possible solution.
