<p>
This is an interpreter for a sub-set of the Scheme programming language. It was written as a learning exercise, and should not be used in any situation where correctness, efficiency or elegance are considered to be important. If none of these factors are of concern, then you may certainly use it for any purpose - what's the worst that could happen?
</p>
<p>
The interpreter supports basic arithmetic and equality operators, conditional statements, the `cons`/`car`/`cdr` list operations, `define` and `lambda`. Some working code examples are shown below.
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