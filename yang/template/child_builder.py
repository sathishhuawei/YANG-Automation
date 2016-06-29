module = ["""import java.util.Objects;""",
"""import com.google.common.base.MoreObjects;""",
"""@Override
        public int hashCode() {
            return Objects.hash(${childs});""",
# """        }""",
"""@Override
        public boolean equals(Object obj) {
            if (this == obj) {
                return true;""",
"""if (obj instanceof ${module_name}Impl) {
                ${module_name}Impl other = (${module_name}Impl) obj;
                return""",
"""                 ${obj_equal};""",        
"""return false;""",
"""@Override
        public String toString() {
            return MoreObjects.toStringHelper(getClass())""",
"""${add_line}""",
""".toString();""",
"""            ${build_obj}"""]


container = ["""import com.google.common.base.MoreObjects;""",
"""import java.util.Objects;""",
"""import java.util.List;""",
"""@Override
        public int hashCode() {
            return Objects.hash(${childs});""",
# """        }""",
"""@Override
        public boolean equals(Object obj) {
            if (this == obj) {
                return true;""",
"""if (obj instanceof ${container_name}Impl) {
                ${container_name}Impl other = (${container_name}Impl) obj;
                return""",
"""                 ${obj_equal};""",        
"""return false;""",
"""@Override
        public String toString() {
            return MoreObjects.toStringHelper(getClass())""",
"""${add_line}""",
""".toString();""",
"""            ${build_obj}"""]


