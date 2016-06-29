"""YANG to Java parser"""

from collections import defaultdict
from pprint import pprint
from string import Template
from template import interface, builder, package_info, parent_builder, parent_interface, child_builder, child_interface
from xml.etree import ElementTree as ET
from distutils.dir_util import copy_tree
import datetime
import difflib
import fileinput
import glob
import os
import re
import shutil
from shutil import copyfile
import webbrowser
import sys
import trace
from xml.dom.minidom import parse, parseString



def etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.iteritems():
                dd[k].append(v)
        d = {t.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.iteritems()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v) for k, v in t.attrib.iteritems())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d

def yang_to_dict(yang_file):
    os.chdir(curr_dir)
    os.system("pyang -f yin " + yang_file + "  -o temp.xml")
    with open('temp.xml', 'r') as myfile:
        xml_snippet = myfile.read().replace('\n', '')
        xml_snippet = re.sub('<\?xml version="1.0" encoding="UTF-8"\?>', '', xml_snippet)
        xml_snippet = re.sub('xmlns\S+"', '', xml_snippet)
        d = etree_to_dict(ET.XML(xml_snippet))
        pprint(d)
        return d

def traverse(parent, d):
    for k, v in d.iteritems():
        if isinstance(v, dict):
            # Traverse dictionary
            statement_builder(parent, k, v)
            traverse(parent + "/" + str(k), v)
        elif isinstance(v, list):
            # Traverse list
            for idx, val in enumerate(v):
                statement_builder(parent, str(k) + "[" + str(idx)+ "]", val)
                traverse(parent + "/" + str(k) + "[" + str(idx)+ "]", val)
        else:
            if not '@' in k:
                # Handle statements like text
                statement_builder(parent, k, v)

def get_child_names(parent, d):
    childs = []
    childs_of_container = []    
    for k, v in d.iteritems():
        if  k == 'leaf' or k == 'leaf-list':
            if isinstance(v, dict):
                childs.append(v['@name']) 
            elif isinstance(v, list):
                for idx, val in enumerate(v):
                    print idx 
                    childs.append(val['@name'])
        if  k == 'container':
            if isinstance(v, dict):
                childs_of_container.append(v['@name']) 
            elif isinstance(v, list):
                for idx, val in enumerate(v):
                    print idx 
                    childs_of_container.append(val['@name'])
    childs = childs + childs_of_container  
    return childs




def statement_builder(parent, statement, body):
    parents_count = parent.count("/")
    statement_list.append({'parent': parent,
                           'parents_count': parents_count,
                           'statement': statement,
                           'body': body})
    key = parent+"/"+statement
    assert not statement_dict.has_key(key)
    statement_dict[key] = body

def get_parents_count(item):
    return item['parents_count']

def print_statement_list(items):
    print "my items", items
    for item in items:
        print item['parents_count'],item['parent'],item['statement'],item['body']

def fill_params(text, params):
    template = Template(text)
    txt = template.substitute(params)
#     print params
#     print text
#     print txt
    return txt


def get_parent_body(parent):
    return statement_dict[parent]

def get_package_path(body):
    file_path = get_pkg_file_path()
    file_path = file_path.split(".")
    file_path2 = []
    for path in file_path:
        file_path2.append(format_name(path))
        
    file_path = ".".join(file_path2)
    return  file_path

def get_file_path(parent):
    a = parent.split("/")
    path = ""
    for i in range(len(a)+1):
        x = "."
        d = 0
        for j in range(1, i):
            d = j
            x = x + "/" + a[j]
            
        if not re.match("^\d+$", a[d]) and x and x != ".":
            body = statement_dict[x]
            if i != len(a):
                path = path + "/" + format_name(body['@name'])
            else:
                path = path + "/" + format_name(body['@name'], True)

    return path[1:]

