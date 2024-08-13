
FROM HTTPS://WWW.CC.GATECH.EDU/~TURK/MATH_GR.HTML

MATHEMATICS FOR COMPUTER GRAPHICS
GREG TURK, AUGUST 1997

"What math should I learn in order to study computer graphics?" This is perhaps the most common general question that students ask me about computer graphics. The answer depends on how deeply you wish to go into the field. If you wish to begin to use off-the-shelf graphics programs then the answer is that you probably do not need to know very much math at all. If you wish to take an introductory course in computer graphics, then you should read the first two sections below for my recommendations (algebra, trigonometry and linear algebra). If you want some day to be a researcher in graphics then I believe that you should consider your mathematics education to be an ongoing process throughout your career.

If you do not particularly care for mathematics, is there still a chance of working in the field? Yes, a few areas within computer graphics are not much concerned with mathematical ideas. You should not give up on graphics just because you are not a math wizard. It is likely, however, that you will have more freedom in choosing research topics if you have a willingness to learn about new mathematical ideas.

There is no absolute answer to what mathematics is important in computer graphics. Different areas within the field require different mathematical techniques, and your own interests will likely lead you towards some topics and may never touch others. Below are descriptions of a number of areas in mathematics that I believe are useful in computer graphics. Do not feel that you need to be an expert in each of these areas to become a graphics researcher! I deliberately included many areas below to give a fairly broad view of the mathematical ideas used in graphics. Many researchers, however, will never find the need to look at some of the topics that I mention below.

Finally, although it should be clear from reading this, the opinions given within this document are entirely my own. It is likely that you would get a different list of topics or at least different emphases from other people who work in computer graphics. Now on to the list of topics.

1) ALGEBRA AND TRIGONOMETRY

    High-school level ALGEBRA AND TRIGONOMETRY are probably the most important areas to know in order to begin to learn about computer graphics. Just about every day I need to determine one or more unknowns from a simple set of equations. Almost as often I need to perform simple trigonometry such as finding the length of the edge of some geometric figure based on other lengths and angles. Algebra and trigonometry are the subjects that will solve such day-to-day tasks in computer graphics.

    What about the GEOMETRY that we learn in high school? It may come as a surprise, but our high school geometry is not very often needed for most tasks in computer graphics. The reason for this is that geometry as it is taught in many schools actually is a course in how to construct mathematical proofs. While proof construction is definitely a valuable intellectual tool, the actual theorems and proofs from your geometry class are not often used in computer graphics. If you go to graduate school in a mathematics related field (including computer graphics) then you may well find yourself proving theorems, but this is not necessary in order to start out in graphics.

    If you have a good understanding of algebra and trigonometry then you are quite prepared to begin reading an introductory book in computer graphics. Most such books contain at least an abbreviated introduction to the next important area of mathematics for computer graphics, namely linear algebra.

    BOOK RECOMMENDATION
        Computer Graphics: Principles and Practice
        James Foley, Andries van Dam, Steven Feiner, John Hughes
        Addison-Wesley
        [a huge book, but still my favorite]

2) LINEAR ALGEBRA

    The ideas of linear algebra are used throughout computer graphics. In fact, any area that concerns itself with numerical representations of geometry often will collect together numbers such as x,y,z positions into mathematical objects called vectors. Vectors and a related mathematical object called a matrix are used all the time in graphics. The language of vectors and matrices is an elegant way to describe (among other things) the way in which an object may be rotated, shifted (translated), or made larger or smaller (scaled). Linear algebra is usually offered either in an advanced high school class or in college. Anyone who wishes to work in computer graphics should eventually get a solid grounding in this subject. As I mentioned before, however, many textbooks in graphics give a reasonable introduction to this topic-- often enough to get you through a first course in graphics.

    BOOK RECOMMENDATION
        Linear Algebra and Its Applications
        Gilbert Strang
        Academic Press

3) CALCULUS

    Knowledge of calculus is an important part of advanced computer graphics. If you plan to do research in graphics, I strongly recommend getting a basic grounding in calculus. This is true not just because it is a collection of tools that are often used in the field, but also because many researchers describe their problems and solutions in the language of calculus. In addition, a number of important mathematical areas require calculus as a prerequisite. This is the one area in mathematics in addition to basic algebra that can open the most doors for you in computer graphics in terms of your future mathematical understanding.
    Calculus is the last of the topics that I will mention that is often introduced in high school. The topics to follow are almost always found in college courses.

