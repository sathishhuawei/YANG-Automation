container = ["""import ${container_path}.${container_name};""",
# """import com.google.common.base.MoreObjects;""",
"""private ${container_name} ${container_name_lower};""",
"""@Override
    public ${container_name} get${container_name}() {
        return ${container_name_lower};""",
"""@Override
    public ${parent_name}Builder set${container_name}(${container_name} ${container_name_lower}) {
        this.${container_name_lower} = ${container_name_lower};
        return this;""",
# """private ${container_name} ${container_name_lower};""",
# """        @Override
#         public ${container_name} get${container_name}() {
#             return ${container_name_lower};""",
# """this.${container_name_lower} = builderObject.get${container_name}();""",
"""@Override
        public ${container_name} get${container_name}() {
            return ${container_name_lower};""",
"""/**
     * Returns the attribute ${container_name_lower}.
     *
     * @return value of ${container_name_lower}
     */
    ${container_name} get${container_name}();

    

    /**
     * Sets the value to attribute ${container_name_lower}.
     *
     * @param ${container_name_lower} value of ${container_name_lower}
     */
    void set${container_name}(${container_name} ${container_name_lower});"""]