def format_name(name, is_file=False, is_variable=False):
    java_keywords_list = """
abstract    continue    for    new    switch
assert    default    goto    package    synchronized
boolean    do    if    private    this
break    double    implements    protected    throw
byte    else    import    public    throws
case    enum    instanceof    return    transient
catch    extends    int    short    try
char    final    interface    static    void
class    finally    long    strictfp   volatile
const    float    native    super    while""".split()

    formatted_name = name
    formatted_name = formatted_name.lower()
    formatted_name = re.sub(r'(^\d)', r'YangAutoPrefix\1', formatted_name)

    if formatted_name in java_keywords_list:
        formatted_name = "YangAutoPrefix" + formatted_name
    formatted_name = formatted_name.capitalize()
    formatted_name = re.sub("[\W_]", " ", formatted_name)

    formatted_name_list = formatted_name.split()
    formatted_name1 = []
    for formatted_name_elem in formatted_name_list:
        formatted_name1.append(formatted_name_elem.capitalize())
    formatted_name = "".join(formatted_name1)
    formatted_name = formatted_name.rstrip()
    if is_file == True:
        return formatted_name
    if is_variable == True:
        formatted_name = formatted_name[0].lower() + formatted_name[1:]
        return formatted_name
    else:
        return formatted_name.lower()

def format_namespace(uri):
    namespace = uri.replace(":" , "/")
    namespace_list = namespace.split("/")
    for i, item in enumerate(namespace_list):
        namespace_list[i] = format_name(item)
    namespace = "/".join(namespace_list)
    return namespace

def get_base_file_path(statement_dict):
    body = get_parent_body('./module')
    
    namespace = format_namespace(body['namespace']['@uri'])
    
    # Format Revision
    if body.has_key('revision'):
        revision = body['revision']['@date'].replace("-" , "")
    else:
        revision = datetime.datetime.now().strftime ("%Y%m%d")

    file_path = test_env_path + default_path + namespace + "/rev" + revision + "/"
    return  file_path

def get_pkg_file_path():

    body = get_parent_body('./module')
    namespace = body['namespace']['@uri'].replace(":" , "/")

    if body.has_key('revision'):
        revision = body['revision']['@date'].replace("-" , "")
    else:
        revision = datetime.datetime.now().strftime ("%Y%m%d")

    file_path = default_path + namespace + "/rev" + revision + "/"
    return  file_path.replace("/", ".")


def check_patterns_in_file(filename, template):
    line_template = template.split("\n")
    open_file = filename
    print "verification in ", open_file
    whole_file = open(open_file, 'r').read()
    for line in line_template:
        line =  str(line).strip().replace("*", "\*")
        line =  str(line).strip().replace("(", "\(")
        line =  str(line).strip().replace(")", "\)")
        if re.search(line, whole_file) is not None:
            print "string presnt in file++++++++|",line,"|+++++++++\n"
        else:
            print "string not presnt in file>>>>>>>>>>>|",line,"|<<<<<<<<<<<<<<<<\n"

def generate_html_diff(snippet, gen_code):
    target = open("snippet", 'w')
    target.write(snippet)
    target.close()



    target = open("code", 'w')
    target.write(gen_code)
    target.close()


    fromlines = open("snippet", 'U').readlines()
    tolines = open("code", 'U').readlines()

    diff = difflib.HtmlDiff().make_file(fromlines, tolines, "snippet","code")
    target = open("test_failed.html", 'w')
    target.write(diff)
    target.close()

def statement_parser(statement_list):
    for item in statement_list:
        statement = item['statement']
        body = item['body']
        parent = item['parent']
        template_files = ['interface', 'builder', 'package_info', 'parent_interface', 'parent_builder', 'child_interface', 'child_builder']

        if re.search("\[\d+\]$", statement):            
            print "I am got statement ", statement
            statement = re.sub("\[\d+\]", "", statement)
               
        #print "I am calling statement ", statement
        
        # Interface
        params = get_params(statement, parent, body)
        files = get_java_files(statement, parent, body)
        print "================================================================================\n" 
        print "Checking below JAVA files for statement ", statement
        print "================================================================================\n" 
        for template_file in template_files:
            if hasattr(eval(template_file), statement.replace("-", "_")):
                print "Check Java File = " , files[template_file]
                print "================================================================================\n" 
                f = open(files[template_file], 'r')
                java_file_text = f.read()
                f.close()
                statement_template_list = eval(template_file + "." + statement.replace("-", "_"))
                for statement_template in statement_template_list:
                    java_snippet = fill_params(statement_template, params)
                    result = java_snippet in java_file_text
                    print result
                    
                    if not result:
                        #print java_snippet
                        #print "-----------------\n" +java_file_text + "------------------\n"
                        generate_html_diff(java_snippet, java_file_text)
