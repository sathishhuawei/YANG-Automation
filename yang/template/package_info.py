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

module = [FILE_HEADER, """/**
 * Implementation of YANG node ${module_name_lower}.
 */""", 
 """package ${package};"""]


container = [FILE_HEADER, """/**
 * Implementation of YANG node ${parent_name_lower}'sChildrenNodes.
 */""",
 """/**
 * Implementation of YANG node ${parent_name_lower}'s children nodes.
 */""", 
 """package ${container_path};"""]