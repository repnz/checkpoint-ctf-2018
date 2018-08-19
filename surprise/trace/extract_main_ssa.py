from parse import parse, compile


def first(lst, start_index, predicate):
    while start_index < len(lst):
        if predicate(lst[start_index]):
            return start_index
        start_index += 1

    return -1


def find_contains(lst, start_index, item):
    return first(lst, start_index, lambda line: item in line)


def find_startswith(lst, start_index, item):
    return first(lst, start_index, lambda line: line.startswith(item))


def extract_main_trace():
    ssa_lines = open('trace.ssa').readlines()  # Read SSA Dump
    main_lines = []

    current_index = find_startswith("Starting main.main", 0, ssa_lines)

    while current_index < len(ssa_lines):
        # Look For A Function Call
        next_starting_index = find_startswith("Starting", current_index + 1, ssa_lines)

        # If it is the end of the trace
        if next_starting_index == -1:
            main_lines += ssa_lines[current_index:]
            break

        # If this is an in package function
        if 'Starting main.' in ssa_lines[next_starting_index]:
            main_lines += ssa_lines[current_index:next_starting_index]
            current_index = next_starting_index
            continue

        # Add the main() lines
        main_lines += ssa_lines[current_index:next_starting_index]

        # Look For The Return To Main
        current_index = find_startswith("proceeding main.", next_starting_index + 1, ssa_lines)

    print ''.join(main_lines)


class SSACodePart(object):
    def __init__(self, function_name, id, code_lines):
        self.id = id
        self.function_name = function_name
        self.code_lines = code_lines

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return '.' + str(self.id) + ':\n' + ''.join(self.code_lines)+"\n"


class SSAFunction(object):
    def __init__(self, name, code_parts, source_start, calls_count):
        self.name = name
        self.var_name = self.name[self.name.index('.')+1:]
        self.code_parts = code_parts
        self.source_start = source_start
        self.calls_count = calls_count

    def get_missing_parts(self):
        if self.code_parts[-1].id is None:
            return []

        current_id = 0
        missing = []

        for p in self.code_parts:
            while int(p.id) != current_id:
                missing.append(int(current_id))
                current_id += 1

            current_id += 1

        return missing

    def __str__(self):
        code = ''.join(map(str, self.code_parts))

        for i in xrange(1000, -1, -1):
            code = code.replace('t'+str(i), self.var_name+str(i)+'_')

        return "func {name} at {source_line}; called {calls_count};\n{code}".format(
            name=self.name,
            source_line=self.source_start,
            calls_count=self.calls_count,
            code=code
        )


class SSAFunctionInstance(object):
    def __init__(self, function_name, start_line, end_line, inner_calls, source_line, code_parts):
        self.source_line = source_line
        self.function_name = function_name
        self.code_parts = code_parts
        self.start_line = start_line
        self.end_line = end_line
        self.inner_calls = inner_calls

    def __str__(self):
        return "func {name} [{start_line}, {end_line}, {source_line}]\n{code}".format(
            name=self.function_name,
            start_line=self.start_line,
            end_line=self.end_line,
            source_line=self.source_line,
            code=''.join(map(str, self.code_parts))
        )


    @staticmethod
    def extract_starting_fields(starting_line):
        result = parse(
            format='Starting {function} at {source_line}.',
            string=starting_line
        )

        if result is not None:
            return result['function'], result['source_line']

        return parse(
            format='Starting {function}.',
            string=starting_line
        )['function'], None


    @staticmethod
    def extract_returning_fields(returning_line):
        result = parse(
            format='Returning from {old_function}, proceeding {current_function} at {source_line}.',
            string=returning_line
        )

        return result['old_function'], result['current_function'], result['source_line']

    @staticmethod
    def parse(lst, index=0):
        function_name, source_line = SSAFunctionInstance.extract_starting_fields(lst[index])
        start_line = index
        inner_calls = []
        code_parts = []

        if index == -1:
            raise Exception("Parse exception: Missing start")

        index += 1
        code_part_start_index = index+1
        code_part_id = None
        current_code_part = []

        while index < len(lst):
            if lst[index].startswith('.'):
                new_code_part_id = int(parse('.{}:', lst[index])[0])

                if new_code_part_id != 0:
                    if code_part_id is None:
                        raise Exception("Missing 0 code part")

                    prev_code_part = SSACodePart(function_name, code_part_id,
                                                 current_code_part + lst[code_part_start_index:index])
                    code_parts.append(prev_code_part)
                    code_part_start_index = index+1
                    code_part_id = new_code_part_id
                    current_code_part = []
                else:
                    code_part_id = 0

            elif lst[index].startswith('Starting'):
                current_code_part += lst[code_part_start_index:index]
                inner_instance = SSAFunctionInstance.parse(lst, index)
                inner_calls.append(inner_instance)
                code_part_start_index = inner_instance.end_line+1
                index = code_part_start_index
                continue

            elif lst[index].startswith('Returning'):
                prev_code_part = SSACodePart(function_name, code_part_id,
                                             current_code_part + lst[code_part_start_index:index])
                code_parts.append(prev_code_part)
                break

            index += 1

        return SSAFunctionInstance(
            function_name=function_name,
            start_line=start_line,
            end_line=index,
            inner_calls=inner_calls,
            source_line=source_line,
            code_parts=code_parts
        )


def print_func(f):
    print str(f)
    print
    for inner_func in f.inner_calls:
        print_func(inner_func)


def extract_functions():
    code_lines = open('trace.ssa').readlines()
    main_init = SSAFunctionInstance.parse(code_lines)
    main_main = SSAFunctionInstance.parse(code_lines, main_init.end_line + 1)

    function_keys = []
    function_instances_dict = {}
    vertex = [main_main, main_init]

    while vertex:
        f = vertex.pop()

        if f.function_name in function_instances_dict:
            function_instances_dict[f.function_name].append(f)
        else:
            function_keys.append(f.function_name)
            function_instances_dict[f.function_name] = [f]

        for child in reversed(f.inner_calls):
            vertex.append(child)

    functions = []

    for function_name in function_keys:
        function_instances = function_instances_dict[function_name]

        code_parts = set()

        for function_instance in function_instances:
            for part in function_instance.code_parts:
                code_parts.add(part)

        functions.append(SSAFunction(
            name=function_name,
            source_start=function_instances[0].source_line,
            code_parts=list(sorted(code_parts, key=lambda part: part.id)),
            calls_count=len(function_instances)
        ))

    return functions


def main():
    functions = extract_functions()

    for func in functions:
        print func.name, func.source_start
        print


if __name__ == '__main__':
    main()
