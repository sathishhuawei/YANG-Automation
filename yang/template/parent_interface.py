container = ["""import ${container_path}.${container_name};""",
"""/**
         * Returns the attribute ${container_name_lower}.
         *
         * @return value of ${container_name_lower}
         */
        ${container_name} get${container_name}();""",
"""/**
         * Returns the builder object of ${container_name_lower}.
         *
         * @param ${container_name_lower} value of ${container_name_lower}
         * @return builder object of ${container_name_lower}
         */""",
"""${parent_name}Builder set${container_name}(${container_name} ${container_name_lower});""",
"""/**
     * Returns the attribute ${container_name_lower}.
     *
     * @return value of ${container_name_lower}
     */
    ${container_name} get${container_name}();""",
"""@Override""",
"""public ${container_name} get${container_name}() {""",
"""@Override""",
"""public void set${container_name}(${container_name} ${container_name_lower}) {"""]