#                         webbrowser.open('file://' + os.path.realpath(failed_result_filename))
                        print "*******************************************************"
                        print "failed report opened in Browser... pls check & resolve"
                        print "*******************************************************"
#                        exit()
                    else:
                        print java_snippet
                        java_file_text = java_file_text.replace(java_snippet, "")
#                         java_file_text = java_file_text.replace(java_snippet, "\"" + java_snippet + "\"")
#                         print "-----------------\n" +java_file_text + "------------------\n"
                        f = open(files[template_file], 'w')
                        f.write(java_file_text.lstrip())
                        f.close()
                        
def get_child(statement, parent, body):
    child_list = get_child_names(".", body)
    child_list_with_new_line = []
    obj_equal = []
    add_line = []
    build_obj = []
    if child_list is not None:
        print child_list
        x = 1
        for i in range(0,len(child_list)):
            child_name = format_name(child_list[i], True)
            child_name_lower = format_name(child_list[i], is_variable=True)                
            obj_equal.append("""Objects.equals(""" + child_name_lower + """, other.""" + child_name_lower +""") &&""")
            add_line.append(".add(\""  + child_name_lower +"\", " + child_name_lower + ")")
            build_obj.append("this."+ child_name_lower +" = builderObject.get"+ child_name +"();")
            child_list_with_new_line.append(child_name_lower)
            #after 4th element need a newline + 16 spaces          
            if x%4 == 0 and x != len(child_list):
                child_list_with_new_line.append("""
             """)
            x = x+1
        child_list_string = ", ".join(child_list_with_new_line)
        child_list_string1 = child_list_string.replace(""", 
             , """, """,
             """)
        childs = child_list_string1
        obj_equal = """
                     """.join(obj_equal)
        obj_equal =  obj_equal[:-2].strip()
        add_line = """
                """.join(add_line)
        build_obj = """
            """.join(build_obj)                                     
        return {'childs': childs, 'build_obj':build_obj, 'add_line':add_line ,'obj_equal':obj_equal }
    
def get_params(statement, parent, body):
    params = {}
    if statement == 'module':
        package_path = get_package_path(body) 
        package_path = package_path[:-1]
        params['package'] = package_path
        params['module_name'] = format_name(body['@name'], True)
        params['module_name_lower'] = format_name(body['@name'], is_variable=True)
        child_list = get_child_names(".", body)
        if child_list is not None:
            result = get_child(statement, parent, body)
            print type(result['obj_equal'])
            params['childs'] = result['childs']
            params['obj_equal'] = result['obj_equal']
            params['add_line'] =  result['add_line']
            params['build_obj'] = result['build_obj']  
    elif statement == 'leaf':
        params['leaf_name'] = format_name(body['@name'], True)
        params['leaf_name_lower'] = format_name(body['@name'], is_variable=True)
        type_dict = {'int8': 'byte', 'int16': 'short', 'int32': 'int', 'int64': 'long', 'string': 'String', 'uint8' : 'short', 'uint16' : 'int', 'uint32' : 'long', 'uint64' : 'BigInteger', 'boolean' : 'boolean', 'union' : 'need to write', 'enumeration' : 'need to write'};
        params['leaf_type'] = type_dict[body['type']['@name']]
        params['parent_name'] = format_name(get_parent_body(parent)['@name'], True)
    elif statement == 'leaf-list':
        params['leaf_list_name'] = format_name(body['@name'], True)
        params['leaf_list_name_lower'] = format_name(body['@name'], is_variable=True)
        type_dict = {'int8': 'byte', 'int16': 'short', 'string': 'String', 'uint16' : 'int'};
        params['leaf_list_type'] = type_dict[body['type']['@name']]
        params['parent_name'] = format_name(get_parent_body(parent)['@name'], True)
    elif statement == 'container':
        name = get_file_path(parent)
        cont_pkg_path = name.split("/")
        del cont_pkg_path[-1]
        cont_pkg_path = '.'.join(cont_pkg_path)
        params['parent_name'] = format_name(get_parent_body(parent)['@name'], True)
        params['parent_name_lower'] = format_name(get_parent_body(parent)['@name'], is_variable=True)
        package_path = get_package_path(body)
        package_path = package_path[:-1]
        name_parent = get_file_path(parent)
        #name_parent = format_name(name_parent)
        name_parent1 = name_parent.split("/")
        name_parent_folder = []
        for i in range(0,len(name_parent1)):
            name_parent_folder.append(format_name(name_parent1[i]))
