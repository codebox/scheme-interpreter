import sys, re

def tokenise(txt):
	tokens = []
	token = None

	for c in txt:
		if c.isspace():
			tokens.append(token)
			token = None

		elif c == '(' or c == ')' or c == '\n':
			tokens.append(token)
			tokens.append(c)
			token = None

		else:
		 	if token == None:
		 		token = ''
		 	token += c

	tokens.append(token)

	return [t for t in tokens if t != None]

def read_list(tokens, context):
	tree = []
	token, remainder = tokens[0], tokens[1:]

	if token != '(':
		raise ValueError('not a list')

	while remainder:
		token, remainder = remainder[0], remainder[1:]
		if token == '(':
			t, remainder = parse_statement([token] + remainder, context)
			tree.append(t)

		elif token == ')':
			return (tree, remainder)

		else:
			tree.append(token)

	raise ValueError('missing closing bracket')

def parse_statement(tokens, context):
	try:
		return (float(tokens[0]), tokens[1:])
	except ValueError:
		pass

	try:
		return read_list(tokens, context)
	except ValueError:
		pass

	if tokens[0] == '\n':
		return (None, tokens[1:])

	if context.has_key(tokens[0]):
		return (context[tokens[0]], tokens[1:])

	raise ValueError('unable to parse ' + str(tokens))

def makeReduce(fn_op):
	return lambda l, context : reduce(fn_op, [eval(a, context) for a in l])

def cons(l, context):
	return [eval(i, context) for i in l]

def car(l, context):
	if len(l) != 1:
		raise Exception('car expects a single list argument')

	return eval(l[0], context)[0]

def cdr(l, context):
	if len(l) != 1:
		raise Exception('cdr expects a single list argument')

	return eval(l[0], context)[1:]

def cond(l, context):
	if len(l) not in [2,3]:
		raise Exception('if expects either 2 or 3 arguments')

	if eval(l[0], context):
		return eval(l[1], context)
	elif len(l) == 3:
		return eval(l[2], context)

def gt(l, context):
	if len(l) != 2:
		raise Exception('> expects 2 arguments')

	return eval(l[0], context) > eval(l[1], context)

def lt(l, context):
	if len(l) != 2:
		raise Exception('< expects 2 arguments')

	return eval(l[0], context) < eval(l[1], context)

def eq(l, context):
	if len(l) != 2:
		raise Exception('= expects 2 arguments')
	result = eval(l[0], context) == eval(l[1], context)
	return result

def define(l, context):
	if len(l) != 2:
		raise Exception('define expects 2 arguments')

	name  = l[0]
	value = l[1]
	context[name] = value
	return None

def make_lambda(l, context):
	if len(l) != 2:
		raise Exception('lambda expects 2 arguments')

	params = l[0]
	body   = l[1]
	def lambda_fn(args):
		arg_dict = dict(zip(params, args))
		local_context = dict(context.items() + arg_dict.items())
		return eval(body, local_context)
	
	return lambda_fn
	
operators = {
	'+' : makeReduce(lambda x,y : x + y),
	'-' : makeReduce(lambda x,y : x - y),
	'*' : makeReduce(lambda x,y : x * y),
	'/' : makeReduce(lambda x,y : x / y),
	'>' : gt,
	'<' : lt,
	'=' : eq,
	'cons' : cons,
	'car'  : car,
	'cdr'  : cdr,
	'if'   : cond,
}

def is_number(txt):
	try:
		float(txt)
		return True
	except:
		return False

def is_function(n):
	return hasattr(n, '__call__')
		
def define(args, context):
	if len(args) != 2:
		raise Exception('define expects 2 arguments')

	name = args[0]
	value = eval(args[1], context)
	context[name] = value

def eval(item, context):
	if isinstance(item, list):
		op, args = item[0], item[1:]

		if op == 'define':
			return define(args, context)

		elif op == 'lambda':
			return make_lambda(args, context)

		elif op in context and is_function(context[op]):
			evaled_args = [eval(arg, context) for arg in args]
			return context[op](evaled_args)
			
		elif op not in operators:
			raise Exception('Unknown operator: ' + op)

		return operators[op](args, context)

	elif is_number(item):
		return float(item)
		
	elif item != None:
		if item in context:
			return eval(context[item], context)
		else:
			raise Exception('unknown variable: ' + item)

if __name__ == '__main__':
	context = {}
	tokens = tokenise(open(sys.argv[1]).read())
	while tokens:
		tree, tokens = parse_statement(tokens, context)
		result = eval(tree, context)	
		if result != None:
			print result