4) DIFFERENTIAL GEOMETRY

    This area of mathematics studies equations that govern the geometry of smooth curves and surfaces. If you are trying to figure out what direction is perpendicular to (points directly away from) a smooth surface (the "normal vector") then you are using differential geometry. Making a vehicle travel at a particular speed along a curved path is also differential geometry. There is a common technique in graphics for making a smooth surface appear rough known as "bump mapping", and this method draws on differential geometry. If you plan to do work with curves and surfaces for shape creation (called "modeling" in the graphics field) then you should learn at least the basics of differential geometry. __MULTIVARIABLE CALCULUS (Анализ функций многих переменных, многомерный анализ)__ is the prerequisite for this area.

    BOOK RECOMMENDATION
        Elementary Differential Geometry
        Barrett O'Neill
        Academic Press

5) NUMERICAL METHODS

    Almost every time we represent and manipulate numbers in the computer we use approximate instead of exact values, and because of this there is always the possibility for errors to creep in. Moreover, there are often many different approaches to solving a given numerical problem, and some methods will be faster, more accurate or require less memory than others. The study of these issues goes by a number of names including "numerical methods" and "scientific computing". This is a very broad area, and several of the other areas of mathematics that I will mention can be considered sub-areas underneath this umbrella.
    These sub-areas include
        SAMPLING THEORY,
        MATRIX EQUATIONS,
        NUMERICAL SOLUTION OF DIFFERENTIAL EQUATIONS,
        and
        OPTIMIZATION.

    BOOK RECOMMENDATION
        Numerical Recipes in C: The Art of Scientific Computing
        William Press, Saul Teukolsky, William Vetterling and Brian Flannery
        Cambridge University Press
        [this is a very valuable reference but is not normally used as a textbook]

6) SAMPLING THEORY and SIGNAL PROCESSING (Теория обработки сигналов)

    Over and over in computer graphics we represent some object such as an image or a surface as a collection of numbers that are stored in a regular two-dimensional array. Whenever we do this we are creating a "sampled" representation of the object. A good understanding of sampling theory is important if we are to use and to control the quality of such representations. A common issue in sampling as it applies to graphics is the jagged edges that can appear on the silhouette of an object when it is drawn on a computer screen. The appearance of such jagged edges (one form of a phenomenon known as "aliasing") is very distracting, and this can be minimized by using well-understood techniques from sampling theory. At the heart of sampling theory are concepts such as CONVOLUTION, the FOURIER TRANSFORM, and SPATIAL AND FREQUENCY REPRESENTATIONS OF FUNCTIONS. These ideas are also important in the fields of image and audio processing.

    BOOK RECOMMENDATION
        The Fourier Transform and Its Applications
        Ronald N. Bracewell
        McGraw Hill

7) MATRIX EQUATIONS

    There are a wide variety of problems that come up in computer graphics that require the numerical solution of matrix equations. Some problems that need matrix techniques include: finding the best position and orientation to match one object to another (one example of a "least squares" problem), creating a surface that drapes over a given collection of points with minimal creases (thin-plate splines), and simulation of materials such as water or cloth. Matrix formulations of problems come up often enough in graphics that I rank this area very high on my list of topics to know.

    BOOK RECOMMENDATION
        Matrix Computations
        Gene Golub and Charles Van Loan
        Johns Hopkins University Press

8) PHYSICS

    Physics is obviously a field of study in its own right and not a sub-category of mathematics. Nevertheless, physics and mathematics are closely tied to one another in several areas within computer graphics. Examples of graphics problems that involve physics include how light interacts with the surfaces of objects, how light bounces around in a complex environment, the way people and animals move, and the motion of water and wind. Knowledge of physics is important for simulating all of these phenomena. This is closely tied to solving differential equations, which I shall discuss next.

9) NUMERICAL SOLUTIONS OF DIFFERENTIAL EQUATIONS

    It is my belief that techniques for solving differential equations are extremely important to computer graphics. As we just discussed, much of computer graphics is devoted to simulating physical systems from the real world. How waves form in water and how an animal walks across the ground are two examples of physical simulation. Simulation of physical systems very often leads to numerical solutions of differential equations. Note that this is actually very different than symbolic solutions to differential equations. Symbolic solutions are exact answers, and usually can be found only for extremely simple sets of equations. Sometimes a college course called "Differential Equations" will only examine symbolic solutions, and this will not help much for most computer graphics problems.

    In physical simulation, one breaks the world down into little pieces that are represented as large vectors. Then the relations between the parts of the world are captured in the entries in matrices. Solving the matrix equations that arise is not usually done exactly, but is instead performed by carrying out a long series of calculations that yields an approximate solution as a list of numbers. This is what numerical solutions of differential equations are about. Note that the solution of matrix equations is an intimate part of numerical solutions to differential equations.