#         name_parent_folder = format_name(name_parent)
        print name_parent_folder
        name_parent_folder = ".".join(name_parent_folder)        
        container_package_path = package_path + "." + name_parent_folder
        print package_path
        print name_parent_folder
        print container_package_path
        params['container_path'] = container_package_path
        params['container_name'] = format_name(body['@name'], True)
        params['container_name_lower'] = format_name(body['@name'], is_variable=True)
        child_list = get_child_names(".", body)
        if child_list is not None:
            result = get_child(statement, parent, body)
            params['childs'] = result['childs']
            params['obj_equal'] = result['obj_equal']
            params['add_line'] =  result['add_line']
            params['build_obj'] = result['build_obj']
    return params

def get_java_files(statement, parent, body):
    file_dict = {}
    if statement == 'module':
        #name = body['@name'].replace("_", "")
        name = format_name(body['@name'], True)
        file_dict['interface'] = base_path + name + "Manager.java"
        file_dict['builder'] = base_path + name + "Service.java"
        file_dict['package_info'] = base_path + "package-info.java"
        child_list = get_child_names(".", body)
        if child_list is not None:
            print child_list
            file_dict['child_interface'] = base_path + name + "Manager.java"
            file_dict['child_builder'] = base_path + name + "Service.java"
    elif statement == 'leaf':
        name = get_file_path(parent)
        if parent == "./module":
            file_dict['interface'] = base_path + name + "Manager.java"
            file_dict['builder'] = base_path + name + "Service.java"
        else:
            file_dict['interface'] = base_path + name + ".java"
            file_dict['builder'] = base_path + name + "Builder.java"
    elif statement == 'container':
        name = format_name(body['@name'], True)
        name_parent = get_file_path(parent)
        cont_pkg_path = name.split("/")
        del cont_pkg_path[-1]
        cont_pkg_path = '/'.join(cont_pkg_path)
        name_parent1 = name_parent.split("/")
        name_parent_folder = []
        for i in range(0,len(name_parent1)):
            name_parent_folder.append(format_name(name_parent1[i]))
#         name_parent_folder = format_name(name_parent)
        name_parent_folder = "/".join(name_parent_folder)
        file_dict['interface'] = base_path + name_parent_folder + "/" + name + ".java"
        file_dict['builder'] = base_path + name_parent_folder + "/" + name + "Builder.java"
        file_dict['package_info'] = base_path + name_parent_folder + "/" + "package-info.java"
        file_dict['parent_interface'] = base_path + name_parent + "Manager.java"
        file_dict['parent_builder'] = base_path  + name_parent + "Service.java"
        child_list = get_child_names(".", body)
        if child_list is not None:
            print child_list
            file_dict['child_interface'] = base_path + name_parent_folder + "/" + name + ".java"
            file_dict['child_builder'] = base_path + name_parent_folder + "/" + name + "Builder.java"
    elif statement == 'leaf-list':
        name = get_file_path(parent)
        if parent == "./module":
            file_dict['interface'] = base_path + name + "Manager.java"
            file_dict['builder'] = base_path + name + "Service.java"
        else:
            file_dict['interface'] = base_path + name + ".java"
            file_dict['builder'] = base_path + name + "Builder.java"            
    return file_dict

