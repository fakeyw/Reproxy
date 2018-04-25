class DA(object):
	__slots__ = ('__local', '__dict__', '__name__', '__wrapped__')
	
	def __init__(self,src,dict):
		object.__setattr__(self,'s',src)
		attr_list = []
		for k,v in dict.items():
			object.__setattr__(self,k,v)
			attr_list.append(k)
		object.__setattr__(self,'attr_list',attr_list)
	
	@property
	def __dict__(self):
		try:
			return self.s.__dict__
		except RuntimeError:
			raise AttributeError('__dict__')

	def __repr__(self):
		try:
			obj = self.s
		except RuntimeError:
			return '<%s unbound>' % self.__class__.__name__
		return repr(obj)

	def __bool__(self):
		try:
			return bool(self.s)
		except RuntimeError:
			return False

	def __unicode__(self):
		try:
			return unicode(self.s)  # noqa
		except RuntimeError:
			return repr(self)

	def __dir__(self):
		try:
			return dir(self.s)
		except RuntimeError:
			return []

	def __delitem__(self, key):
		del self.s[key]
	
	def __getattr__(self,name):
		return getattr(self.s,name)
		
	#def __setattr__(self,name,value):
	#	setattr(self.s,name,value)

	def __enter__(self):
		pass
		
	def __exit__(self,a,b,c):
		pass
	
	def __str__(self):
		return "Secured "+str(self.s)
		
	def __setattr__(self,k,v):
		if k in object.__getattr__(self,'attr_list'):
			object.__setattr__(self,'uuid',v)
		else:
			setattr(self.s,k,v)
		
	#__setattr__ = lambda x, n, v: setattr(x.s, n, v)
	__delattr__ = lambda x, n: delattr(x, n)
	__lt__ = lambda x, o: x.s < o
	__le__ = lambda x, o: x.s <= o
	__eq__ = lambda x, o: x.s == o
	__ne__ = lambda x, o: x.s != o
	__gt__ = lambda x, o: x.s > o
	__ge__ = lambda x, o: x.s >= o
	__cmp__ = lambda x, o: cmp(x.s, o)  # noqa
	__hash__ = lambda x: hash(x.s)
	__call__ = lambda x, *a, **kw: x.s(*a, **kw)
	__len__ = lambda x: len(x.s)
	__getitem__ = lambda x, i: x.s[i]
	__setitem__ = lambda x, i, v: x.s.__setitem__(i,v)
	__iter__ = lambda x: iter(x.s)
	__contains__ = lambda x, i: i in x.s
	__add__ = lambda x, o: x.s + o
	__sub__ = lambda x, o: x.s - o
	__mul__ = lambda x, o: x.s * o
	__floordiv__ = lambda x, o: x.s // o
	__mod__ = lambda x, o: x.s % o
	__divmod__ = lambda x, o: x.s.__divmod__(o)
	__pow__ = lambda x, o: x.s ** o
	__lshift__ = lambda x, o: x.s << o
	__rshift__ = lambda x, o: x.s >> o
	__and__ = lambda x, o: x.s & o
	__xor__ = lambda x, o: x.s ^ o
	__or__ = lambda x, o: x.s | o
	__div__ = lambda x, o: x.s.__div__(o)
	__truediv__ = lambda x, o: x.s.__truediv__(o)
	__neg__ = lambda x: -(x.s)
	__pos__ = lambda x: +(x.s)
	__abs__ = lambda x: abs(x.s)
	__invert__ = lambda x: ~(x.s)
	__complex__ = lambda x: complex(x.s)
	__int__ = lambda x: int(x.s)
	__long__ = lambda x: long(x.s)  # noqa
	__float__ = lambda x: float(x.s)
	__oct__ = lambda x: oct(x.s)
	__hex__ = lambda x: hex(x.s)
	__index__ = lambda x: x.s.__index__()
	__coerce__ = lambda x, o: x.s.__coerce__(x, o)
	#__enter__ = lambda x: x.__enter__()
	#__exit__ = lambda x, *a, **kw: x.__exit__(*a, **kw)
	__radd__ = lambda x, o: o + x.s
	__rsub__ = lambda x, o: o - x.s
	__rmul__ = lambda x, o: o * x.s
	__rdiv__ = lambda x, o: o / x.s
	__rfloordiv__ = lambda x, o: o // x.s
	__rmod__ = lambda x, o: o % x.s
	__rdivmod__ = lambda x, o: x.s.__rdivmod__(o)
	__copy__ = lambda x: copy.copy(x.s)
	__deepcopy__ = lambda x, memo: copy.deepcopy(x.s, memo)