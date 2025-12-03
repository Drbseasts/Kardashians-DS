#id1:
#name1:
#username1:
#id2:
#name2:
#username2:


"""A class represnting a node in an AVL tree"""

class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 
	
	@type key: int
	@param key: key of your node
	@type value: string
	@param value: data of your node
	"""
	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		self.height = -1
		

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		return False


"""
A class implementing an AVL tree.
"""

class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.
	"""
	def __init__(self):
		self.root = None


	"""searches for a node in the dictionary corresponding to the key (starting at the root)
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def search(self, key):
		path_len = 1
		tree = self.root
		while(tree.is_real_node()):
			if tree.key < key:
				tree = tree.left
			elif tree.key > key:
				tree = tree.right
			else:
				return tree,path_len
			path_len += 1
		return None, -1


	"""searches for a node in the dictionary corresponding to the key, starting at the max
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def finger_search(self, key):
		max = self.root
		path_len = 0
		while (max.right.is_real_node()):
			max = max.right
		while(max.parent != None and max.key > key):
			max = max.parent
			path_len += 1
		node, search_len = max.search(key)
		tot_len = -1 if search_len == -1 else search_len + path_len
		return node, tot_len


	"""inserts a new node into the dictionary with corresponding key and value (starting at the root)

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def insert(self, key, val):
		new_node = AVLNode(key,val)
		new_node.height = 0
		path_len = 1
		# if tree is empty
		if self.root == None:
			self.root = new_node
			return (new_node , 0, 1)
		# insert node as BST
		tree = self.root
		while tree.is_real_node():
			parent = tree
			if key < tree.key :
				tree = tree.left
			elif key > tree.key:
				tree = tree.right
			path_len += 1
		if key < parent.key:
			parent.left = new_node
		if key > parent.key:
			parent.right = new_node
		
		while parent != None:
			abs_BF = abs(BF(parent))
			old_height = parent.height
			update_height(parent)
			if abs_BF < 2 and parent.height== old_height:
				break
			elif abs_BF < 2 and parent.height!= old_height:
				parent = parent.parent
			else:


			


	"""inserts a new node into the dictionary with corresponding key and value, starting at the max

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def finger_insert(self, key, val):
		return None, -1, -1


	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	"""
	def delete(self, node):
		return	

	
	"""joins self with item and another AVLTree

	@type tree2: AVLTree 
	@param tree2: a dictionary to be joined with self
	@type key: int 
	@param key: the key separting self and tree2
	@type val: string
	@param val: the value corresponding to key
	@pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
	or the opposite way
	"""
	def join(self, tree2, key, val):
		return


	"""splits the dictionary at a given node

	@type node: AVLNode
	@pre: node is in self
	@param node: the node in the dictionary to be used for the split
	@rtype: (AVLTree, AVLTree)
	@returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
	dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
	dictionary larger than node.key.
	"""
	def split(self, node):
		return None, None

	
	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):
		return None


	"""returns the node with the maximal key in the dictionary

	@rtype: AVLNode
	@returns: the maximal node, None if the dictionary is empty
	"""
	def max_node(self):
		return None

	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self):
		return -1	


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return None



#calculate the BF of a given node
def BF(node):
	return node.left.height - node.right.height
#check if the height of a node has changed
def has_height_changed(node):
	rh = node.right.height
	lh = node.left.height
	new_height = 1 + max(rh, lh)
	return new_height != node.height
#update height of a node
def update_height(node):
	rh = node.right.height
	lh = node.left.height
	node.height = 1 + max(rh, lh)
#do a right rotation
def right_rotation(tree):
	left_subtree = tree.left
	tree.left = left_subtree.right
	tree.left.parent = tree
	left_subtree.right = tree
	left_subtree.parent = tree.parent
	if tree.parent.right == tree:
		left_subtree.parent.right = left_subtree
	else:
		left_subtree.parent.left = left_subtree
	tree.parent = left_subtree
#do a left rotation
def left_rotation(tree):
	right_subtree = tree.right
	tree.right = right_subtree.left
	tree.right.parent = tree
	right_subtree.left = tree
	right_subtree.parent = tree.parent
	if tree.parent.right == tree:
		right_subtree.parent.right = right_subtree
	else:
		right_subtree.parent.left = right_subtree
	tree.parent = right_subtree