def create_pom_xml():
    print "sathish"
    curr_dir = os.getcwd()
    os.chdir(test_app_fodler)
    #shutil.copyfile('../rest/pom.xml', 'pom.xml')

def modify_test_pom_xml():
    utils_pom_file = utils_folder + "pom.xml"
    test_app_pom_file = test_app_fodler + "pom.xml"
    dummy_xml = test_app_fodler + "dummy_pom.xml"
    f = open(utils_pom_file, 'r')
    utils_pom_file_text = f.read()
    f.close()
    #print utils_folder
    #print utils_pom_file_text
    m = re.search('<version>(\S+)</version>', utils_pom_file_text) 
    onos_snap_shot_version =  m.group(1)
    print onos_snap_shot_version
    f = open(test_app_pom_file, 'r')
    test_app_pom_file_text = f.read()
    f.close()
    test_app_pom_file_text = re.sub('<version>(\S+)</version>', '<version>' + onos_snap_shot_version + '</version>', test_app_pom_file_text, 1)
    f = open(dummy_xml, 'w')
    f.write(test_app_pom_file_text)
    f.close
    shutil.move(test_app_fodler + 'pom.xml', test_app_fodler + 'pom_original.xml')
    shutil.move(dummy_xml, test_app_pom_file)            

def modify_utils_pom_xml():
    test_module_body = """<module>test</module>"""
    utils_pom_file = utils_folder + "pom.xml"
    f = open(utils_pom_file, 'r')
    pom_file_text = f.read()
    f.close()
    result = test_module_body in pom_file_text
    print result
    if not result:
        with open(utils_pom_file, 'r') as myfile:
            xml_snippet = myfile.read()
            xml_snippet = re.sub('</modules>', '    <module>test</module>\r    </modules>', xml_snippet)
            f = open(utils_folder + "pom_tmp.xml", 'w')
            f.write(xml_snippet)
            f.close
            shutil.copyfile(utils_folder + 'pom.xml', utils_folder + 'pom_original.xml')
            shutil.copyfile(utils_folder + "pom_tmp.xml", utils_folder + 'pom.xml')
    else:
        print "already line is present", test_module_body
    
def create_folder_run_mvn():
    os.system("sudo rm -rf " + test_app_fodler)
    shutil.copytree(yang_files_source_folder, test_app_fodler)
    modify_utils_pom_xml()
    modify_test_pom_xml()
    curr_dir = os.getcwd()
    os.chdir(test_app_fodler)
    os.system("mvn --version")
    os.system("mvn clean install -DskipTests")
    result = os.system("sudo chmod 777 -R " + test_app_fodler)
    print result
    os.chdir(curr_dir)
    print os.getcwd()
    os.chdir(test_app_yang_folder)
    print os.getcwd()
    yang_files_list = []
    for file_list in os.listdir(test_app_yang_folder):
        if file_list.endswith(".yang"):
            yang_files_list.append(file_list)
    return yang_files_list

def backup_java_files():
    from_directory = test_env_path
    to_directory = test_env_path + "../java_temp/"
    copy_tree(from_directory, to_directory)

def get_test_case_list():
    t = []
    dir_list = os.listdir(test_env_path + default_path)
    dir_list.sort()
    for d in dir_list:
        x = os.path.join(test_env_path + default_path, d)
        if os.path.isdir(x):
            t.append(d)
    return t

