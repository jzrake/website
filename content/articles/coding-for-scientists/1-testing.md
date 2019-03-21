### The need for testing
As scientists, it is not enough just to be right. Unless we can prove that we are right, our conclusions are just assertions. If we are using simulation results as scientific evidence, then those simulations need not only be correct, but provably so. So, we test our codes to render evidence they are correct. But the scope of code testing is much wider than that. Building software from small components that can be tested independently from one another ensures the fidelity of the larger system. This, in turn, keeps the project's complexity in check as it grows and evolves.


### Regression versus unit testing
In my own training, writing codes for astrophysical gasdynamics, I learned to validate my code by subjecting it to a suite of "test problems." A test problem is a set of initial conditions whose evolution in time is either known analytically, or possesses certain qualitative features that are generally accepted and documented in the literature. When our code can evolve some initial data consistently with our expectations, it is said to have passed a test problem.

Software professionals refer to this procedure as "regression testing" --- comparing the software's output with some benchmark data. Regression tests validate the code's performance as a whole, help ensure consistency of its results over time, and are an integral part of any project's test suite.

However, they are not the whole shebang. A code that passes a regression suite but is not _unit tested_ is like a car that drives, but has no dipstick to check the oil. In a car like that, the only way to find out whether the engine had any oil would be to drive it and hope the engine doesn't explode (in which case we would know there was no oil). But a mechanic would never service a car like that, and nobody would ever buy one. Just one more car analogy --- think of the old way emissions were tested, by hooking up a sensor to the tailpipe. A machine would produce a readout of the exhaust's chemical composition, but had no way to determine which of the car's components was contributing which fume. These days, emissions testing is closer to a suite of unit tests, where the car's computer provides reports from different stages of the combustion process (which is honest assuming it's not a VW).

Similarly, a code that has unit tests provides a detailed report of its internal condition by running its individiual parts in isolation. Obviously, this makes it easier for us to extend and maintain it. But it also demands better quality composition, namely, that the code is properly factored (meaning that its parts _can_ be run in isolation). That is where the design aspect enters, and we'll cover that in [Section 2]({{root}}/articles/coding-for-scientists/2-design.html).

### In my own experience
Somehow or another, many of us write our science codes dependent entirely on regression tests. We commonly run all the parts in combination until we get the code to pass test problems. Then, we make figures that proving the code's aptitude on those tests, and file them away or put them in a paper. Diagostics like the code's order of convergence are particulary important because they are quantitative, but they are also labor-intensive and difficult to automate. So, we usually test them once and save figures documenting the code's behavior at one point in time. Henceforth we modify any critical lines of code at our own peril, and hope that if we broke something, it makes a huge noise and not a quiet one.

If we're lucky, someone has automated some regression tests, so before commiting our changes we can ensure we haven't broken someone else's test problem. I don't know of anyone who uses automated numerical convergence tests. Doing so would ensure quantitatively that the solvers are functioning at their rated level of accuracy.


### True units and integration tests
A pure unit of code is one whose functioning is entirely self-contained. That is, you just provide it some data, and it returns an answer without referencing other modules in your project. Sometimes this looks like it can't be accomplished, but it can. Consider a unit of code contained in class called `Bicycle`. The bicycle depends on some wheels in order to ride, so it appears like it does not exist as a pure unit. However, if our design is modular then we can use what is sometimes called a _test double_, which in this case might be a trivial implementation of a wheel component --- one which may not be so light or aerodynamic, but which we know cannot fail. Then, any unexpected outcome when we call `Bicycle::ride()` must indicate a fault in the `Bicycle` class.

It is generally good practice to aim for components that are either pure units, or function when they are combined with one or two other components. Tests which are run on a few components wired together are called _integration test_, and are likely to form the majority of your tests.

It should not be necessary to be exhaustive in writing unit and integration tests. In my own experience, even sanity checks can expose a surprising number of issues that would otherwise break the code somewhere else. For example, a sanity check might ensure that a method for finite-differencing does not index an array out-of-bounds, or that the size of the array it returns is what we expect. Even just having a single boring test ensures that a component can be started up in relative isolation, which by itself is valuable. Having the boring test also gives you a place to start from if you suspect the component is doing something wrong. Rather than run the whole application, just throw some mock data at the component in your unit test and see what comes back. When the result is correct, don't delete the new test! You just expanded your test suite.


### Automated testing
Good practice, in my own opinion, is to write the code with built-in unit tests. Allow your code to be run in various modes based on a word given to the command line: `./mycode do-science` to run a research problem or `./mycode test` to run through the suite of unit and integration tests.

Although it's not necessary, it can be quite helpful to use a framework for unit testing. There are many to choose from, but I prefer it if the framework comes in a header file, because then you simply `#include` it in the source file that does the testing, and it does not add an external dependency to your project. A good example for C++ code is called [Catch](https://github.com/philsquared/Catch).


---------------
[Previous]({{root}}/articles/coding-for-scientists/0-introduction.html) --- [Next]({{root}}/articles/coding-for-scientists/2-design.html)
