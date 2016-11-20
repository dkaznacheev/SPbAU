head' (x:xs) = x
tail' [] = []
tail' (x:xs) = xs
take' 0 xs = []
take' n (x:xs) = x:(take' (n - 1) xs)
drop' 0 xs = xs
drop' n [] = []
drop' n (x:xs) = drop' (n - 1) xs
filter' f [] = []
filter' f (x:xs) | f x = x:(filter' f xs) | otherwise = filter' f xs
foldl' (f) n [] = n
foldl' (f) n xs = foldl' (f) (f n (head' xs)) (tail' xs)
concat' [] ys = ys
concat' xs ys = (head' xs):(concat' (tail' xs) ys)
quickSort' [] = []
quickSort' [x] = [x]
quickSort' xs =  (quickSort' (filter (< pivot xs) xs)) 
                 `concat'` ((filter (== pivot xs) xs)) 
                 `concat'` quickSort'((filter (> pivot xs) xs)) where
    len [] = 0
    len xs = 1 + len (tail' xs)
    pivot xs = head' (drop' ((len xs) `div` 2) xs)
    
    
