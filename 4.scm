
(define (fact_iter n)
    (fact_iter_inner 1 1 n))
(define (fact_iter_inner acc depth target_depth)
    (if (> depth target_depth) acc
        (fact_iter_inner (* acc depth) (+ depth 1) target_depth)))

(display (fact_iter 3))(newline)