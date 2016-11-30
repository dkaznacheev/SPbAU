import Prelude hiding (lookup)

data BinaryTree k v = Nil | Node k v (BinaryTree k v) (BinaryTree k v) deriving (Show, Eq)

insert :: Ord k => k -> v -> BinaryTree k v -> BinaryTree k v
insert k v Nil = Node k v Nil Nil
insert k v (Node nk nv left right) 
    | k == nk = Node nk v left right
    | k < nk = Node nk nv (insert k v left) right
    | k > nk = Node nk nv left (insert k v right)

lookup :: Ord k => k -> BinaryTree k v -> Maybe v  
lookup k Nil = Nothing
lookup k (Node nk nv left right)
    | k == nk = Just nv
    | k < nk = lookup k left
    | k > nk = lookup k right
    
delete :: Ord k => k -> BinaryTree k v -> BinaryTree k v    
delete k Nil = Nil
delete k (Node nk nv left right)
    | k == nk = rebuilt (Node nk nv left right)
    | k < nk = Node nk nv (delete k left) right
    | k > nk = Node nk nv left (delete k right)

rebuilt (Node nk nv Nil right) = right
rebuilt (Node nk nv left right) = Node lk lv left' right where
    lk = fst rleft
    lv = snd rleft
    rleft = rightest left
    left' = delete lk left
    rightest (Node nk nv _ Nil) = (nk, nv)
    rightest (Node nk nv _ right) = rightest right