def generate_validation_result():
    diff = ""
    summary = []
    org_test_env_path = test_env_path + "../java_temp/"

    testcase = get_test_case_list()
    failed_testcases = 0

    for t in testcase:
        passed_count = 0
        failed_count = 0
        for root, dirs, files in os.walk(test_env_path + default_path + t):
            dirs.sort()
            for name in files:
                if not name.endswith(".java"):
                    continue
                right_file = os.path.join(root, name)
                left_file = right_file.replace(test_env_path, org_test_env_path)

                if os.path.getsize(right_file) > 0:
                    left_text = open(left_file, 'U').readlines()
                    right_text = open(right_file, 'U').readlines()

                    left_file = left_file.replace(org_test_env_path + default_path, "\n[YANG_UTILS_GENRATED_JAVA_CODE]\n")
                    right_file = right_file.replace(test_env_path + default_path, "\n[AFTER VERIFIED LINE REMOVAL]\n")

                    diff += difflib.HtmlDiff().make_file(left_text, right_text, left_file, right_file)
                    failed_count += 1
                else:
                    passed_count += 1

        summary.append("Java files Passed = {}\tFailed = {}\t PassRate = {:.0%}\tTestcase_folder_name = {}"
                       .format(passed_count, failed_count, float(passed_count) / (passed_count + failed_count),  t))
        if failed_count > 0:
            failed_testcases += 1

    passed_testcases = len(testcase) - failed_testcases
    summary.insert(0, "TESTCASES PASSED = {}\tTESTCASES FAILED = {}\tPASS RATE = {:.0%}"
                   .format(passed_testcases, failed_testcases, float(passed_testcases) / (passed_testcases + failed_testcases)))
    #print summary
    print "total testcases", len(testcase)
    print "testcases", testcase
    print "passed_testcases", passed_testcases
    print "failed_testcases", failed_testcases
    print "pass_rate", str((float(passed_testcases) / (passed_testcases + failed_testcases)) * 100) + "%"

    result = difflib.HtmlDiff().make_file(summary, "", "YANG TEST RESULT SUMMARY", "")
    result += diff
    target = open("test_result.html", 'w')
    target.write(result)
    target.close()


def intialize_globals():
    global statement_list
    global statement_dict
    global base_path
    statement_list = []
    statement_dict = {}
    base_path = ""

def revert_changes():
    shutil.copyfile(utils_folder + 'pom_original.xml', utils_folder + 'pom.xml')
#    shutil.copyfile(test_app_fodler + 'pom_original.xml', test_app_fodler + 'pom.xml')
#     os.system("sudo rm -rf " + test_app_fodler)

def test_yang():
    file_list = create_folder_run_mvn()
    backup_java_files()
    file_list = sorted(file_list)
    #os.system("dconf write /org/compiz/profiles/unity/plugins/core/focus-prevention-level 0")
    for yang_file in file_list:
        intialize_globals()
        #d = yang_to_dict("/home/root1/onos/utils/test/src/main/yang/Test_case_2.yang")
        print yang_file
        d = yang_to_dict(test_app_yang_folder + yang_file)
        traverse(".", d)

        global base_path
        base_path = get_base_file_path(statement_dict)
        statement_list.sort(key=get_parents_count, reverse=True)
        #print_statement_list(statement_list)
        #print "\n".join(statement_dict.keys())
        statement_parser(statement_list)
    generate_validation_result()
    print "************************************************************"
    print "YANG TEST RESULT SUMMARY opened in Browser.................."
    print "************************************************************"
    webbrowser.open('file://' + os.path.realpath(result_filename))
    #os.system("dconf write /org/compiz/profiles/unity/plugins/core/focus-prevention-level 1")
    revert_changes()
    exit()
    
curr_dir = os.getcwd()
print os.environ['ONOS_ROOT']
ONOS_ROOT = os.environ['ONOS_ROOT']
print ONOS_ROOT

test_env_path = "/home/root1/onos/utils/test/src/main/java/"
default_path = "org/onosproject/yang/gen/v1/"
yang_files_source_folder = "/home/root1/yang_automation/test/"
test_app_fodler = "/home/root1/onos/utils/test/"
utils_folder = "/home/root1/onos/utils/"
test_app_yang_folder = test_app_fodler + "src/main/yang/"
result_filename = "test_result.html"
failed_result_filename = "test_failed.html"
import math

content = dir(math)

print content
raw_input()


test_yang()