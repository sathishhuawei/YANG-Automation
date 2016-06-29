FILE_HEADER = """/*
 * Copyright 2016-present Open Networking Laboratory
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */"""

module = [FILE_HEADER,
"""package ${package};""",
"""public interface ${module_name} {""",
"""/**
 * Abstraction of an entity which represents the functionality of ${module_name_lower}.
 */""",
"""/**
     * Builder for ${module_name_lower}.
     */
    interface ${module_name}Builder {

""",
"""/**
         * Builds object of ${module_name_lower}.
         *
         * @return object of ${module_name_lower}.
         */
        ${module_name} build();""",
"""    }""",
"""}""",
"""/**
 * Represents the implementation of ${module_name_lower}Manager.
 */""",
"""public class ${module_name}Manager implements ${module_name}Service {""",
"""import org.apache.felix.scr.annotations.Activate;""",
"""import org.apache.felix.scr.annotations.Component;""",
"""import org.apache.felix.scr.annotations.Deactivate;""",
"""import org.apache.felix.scr.annotations.Service;""",
"""import org.slf4j.Logger;""",
"""import static org.slf4j.LoggerFactory.getLogger;""",
"""@Component (immediate = true)""",
"""@Service""",
"""private final Logger log = getLogger(getClass());""",
"""@Activate""",
"""public void activate() {""",
"""//TODO: YANG utils generated code""",
"""log.info("Started");""",
"""@Deactivate""","""public void deactivate() {""",
"""//TODO: YANG utils generated code""",
"""log.info("Stopped");"""]

leaf = ["""/**
         * Returns the builder object of ${leaf_name_lower}.
         *
         * @param ${leaf_name_lower} value of ${leaf_name_lower}
         * @return builder object of ${leaf_name_lower}
         */
        ${parent_name}Builder set${leaf_name}(${leaf_type} ${leaf_name_lower});
""",
"""/**
     * Returns the attribute ${leaf_name_lower}.
     *
     * @return value of ${leaf_name_lower}
     */
    ${leaf_type} get${leaf_name}();
""",
"""/**
         * Returns the attribute ${leaf_name_lower}.
         *
         * @return value of ${leaf_name_lower}
         */
        ${leaf_type} get${leaf_name}();
""",
"""@Override
    public ${leaf_type} get${leaf_name}() {
        //TODO: YANG utils generated code""",
"""return false;""",
"""return 0;""",
"""return null;""",
"""import java.math.BigInteger;""",
"""@Override
    public void set${leaf_name}(${leaf_type} ${leaf_name_lower}) {
        //TODO: YANG utils generated code""",
"""/**
     * Returns the attribute ${leaf_name_lower}.
     *
     * @return value of ${leaf_name_lower}
     */
    int ${leaf_name_lower}();""",
"""        /**
         * Returns the attribute ${leaf_name_lower}.
         *
         * @return value of ${leaf_name_lower}
         */
        int ${leaf_name_lower}();""",
"""        /**
         * Returns the builder object of ${leaf_name_lower}.
         *
         * @param ${leaf_name_lower} value of ${leaf_name_lower}
         * @return builder object of ${leaf_name_lower}
         */""",
"""${parent_name}Builder typedef1(int ${leaf_name_lower});"""]

container = [FILE_HEADER,
"""package ${container_path};""",
"""import org.onosproject.yangutils.translator.tojava.HasAugmentation;""",
"""/**
 * Abstraction of an entity which represents the functionality of ${container_name_lower}.
 */""",
"""public interface ${container_name} extends HasAugmentation {""",
"""/**
     * Builder for ${container_name_lower}.
     */
    interface ${container_name}Builder {""",
"""/**
         * Builds object of ${container_name_lower}.
         *
         * @return object of ${container_name_lower}.
         */
        ${container_name} build();""",
"""    }""",
"""}""",
"""public interface ${container_name} {""",]

leaf_list = ["""import java.util.List;""",
"""/**
     * Returns the attribute ${leaf_list_name_lower}.
     *
     * @return list of ${leaf_list_name_lower}
     */""",
"""        /**
         * Returns the attribute ${leaf_list_name_lower}.
         *
         * @return list of ${leaf_list_name_lower}
         */""",     
"""List<${leaf_list_type}> get${leaf_list_name}();""",
"""/**
         * Returns the builder object of ${leaf_list_name_lower}.
         *
         * @param ${leaf_list_name_lower} list of ${leaf_list_name_lower}
         * @return builder object of ${leaf_list_name_lower}
         */""",
"""${parent_name}Builder set${leaf_list_name}(List<${leaf_list_type}> ${leaf_list_name_lower});""",
"""@Override
    public List<String> get${leaf_list_name}() {""",
"""return null;""",
"""@Override
    public void set${leaf_list_name}(List<String> ${leaf_list_name_lower}) {"""]
