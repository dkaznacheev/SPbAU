import Prelude hiding (lookup)

data BinaryTree k v = Nil | Node k v (BinaryTree k v) (BinaryTree k v) deriving (Show, Eq)

insert Nil k v = Node k v Nil Nil
insert (Node nk nv left right) k v
    | k == nk = Node k v left right
    | k < nk = Node nk nv (insert left k v) right
    | k > nk = Node nk nv left (insert right k v)

lookup Nil k = Nothing
lookup (Node nk nv left right) k 
    | k == nk = Just nv
    | k < nk = lookup left k
    | k > nk = lookup right k

delete Nil k = Nil
delete (Node nk nv left right) k
    | k == nk = rebuilt (Node nk nv left right)
    | k < nk = Node nk nv (delete left k) right
    | k > nk = Node nk nv left (delete right k)

rebuilt (Node nk nv Nil right) = right
rebuilt (Node nk nv left right) = Node lk lv left' right where
    lk = fst rleft
    lv = snd rleft
    rleft = rightest left
    left' = delete left lk
    rightest (Node nk nv _ Nil) = (nk, nv)
    rightest (Node nk nv _ right) = rightest right

