from pyang.grammar import stmt_map
from datetime import datetime
from common import yang_to_dict
from string import Template
from random import randint  # @UnusedImport
from pprint import pprint  # @UnusedImport

template = {
'import': """module ${module_name} {
    namespace "test:${module_name}";
    prefix test;

    revision ${date};

    identity my-identity {
        status current;
        description "identity-description-string2";
        reference "identity-reference-string2";
    }

    feature my-feature {
        status current;
        description "feature-description-string2";
        reference "feature-reference-string2";
    }

    rpc my-rpc {
    }

    grouping my-grouping {
    }
}
""",

'include': """submodule ${module_name} {
    belongs-to "module-identifier0" {
        prefix test;
    }

    revision ${date};
}
"""}

def indent(txt, level):
    return ' ' * level * 2 + txt

def convert_substmt_to_yang(substmt, parent):
    lines = []
    name = substmt[0]
    if name == '$interleave':
        ss_list = substmt[1]
        for ss in ss_list:
            lines += convert_substmt_to_yang(ss, parent)
    elif name == '$choice':
        cases_list = substmt[1]
        ss_list = cases_list[1]
        for ss in ss_list:
            lines += convert_substmt_to_yang(ss, parent)
#         for cases in cases_list:
    else:
#         occurrence = substmt[1]
        if parent.count(name) < max_nested_count:
            lines += convert_stmt_to_yang(name, parent)
    return lines

def convert_stmt_to_yang(statement, parent):
    lines = []

    if check_supported:
        if not statement in supported_statement:
            return lines
    else:
        if statement in unsupported_statement:
            return lines

    indent_level = len(parent)
    level = str(indent_level)

    stmt = stmt_map[statement]
    arg_type = stmt[0]
    substmts = stmt[1]

    identity_ref = {'base': 'prefix-identifier2:my-identity',
     'if-feature': 'prefix-identifier2:my-feature',
     'type': 'string',
     'uses': 'prefix-identifier2:my-grouping'}

    stmt_arg_lvl = statement + '-' + str(arg_type) + level

    if parent:
        parent_stmt_arg_lvl = '"' + parent[-1] + '-' + stmt_arg_lvl + '"'

    def f(lst, idx):
        return lst[idx % len(lst)]

    arg_type_map = {
        "_comment": lambda x: f(["//Comment", "/*Comment*/"], x),
        "absolute-schema-nodeid": lambda x: "/prefix-identifier2:my-rpc",
        "boolean": lambda x: f(['true', 'false'], x),
        "date": lambda x: '"' + datetime.now().strftime("%Y-%m-%d") + '"',
        "descendant-schema-nodeid": lambda x: "prefix-identifier2:my-container",
        "deviate-arg": lambda x: f(['not-supported', 'add', 'delete', 'replace'], x),
        "enum-arg": lambda x: parent_stmt_arg_lvl,
        "fraction-digits-arg": lambda x: f(['1'], x),
        "identifier": lambda x: stmt_arg_lvl,
        "identifier-ref": lambda x: identity_ref[statement],
        "integer": lambda x: f(['100', '0', '-100'], x),
        "key-arg": lambda x: 'leaf-identifier' + level,
        "length-arg": lambda x: f(['"1..255"', '"11 | 42..max"'], x),
        "max-value": lambda x: f(['1', '2'], x),
        "non-negative-integer": lambda x: f(['100', '0'], x),
        "ordered-by-arg": lambda x: f(['user', 'system'], x),
        "path-arg": lambda x: f(['absolute-path', 'relative-path'], x),
        "range-arg": lambda x: f(['"1..4 | 10..20"', '"11..max"'], x),
        "schema-nodeid": lambda x: "/prefix-identifier2:my-rpc",
        "status-arg": lambda x: f(['current', 'obsolete', 'deprecated'], x),
        "string": lambda x: parent_stmt_arg_lvl,
        "unique-arg": lambda x: 'leaf-identifier' + level,
        "uri": lambda x: parent_stmt_arg_lvl.replace('-', ':'),
        "version": lambda x: '1',
        None: lambda x: '',}

    if len(substmts) > 0:
        line_end = ' {'
    else:
        line_end = ';'

    idx = 0  # randint(1, 10)
    line = statement + ' ' + arg_type_map[arg_type](idx) + line_end
    lines.append(indent(line, indent_level))

    for substmt in substmts:
        lines += convert_substmt_to_yang(substmt, parent + [statement])

    if len(substmts) > 0:
        lines.append(indent('}', indent_level))

    # Resolve dependencies
    if statement in ['import', 'include']:
        module_name = stmt_arg_lvl
        params =  {'module_name' : module_name,
                  'date' : datetime.now().strftime ("%Y-%m-%d")}
        yang_txt = Template(template[statement]).substitute(params)
        filename = module_name + ".yang"
        open(filename, 'w').write(yang_txt)

    return lines

def auto_generate_yang(top_stmt, yang_file):
    print "[INFO] Generating YANG file " + yang_file + "..."
    lines = convert_stmt_to_yang(top_stmt, [])
    yang_txt = "\r".join(lines)
    open(yang_file, 'w').write(yang_txt)

    print "[INFO] Verifying YANG file..."
    yang_to_dict(yang_file)

    print "[INFO] Done."

def main():
    global max_nested_count
    global check_supported
    global supported_statement
    global unsupported_statement

    # --------------------- User Configuration ---------------------------------

    max_nested_count = 1  # Range 1 - 3
    check_supported = False  # True or False

    # If check_supported is True
    supported_statement = ['module', 'leaf', 'namespace', 'prefix', 'type',
                           'container', 'yang-version', 'list', 'key']

    # If check_supported is False
    unsupported_statement = ['$cut', 'grouping', 'typedef', 'unique', 'config',
                             'default', 'choice', 'augment', 'uses']

    auto_generate_yang('module', 'module-identifier0.yang')

#     max_nested_count = 2  # Range 1 - 3
#     check_supported = True  # True or False
#     auto_generate_yang('module', 'Testcase002.yang')

# pprint(stmt_map)
main()