10) OPTIMIZATION

    Quite often in computer graphics we are looking for a description of an object or a collection of objects that satisfies some desired goal. Examples include looking for the positions of lights that give a certain "feeling" to how a room is lit, figuring out how an animated character can move its limbs to carry out a particular action, and positioning shapes and text on a page so that the result does not look cluttered. Each of these examples can be stated as an optimization problem. Ten years ago there was little in the graphics literature that made use of optimization techniques, but the field is using optimization more and more in recent work. I think that optimization will continue to play an increasingly important role in computer graphics.

11) PROBABILITY and STATISTICS

    There are a number of areas within computer graphics that make use of probability and/or statistics. Certainly when researchers carry out studies using human subject, they require statistical methods in order to perform the analysis of the data. Graphics related areas that often make use of human subjects include Virtual Reality and Human-Computer Interaction (HCI). In addition, many computer descriptions of the real world involve using various probabilities that a given action will occur. The probability that a tree limb will branch during growth or that a synthetic animal will decide to walk in a particular direction are two examples of this. Finally, some techniques for solving difficult equations make use of random numbers to estimate their solutions. An important example of this is a class of techniques known as Monte Carlo methods that are often used to determine how light propagates in an environment. These are just a few of the ways that probability and statistics are used in computer graphics.

12) COMPUTATIONAL GEOMETRY - АЛГОРИТМЫ И СТРУКТУРЫ ДАННЫХ ДЛЯ CG

    Computational geometry is the study of efficient ways to represent and manipulate geometry within the computer. Typical problems include testing whether two objects collide, deciding how to break up a polygon into triangles, and finding the nearest point in a group to a given location. This area is a blend of algorithms, data structures and mathematics. Researchers in graphics who work on creating shapes (modeling) draw heavily upon this area.

    BOOK RECOMMENDATIONS

        Computational Geometry in C
        Joseph O'Rourke
        Cambridge University Press
        [undergraduate text]

        Computational Geometry: An Introduction
        Franco Preparata and Michael Shamos
        Springer-Verlag
        [the classic text, somewhat dated]

13) ТЕОРМЕХ

    https://library.bmstu.ru/Pages/Edu/Books/1kurs/2semestr/teoreticheskaya_mehanika
    https://ru.wikipedia.org/wiki/Теоретическая_механика


CONCLUDING WORDS: APPLIED AND PURE MATHEMATICS

One common thread to many of the mathematical topics that are associate with graphics is that they are from the applied side instead of the theoretical side of mathematics. This should not come as a surprise. Many of the problems in computer graphics are closely tied to problems that physicists and engineers have studied, and the mathematical tools of the physicist and of the engineer are overwhelmingly the tools that graphics researchers use. Most of the topics that make up theoretical ("pure") mathematics are seldom put to use in computer graphics. This should not be taken as an absolute truth, however. We should pay attention to examples from other fields: molecular biology is now drawing upon knot theory for the study of DNA dynamics, and subatomic physics makes use of abstract group theory. Who can tell when a "pure" mathematics topic will be put to use in computer graphics?

There are a few areas of mathematics that seem as though they ought to be important and yet never really play a large part in computer graphics. Perhaps the most interesting of these areas is __TOPOLOGY__. The usual one-sentence description of topology is the study of why a doughnut and a coffee cup are the same. The answer is that they are both surfaces with one hole. Here we are talking about ideas from topology. Aren't surfaces a big part of computer graphics? Yes, but it turns out that most of the ideas in topology that are useful to graphics can be learned in a first course in differential geometry. Differential geometry studies the *shapes* of surfaces, whereas topology studies things such as which parts of a surface are next to which other parts. I have seen very little topology that is put to use in graphics, and I believe that this is because much of topology is concerned with rather abstract sets, and that much of topology is far removed from the concepts in three dimensional Euclidean space that is so central to most of graphics. There are times when the formalism of topology (the symbolic notation) is a convenient way to express ideas in graphics, but the actual tools from abstract topology so seldom play a role in graphics. Study this beautiful subject for its own sake, but don't expect an immediate payoff for graphics!

I have been asked a few times whether either __ABSTRACT ALGEBRA__ (group theory, rings, etc.) or __NUMBER THEORY__ play a role in computer graphics. Not much that I have seen. These subjects, like topology, are areas that are full of beautiful ideas. Unfortunately these ideas seldom find their way into computer graphics.
