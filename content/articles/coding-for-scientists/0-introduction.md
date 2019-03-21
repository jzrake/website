### Overview
Scientists write a lot of code. However most of us were not trained as software engineers. More likely, we learned to code on-the-job, from other scientists who learned the same way. So, it's no surprise that the software tools we devise to meet scientific challenges are, well, not always "optimal." In design, our codes tend to be complex where they could be simple, and brutish where they could be elegant. Stylistically, we write code in our own idiosyncratic ways, rather than adhering to established guidelines. In worst cases, we end up with software that sometimes breaks mysteriously, or that can't be easily validated.

What we want is software that is a pleasure to work with, which can be shared with collaborators, and from which we consistently derive scientific productivity. This means our program should work when we pick it up 3 years from now on a different machine, or when we send it to a colleague. The source code should remain understandable to us Long after we forgot how we wrote it. Most importantly, we (or the code itself) must be able to prove that it works.

The opposite state of affairs may have unfortunate consequences for our productivity, and even at times our psychological well-being. Many of us know what it's like to fret over a piece of code that crashes "sometimes" and not others, or only on certain computers. How do we sleep soundly after deploying lines of code that will consume millions of CPU hours?

Poor software integrity also translates to the quality of our science results. I have seen interesting questions go unexplored for reasons unrelated to accuracy or correctness of algorithms, or access to CPU hours. For example, I mentored a student who exposed a bug in a cosmology code by trying to write a diagnsotic that would reveal new details about her results. She found that a function which meant only to query the simulation data triggered a mysterious side-effect that ultimately led to a segmentation fault. The issue occured rarely, and only when the code was run in parallel on many cores. In the end, we never found the bug, and good science was left unaddressed.

There is also the question of workflow. A good program should be written for people to use it. Its means of control should be clearly documented, and its output products must be well defined. The code should be able to make snapshots of its internal state, to which it may be restored at a later time by reading a file or a directory.

Do we all need to be guru software architects to improve on the current situation? In these articles, I hope to demonstrate that we do not. For the most part, we're not facing the types of enormous design challenges such specialists are required for. As complex as science simulation codes may become, they pail in comparison to the types of codes that push the limits of software design. For our own purposes, there are well established, and rather accessible principles and methodologies that would go a long way if they were made relevant and accessible. That's what I'm hoping these articles will provide.


### 1. Testing

I believe the most important thing we ought to do, and by and large have not been shown how to do, is to properly test our codes. That may sound trivial, because scientists do, of course, test their codes. The relevant question is _how_ do they do their testing? Is a module tested once using some `printf`'s, and then assumed to work properly forever onwards? In my own carreer, I hereby confess to wasting unspeakable swaths of time on research-critical development doing things this way. If I suspected a bug to have emerged in a section of code, I would write new `printf`'s or fire up a debugger. Then I would launch the application and search thousands of output lines for evidence of the problem's source. Once convinced it was fixed, I would erase the `printf`'s or close the debugger, and resume believing that piece of code to be correct.

I wish I could plead that I knew better than this. But, I knew that formal methods existed for preventing this type of cycle. I even knew how to write a unit test. The problem was not even laziness! In hindsight, I now know the problem was that I _couldn't_ unit test my code, for a very obvious reason. My code was not composed of testable units! So instead, I resorted mostly to _regression_ tests, which aim to validate the code's output against some produced at an earlier time when the code was thought to be working well.

In an article on on testing, I'll explain the difference between different types of testing strategies, and argue that proper unit tests serve multiple purposes. Asside from guaranteeing correctness, they ensure proper factoring of the code, which is in turn the key to limiting the complexity of a piece of software.


### 2. Design

As scientists, the primary aspect of software design that we must concern ourselves with is ensuring that our code is testable. Accomplishing this is not trivial, but neither is it black magic. Simply put, code that can be unit tested is composed of testable units. When your software is in this state, it is said to be well factored, which means in turn that units of code are sorted by the data structures and functions to which they need access. Factoring is a skill which gets better with practice, as we learn to spot ways to piece things together with the fewest number of inter-dependencies.

As far as object-oriented design goes, I believe the only thing we _must_ utilize and understand is encapsulation, which means limiting the access a component has to the detailed functioning of its peers. Each function should define a "contract," something it promises to do as long the data you provide to it meets the stipulations of the contract. The details of the function fulfills its end of the bargain is its own business. If you are content not knowing, then you are respecting encapsulation.

Although object-oriented language constructs (as provided by modern Fortran or C++) can help to ensure encapsulation, they are not necessary. You can get good encapsulation without classes, or break it entirely while using them. Classes are commonly (sometimes unwittingly) used to write monolithic code! The converse is also true — elegantly factored code can be expressed without the help of fancy language features. In general, using a particular language syntax does not imply you are upholding the paradigm that syntax was meant to support.


### 3. Tools

As scientific programmers, I don't believe we need much heavy machinery to get our work done. Some awareness of tools that exist to solve common problems can go a long way, while too many dependencies can make your software, and your workflow, less portable. There is some nuance in deciding when to incorporate outside dependencies into your project, and when to solve the problem on your own.

Your primary tool is a good text editor — probably VI, Emacs, or Sublime Text. Other than that, know the basics of Makefile's and having a memory checker (valgrind) and a debugger (gdb or lldb) is probably sufficient.



---------------
[Previous]({{root}}/articles/coding-for-scientists.html) — [Next]({{root}}/articles/coding-for-scientists/1-testing.html)
