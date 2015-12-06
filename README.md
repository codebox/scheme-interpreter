<p>
This is an interpreter for a sub-set of the Scheme programming language. It was written as a learning exercise, and should not be used for anything important.
</p>
<p>
To use the interpreter, write your Scheme code into a text file and run <code>scheme.py</code>, passing the file name and location as a
command-line argument, for example:
</p>

<pre>
python scheme.py mycode.txt
</pre>

<p>
The interpreter supports basic arithmetic and equality operators, conditional statements, the <code>cons</code>/<code>car</code>/<code>cdr</code>
list operations, <code>define</code> and <code>lambda</code>.
</p>
<p>
Each statement in the source file will be evaluated in turn, and any printable results will be displayed to standard output. A couple of
working Scheme programs and their resulting output are shown below:
</p>

<pre>
(define factorial (
    lambda (n) (
        if (= n 1) 
            1 
            (* n (factorial (- n 1)))
        )
    )
)
(factorial 6)
</pre>
<pre>
720.0
</pre>
<p>&nbsp;</p>
<pre>
(define fib (
    lambda (n) (
        if (&lt; n 3)
            1
            (+ (fib (- n 1)) (fib (- n 2)))
        )
    )
)
(fib 10)
</pre>
<pre>
55.0
</pre>
