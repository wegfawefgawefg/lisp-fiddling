(define (sqrt n)
    (define (square x)
        (* x x))
    (define (improve guess)
        (/ (+ guess (/ n guess)) 2))
    (define (is_good_enough guess)
        (< (abs (- n (square guess))) 0.0001 ))
    (define (is_good_enough_2 guess last_guess)
        (< (abs (- guess last_guess)) 0.0001 ))
    (define (sqrt_iter guess last_guess)
        (if (is_good_enough_2 guess last_guess) guess
            (sqrt_iter (improve guess) guess)))
    (sqrt_iter 1 2))

(display (sqrt 2))
(newline)