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
		return self.right != None and self.left != None
			


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
		while max.right.is_real_node():
			max = max.right
		while max.parent != None and max.key > key:
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
		path_len = 0
		# if tree is empty
		if self.root == None:
			virtual_left_node = AVLNode(-1, -1)
			virtual_right_node = AVLNode(-1, -1)
			self.root = new_node
			self.root.right = virtual_right_node
			self.root.left = virtual_left_node
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
		new_node.parent = parent
		# do requied rotations
		h=0
		while parent != None:
			BF_parent = parent.BF()
			abs_BF = abs(BF_parent)
			old_height = parent.height
			parent.update_height()
			if abs_BF < 2 and parent.height== old_height:
				h+=1
				break
			elif abs_BF < 2 and parent.height!= old_height:
				parent = parent.parent
			else:
				right_BF = parent.right.BF()
				if BF_parent == -2 :
					if right_BF == -1:
						parent.left_rotation()
					elif right_BF == 1:
						parent.right_left_rotation()
				left_BF = parent.left.BF()
				if BF_parent == 2:
					if left_BF == -1:
						parent.left_right_rotation()
					elif left_BF == 1:
						parent.right_rotation()
				break
		return new_node, path_len, h
	


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
		max = self.root
		path_len = 0
		while max.right.is_real_node():
			max = max.right
		while max.parent != None and max.key > key:
			max = max.parent
			path_len += 1
		res = max.insert(key, val)
		return res[0], res[1] + path_len, res[2]


	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	"""
	def delete(self, node):
		# do deletion as bst
		parent = node.bst_deletion()
		# do requied rotations
		while parent != None:
			BF_parent = parent.BF()
			abs_BF = abs(BF_parent)
			old_height = parent.height
			parent.update_height()
			if abs_BF < 2 and parent.height== old_height:
				break
			elif abs_BF < 2 and parent.height!= old_height:
				parent = parent.parent
			else:
				right_BF = parent.right.BF()
				if BF_parent == -2 :
					if right_BF == -1 or right_BF == 0 :
						parent.left_rotation()
					elif right_BF == 1:
						parent.right_left_rotation()
				left_BF = parent.left.BF()
				if BF_parent == 2:
					if left_BF == -1:
						parent.left_right_rotation()
					elif left_BF == 1 or left_BF == 0:
						parent.right_rotation()
						parent = parent.parent 
				
		
			

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
		new_node = AVLNode(key, val)
		tree = self.root
		if val > tree2.root.val:
			new_node.left = tree2
			tree2.parent = new_node
			while tree.height > tree2.height:
				tree = tree.left
			new_node.right = tree
			new_node.parent = tree.parent
			tree.parent = new_node
			new_node.parent.left = new_node
			new_node.update_height()
			if new_node.parent.BF() == 2:
				new_node.parent.right_rotation()
		else:
			new_node.right = tree2
			tree2.parent = new_node
			while tree.height > tree2.height:
				tree = tree.right
			new_node.left = tree
			new_node.parent = tree.parent
			tree.parent = new_node
			new_node.parent.right = new_node
			new_node.update_height()
			if new_node.parent.BF() == -2:
				new_node.parent.right_rotation()
		
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


	def find_successor(self):
		p = self
		if self.right == None:
			while (p == p.parent.right):
				p = p.parent
			return p.parent
		else:
			p = p.right
			while (p.left.is_real_node()):
				p = p.left
		return p
	

	def bst_deletion(self):
		right = self.right
		left = self.left
		parent = self.parent
		if not right.is_real_node() and not left.is_real_node():
			vr_node = AVLNode(-1,-1)
			if parent.right == self:
				parent.right = vr_node
			if parent.left == self:
				parent.left = vr_node
			return parent
		elif right.is_real_node() and not left.is_real_node():
			parent.right = right
			right.parent = parent
			return parent
		elif not right.is_real_node() and left.is_real_node():
			parent.left = left
			left.parent = parent
			return parent
		else:
			successor = self.find_successor()
			successor.right.parent = successor.parent
			successor.parent.left = successor.right
			parent = successor.parent
			if self.parent.right == self:
				self.parent.right = successor
			else:
				self.parent.left = successor
			successor.parent = self.parent
			successor.right = self.right
			successor.left = self.left
			successor.left.parent = successor
			successor.right.parent = successor
			return parent



		
			
			
	#calculate the BF of a given node
	def BF(self):
		return self.left.height - self.right.height
	#check if the height of a node has changed
	def has_height_changed(self):
		rh = self.right.height
		lh = self.left.height
		new_height = 1 + max(rh, lh)
		return new_height != self.height
	#update height of a node

	def update_height(self):
		rh = self.right.height
		lh = self.left.height
		self.height = 1 + max(rh, lh)
	#do a right rotation
	def right_rotation(self):
		left_subtree = self.left
		self.left = left_subtree.right
		self.left.parent = self
		left_subtree.right = self
		left_subtree.parent = self.parent
		if self.parent.right == self:
			left_subtree.parent.right = left_subtree
		else:
			left_subtree.parent.left = left_subtree
		self.parent = left_subtree
	#do a left rotation
	def left_rotation(self):
		right_subtree = self.right
		self.right = right_subtree.left
		self.right.parent = self
		right_subtree.left = self
		right_subtree.parent = self.parent
		if self.parent.right == self:
			right_subtree.parent.right = right_subtree
		else:
			right_subtree.parent.left = right_subtree
		self.parent = right_subtree
	def left_right_rotation(self):
		self.left.left_rotation()
		self.right_rotation()
	def right_left_rotation(self):
		self.right.right_rotation()
		self.left_rotation()
		


