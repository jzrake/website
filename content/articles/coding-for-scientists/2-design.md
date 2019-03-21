### The story of a new code
So how did we write codes like this in the first place? First, we wrote a simple program, say 100 lines, with a very limited scope, and it worked! Then, we improved its accuracy by adding another 100 lines in some new and better functions. And, we added a confguration flag so we could select between "old" and "new" level accuracy.

This process generally goes fast with a new code, for a simple and profound reason --- the code only consists of one or two small units. But then we add new levels of accuracy, and new capabilities, say logging, parallelism, and serialization. Of course, these new pieces of code depend on the old ones. For instance, the subroutines that facilitates parallelism need to communicate data structures used by the physics solver. This means we can't use the former without the latter. In other words, we did not write a new unit of code, we only inflated the existing unit.

This is how we create monoliths. This is why development slows down, why bugs begin to appear, why changing something in one module breaks something in another. This is why we get memory leaks and segmentation faults. And worse, it's why we use up CPU hours silently computing wrong numbers.

<br><br>

![monolith](https://4.bp.blogspot.com/-KPenZuhOwv4/UgogBWtUuHI/AAAAAAAAsL0/5VCAn1rh6s8/s1600/Artistic-Fields-Magnet-Magnets-Monolith.jpg)


### I can't let you do that, Dave...
Once our code has a mind of its own, it may be very difficult to bring it back under our control. The prospect of producing new science is more exciting than refactoring our code, and there may be time and career pressures that take precedence. So, we live with it. Sometimes the code propagates, and gets embedded in other projects, making it even more difficult to tame.

This accumulation of bad smelling code is sometimes referred to as _technical debt_. In our haste, we essentially purchased some capabilities on borrowed funds. We pay interest on these purchases until the debt is paid off, that is, until the code is properly factored. If poorly factored code is technical debt, then unit tests are money in the bank.

### Factoring and encapsulation
Proper development involves writing a new unit of code as if it lives in a vaccuum. This is called _encapsulation_, and that is the essence of object-oriented programming. Writing code as encapsulated units restores the speed and efficiency we had at the beginning of the development cycle.

>If poorly factored code is technical debt, then unit tests are money in the bank.

In practice, all of your units will require certain others to function. Well factored code is sorted into units based on what other units it depends on. Let's say we have a class `A`, which cannot function without access to other classes `B` and `C`. Refactoring means that we sort the methods of `A` by which of them require access to methods in `B` versus `C`. We then create two new classes `Ab` and `Ac`, which depend only on `B` and `C` respectively. If one of `A`'s methods depended on both `B` and `C`, then we split that method into two others, `Ab::part1` and `Ac::part2`. Then, in the subroutine which invoked `A`, we write something like the following:

    b = B()
    c = C()
    a1 = Ab(b)
    a2 = Ac(c)
    result1 = a1.part1()
    result2 = a2.part2(result1)

Sorry if that's a little obtuse, we'll cover more on specific techniques for refactoring later. The point for now is that code is testable as a unit exactly when it is properly factored, and that well factored code is sorted by dependency.

Even well factored code may not be strictly unit testable, but it doesn't have to be. The term for testing the interacting between two or more units of code is _integration testing_. This is likely to be the meat and potatoes of your test suite. In the example above, `Ab` still depends on `B`, and `Ac` still depends on `C`. The reason we refactored it was so that we could test the pairwise couplings directly. Sometimes the best factorization is not obvious immediately, but in the course of developing your code you will become more adept at spotting optimal factorizations.

## What not to do

Before we discuss specific techniques for code refactoring, I want to illustrate how our code gets to be "de-factored" in the first place. I'll use the example of writing a Godunov-type hydrodynamics code, something I have donemany times, and helped students to do. If you're interested in the context specifically, there is [a recipe here]({{root}}/static/how-to-write-a-hydro-code.pdf), that was written by [Weiqun Zhang](https://ccse.lbl.gov/people/weiqun). I'll write the examples in Python-like pseudo code.

### My first hydrodynamics code
The first thing a hydro code needs is a grid. A grid has a shape and an extent, and some type of geometrical information attached to it:

{# highlight Python #}

    class Grid:
        geometry = 'spherical'
        shape = [32, 32, 64]
        lower = [1.0, 0.0, 0.0]
        upper = [10.0, PI, 2 * PI]
        nfields = 5 # number of field variables

{# endhighlight #}

This class looks good so far. It describes a `32 x 32 x 64` chunk of logically cartesian grid points in a spherical geometry, with polar and azimuthal angles covering the whole sphere. The next thing we need is a way to initialize some data on the grid. Since the grid knows the location of its lattice points, let's add a member function that sets initial data by calling a function `f(r, theta, phi)`.

{# highlight Python #}

    class Grid:
        def set_initial_density(self, f):
            self.solution = numpy.zeros(self.shape + [self.nfields])

            for i in range (shape[0]):
                for j in range (shape[1]):
                    for k in range (shape[2]):
                        r, theta, phi = self.coordinate_at_index(i, j, k)
                        self.solution[i,j,k] = f(r, theta, phi)

        def coordinate_at_index(self, i, j, k):
            """
            Compute the coordinates of a given lattice point
            i, j, k (assuming the grid has uniform spacing).
            """
            N, U, L = self.shape, self.lower, self.upper
            x0 = L[0] + (i + 0.5) * (U[0] - L[0]) / N[0]
            x1 = L[1] + (j + 0.5) * (U[1] - L[1]) / N[1]
            x2 = L[2] + (k + 0.5) * (U[2] - L[2]) / N[2]
            return x1, x2, x3

{# endhighlight #}

Great! The next thing we need to do is advance the solution in time. The grid already has the solution data, because we just initialized it. So, it seems logical to stick a function in there that can evolve that data to the next time step:

{# highlight Python #}

    class Grid:
        def advance(self, dt):
            # Do some complicated stuff to get a time derivative, L
            self.solution += dt * L[0]

{# endhighlight #}



The "complicated stuff" referred to in the comment includes setting boundary conditions, interpolating the solution from cell centers to interfaces, and solving a Riemann problem. The class also needs to remember how many step it has taken, and what time it's at. So, we added methods and member data for those things as well...

But now this is getting exciting! Let's add a method to write the solution to a file so we can see our creation. And, another method to read that data back so we can restart the run at a later time.

### Some reflection
Now, let's look the methods and data in our `Grid` class:

{# highlight Python #}

    class Grid:
        time = 0.0
        iteration = 0
        def set_initial_data(self, f): pass
        def coordinate_at_index(self, i, j, k): pass
        def advance(self, dt): pass
        def solve_riemann_problems(self): pass
        def apply_boundary_condition(self): pass
        def interpolate_solution(self): pass
        def write_checkpoint(self, filename): pass
        def read_checkpoint(self, filename): pass

{# endhighlight #}

You might think of this list of the class's methods as its _curriculum vitae_, the types of responsibilities it is able to assume. Evidently this class's skills fall under roughly five catagories:

1. Getting geometrical information about a lattice
2. Storing solution data
3. Storing a simulation state
4. Updating solution data (algorithms)
5. Exchanging solution data with the file system

Now, we ask ourselves, which of these things should really be the responsibilities of a class called `Grid`? Certainly number 1, and _maybe_ number 2. But what about the others? Is the simulation state a property of a `Grid`, or how about the algorithms responsible for advancing the solution? A better name for this class is probably `Simulation`, because it does everything! Some programmers call this type of bad code smell a [God object](https://en.wikipedia.org/wiki/God_object).

But what's really the problem? Why not just rename the class `Simulation` and be done with it? Indeed, your code might then be _organized_. But, it would still not be _factored_. Why not? Because it can't be unit tested! Why not? Because it's not composed of testable units! To determine whether the Riemann solver is working, we first need a `Grid` class. But now suddenly we are testing the behavior of the whole code, which is not unit testing.

### My second hydro code
When I discovered this as a graduate student, I decided to "improve" things a bit. I separated these responsibilities into classes with more better fitting names. Something like this:


{# highlight Python #}

    class Simulation:
        grid = SphericalGrid()
        data = SolutionData()
        status = SimulationStatus()
        solutionScheme = MethodOfLinesTVD()
        checkpointWriter = CheckpointWriterHDF5()

{# endhighlight #}

On the surface, this looks much better! I even used some fancy stuff like "inheritance," meaning that each of those classes can be exchanged for a different one that does the same type of thing in a different way. For example, `CheckpointWriterHDF5` inherits `CheckpointWriter`, as does `CheckpointWriterASCII` and `CheckpointWriterBinary`. The concrete class that fulfills the abstract responsibility of writing checkpoints need only be considered when the `Simulation` class is first constructed.

Now, all that's left is to get things initialized. Hmm. Well, a `SolutionData` certainly needs to know the shape of the grid. And, a `CheckpointWriter` needs a `SolutionData` and also a `SimulationStatus` so it has something to write. It's such a headache to think about which parts need which other parts, why not simply give all the classes access to the main simulation class? Then they can get whatever they want, anytime!

{# highlight Python #}

    class Simulation:
        def __init__(self):
            self.grid.simulation = self
            self.data.simulation = self
            self.status.simulation = self
            self.solutionScheme.simulation = self
            self.checkpointWriter.simulation = self

{# endhighlight #}

![wolf](http://fablesofaesop.com/wp-content/uploads/2013/11/0135-100.jpg)


This is __very__ wrong, as it has only made the problem worse. Because, I have now essentially coupled every component of the code to every other component, without restricting whatsoever how the state of one might influence the behavior of another. That is precisely what leads to the crippling level of complexity that can render a project unmaintainable. Actually, this type of monolithic design is more incidious, because it _looks_ like an object-oriented system! It is a wolf in sheep's clothing.



---------------
[Previous]({{root}}/articles/coding-for-scientists/1-testing.html) --- [Next]({{root}}/articles/coding-for-scientists/3-tools.html)
