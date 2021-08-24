(define (fact n)
    (if (<= n 1) 
        1
        (* n (fact (- n 1)))))

(display (fact 3.5))
(newline)