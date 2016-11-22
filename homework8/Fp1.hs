head' (x:xs) = x

tail' [] = []
tail' (x:xs) = xs

take' 0 xs = []
take' n xs = head' xs : take' (n - 1) (tail' xs)

drop' 0 xs = xs
drop' n [] = []
drop' n xs = drop' (n - 1) (tail' xs)

filter' f [] = []
filter' f xs | f (head' xs) = (head' xs):filter' f (tail' xs) | otherwise = filter' f (tail' xs)

foldl' (f) n [] = n
foldl' (f) n xs = foldl' (f) next_n (tail' xs) where
    next_n = (f) n (head' xs)

concat' [] ys = ys
concat' xs ys = (head' xs):(concat' (tail' xs) ys)

quickSort' [] = []
quickSort' [x] = [x]
quickSort' xs =  quickSort' lesser `concat'` equal `concat'` quickSort' greater where
    lesser = filter (< pivot) xs
    equal = filter (== pivot) xs
    greater = filter (> pivot) xs
    pivot = head' xs
    
    
