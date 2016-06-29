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
 */
"""

module = [FILE_HEADER,
"""package ${package};""",
"""
/**
 * Represents the builder implementation of ${module_name_lower}.
 */""",
"""public class ${module_name}Builder implements ${module_name}.${module_name}Builder {
""",
""" @Override
    public ${module_name} build() {
        return new ${module_name}Impl(this);""",
"""    }""",
"""/**
     * Creates an instance of ${module_name_lower}Builder.
     */
    public ${module_name}Builder() {""",
"""}""",    
"""/**
     * Represents the implementation of ${module_name_lower}.
     */""",
"""public final class ${module_name}Impl implements ${module_name} {
""",
"""/**
         * Creates an instance of ${module_name_lower}Impl.
         *
         * @param builderObject builder object of ${module_name_lower}
         */""",
"""public ${module_name}Impl(${module_name}Builder builderObject) {""",
"""/**
 * Abstraction of an entity which represents the functionality of ${module_name_lower}Service.
 */""",
"""public interface ${module_name}Service {"""]


leaf = ["""    private ${leaf_type} ${leaf_name_lower};""",
# """import java.util.Objects;""",        
"""@Override
    public ${leaf_type} get${leaf_name}() {
        return ${leaf_name_lower};
    }""",
"""@Override
    public ${parent_name}Builder set${leaf_name}(${leaf_type} ${leaf_name_lower}) {
        this.${leaf_name_lower} = ${leaf_name_lower};
        return this;
    }""",
"""@Override
        public ${leaf_type} get${leaf_name}() {
            return ${leaf_name_lower};
        }""",
"""/**
     * Returns the attribute ${leaf_name_lower}.
     *
     * @return value of ${leaf_name_lower}
     */
    ${leaf_type} get${leaf_name}();""",
"""/**
     * Sets the value to attribute ${leaf_name_lower}.
     *
     * @param ${leaf_name_lower} value of ${leaf_name_lower}
     */
    void set${leaf_name}(${leaf_type} ${leaf_name_lower});""",
"""import java.math.BigInteger;""",
"""@Override""",
"""public int ${leaf_name_lower}() {""",
"""return ${leaf_name_lower};""",
"""@Override""",
"""public ${parent_name}Builder ${leaf_name_lower}(int ${leaf_name_lower}) {""",
"""this.${leaf_name_lower} = ${leaf_name_lower};""",
"""return this;""",
"""@Override""",
"""public int ${leaf_name_lower}() {""",
"""return ${leaf_name_lower};""",
"""this.${leaf_name_lower} = builderObject.${leaf_name_lower}();""",
"""return Objects.hash(${leaf_name_lower});"""]
# """        @Override
#         public int hashCode() {
#             return Objects.hash(${leaf_name_lower});""",
# """@Override
#         public ${leaf_type} equals(Object obj) {
#             if (this == obj) {
#                 return true;""",
# """Objects.equals(${leaf_name_lower}, other.${leaf_name_lower});""",
# """this.${leaf_name_lower} = builderObject.get${leaf_name}();""",
# """@Override
#         public String toString() {
#             return MoreObjects.toStringHelper(getClass())
#                 .add("${leaf_name_lower}", ${leaf_name_lower})
#                 .toString();""",
# """return false;"""]
# """if (obj instanceof ${parent_name}Impl) {
#                 TestCase1Impl other = (${parent_name}Impl) obj;
#                 return"""

container = [FILE_HEADER,
"""package ${container_path};""",
"""import java.util.ArrayList;""",
# """import java.util.List;""",
"""import org.onosproject.yangutils.translator.tojava.AugmentedInfo;""",
# """import com.google.common.base.MoreObjects;""",
"""/**
 * Represents the builder implementation of ${container_name_lower}.
 */
public class ${container_name}Builder implements ${container_name}.${container_name}Builder {""",
"""@Override
    public ${container_name} build() {
        return new ${container_name}Impl(this);
    }""",
"""/**
     * Creates an instance of ${container_name_lower}Builder.
     */""",
"""public ${container_name}Builder() {""",
# """    }""",
"""/**
     * Represents the implementation of ${container_name_lower}.
     */""",
"""public final class ${container_name}Impl implements ${container_name} {""",
"""private List<AugmentedInfo> augmentedInfoList = new ArrayList<>();""",
# """if (obj instanceof ${container_name}Impl) {
#                 ${container_name}Impl other = (${container_name}Impl) obj;
#                 return""",
# """            }""",
"""/**
         * Creates an instance of ${container_name_lower}Impl.
         *
         * @param builderObject builder object of ${container_name_lower}
         */
        public ${container_name}Impl(${container_name}Builder builderObject) {""",
"""}""",
"""@Override
        public void addAugmentation(AugmentedInfo value) {
            getAugmentedInfoList().add(value);""",
# """        }""",
"""@Override
        public List<AugmentedInfo> getAugmentedInfoList() {
            return augmentedInfoList;""",
# """        }""",
"""@Override
        public void removeAugmentation() {
            getAugmentedInfoList().clear();""",
"""public ${container_name} build() {""",
"""return new ${container_name}Impl(this);""",
"""public int hashCode() {""",
"""public boolean equals(Object obj) {""",
"""if (this == obj) {""",
"""return true;""",
"""public String toString() {""",
"""return MoreObjects.toStringHelper(getClass())""",]
# """if (obj instanceof ${container_name}Impl) {
#                 ${container_name}Impl other = (${container_name}Impl) obj;
#                 return"""]
# """        }""",
# """    }""",
# """}"""]

leaf_list = ["""import java.util.List;""",
"""private List<${leaf_list_type}> ${leaf_list_name_lower};""",
"""@Override
    public List<${leaf_list_type}> get${leaf_list_name}() {
        return ${leaf_list_name_lower};""",
"""@Override
    public ${parent_name}Builder set${leaf_list_name}(List<${leaf_list_type}> ${leaf_list_name_lower}) {
        this.${leaf_list_name_lower} = ${leaf_list_name_lower};
        return this;""",
"""@Override
        public List<${leaf_list_type}> get${leaf_list_name}() {
            return ${leaf_list_name_lower};""",
"""/**
     * Returns the attribute ${leaf_list_name_lower}.
     *
     * @return list of ${leaf_list_name_lower}
     */
    List<String> get${leaf_list_name}();""",
"""    /**
     * Sets the value to attribute ${leaf_list_name_lower}.
     *
     * @param ${leaf_list_name_lower} list of ${leaf_list_name_lower}
     */
    void set${leaf_list_name}(List<String> ${leaf_list_name_lower});"""]

