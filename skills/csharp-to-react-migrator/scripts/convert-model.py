#!/usr/bin/env python3
"""
Convert C# model classes to Prisma schema
"""

import argparse
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class CSharpModelParser:
    """Parse C# model classes"""
    
    # C# to Prisma type mapping
    TYPE_MAPPING = {
        'int': 'Int',
        'long': 'BigInt',
        'short': 'Int',
        'byte': 'Int',
        'float': 'Float',
        'double': 'Float',
        'decimal': 'Decimal',
        'bool': 'Boolean',
        'string': 'String',
        'char': 'String',
        'DateTime': 'DateTime',
        'DateTimeOffset': 'DateTime',
        'Guid': 'String',
        'byte[]': 'Bytes',
    }
    
    def __init__(self):
        self.current_class = None
        self.properties = []
        self.attributes = {}
    
    def parse_file(self, file_path: str) -> Dict:
        """Parse a C# model file and extract class information"""
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        
        # Find class definition
        class_match = re.search(r'public\s+class\s+(\w+)', content)
        if not class_match:
            raise ValueError(f"No public class found in {file_path}")
        
        class_name = class_match.group(1)
        
        # Extract properties
        properties = self._extract_properties(content)
        
        # Extract attributes
        attributes = self._extract_attributes(content)
        
        return {
            'class_name': class_name,
            'properties': properties,
            'attributes': attributes,
            'file_path': file_path
        }
    
    def _extract_properties(self, content: str) -> List[Dict]:
        """Extract properties from C# class"""
        
        properties = []
        
        # Pattern to match C# properties
        # public Type Name { get; set; }
        pattern = r'public\s+(\w+(?:<[\w\s,<>]+>)?)\s+(\w+)\s*\{\s*(?:get|set|init).*?\}'
        
        matches = re.finditer(pattern, content)
        
        for match in matches:
            csharp_type = match.group(1)
            property_name = match.group(2)
            
            # Check if nullable
            is_nullable = csharp_type.endswith('?')
            if is_nullable:
                csharp_type = csharp_type[:-1]
            
            # Handle generic types (e.g., List<T>)
            is_collection = False
            if csharp_type.startswith('List<') or csharp_type.startswith('ICollection<'):
                is_collection = True
                # Extract inner type
                inner_match = re.search(r'<(\w+)>', csharp_type)
                if inner_match:
                    csharp_type = inner_match.group(1)
            
            # Map C# type to Prisma type
            prisma_type = self.TYPE_MAPPING.get(csharp_type, 'String')
            
            properties.append({
                'name': property_name,
                'csharp_type': csharp_type,
                'prisma_type': prisma_type,
                'is_nullable': is_nullable,
                'is_collection': is_collection
            })
        
        return properties
    
    def _extract_attributes(self, content: str) -> Dict:
        """Extract DataAnnotations attributes"""
        
        attributes = {}
        
        # Common validation attributes
        attr_patterns = {
            'required': r'\[Required\]',
            'key': r'\[Key\]',
            'email': r'\[EmailAddress\]',
            'string_length': r'\[StringLength\((\d+)\)\]',
            'range': r'\[Range\((.*?)\)\]',
            'min_length': r'\[MinLength\((\d+)\)\]',
            'max_length': r'\[MaxLength\((\d+)\)\]',
        }
        
        # Find property with attributes
        prop_pattern = r'(\[[\s\S]*?\])\s*public\s+\w+\s+(\w+)'
        
        for match in re.finditer(prop_pattern, content):
            attr_block = match.group(1)
            prop_name = match.group(2)
            
            prop_attrs = {}
            
            for attr_name, pattern in attr_patterns.items():
                if re.search(pattern, attr_block):
                    attr_match = re.search(pattern, attr_block)
                    if attr_match.groups():
                        prop_attrs[attr_name] = attr_match.group(1)
                    else:
                        prop_attrs[attr_name] = True
            
            if prop_attrs:
                attributes[prop_name] = prop_attrs
        
        return attributes


class PrismaSchemaGenerator:
    """Generate Prisma schema from parsed C# models"""
    
    def __init__(self):
        self.models = []
    
    def add_model(self, model_data: Dict):
        """Add a model to the schema"""
        self.models.append(model_data)
    
    def generate_schema(self) -> str:
        """Generate complete Prisma schema"""
        
        schema_parts = [
            '// This is your Prisma schema file',
            '// Generated from C# models',
            '',
            'generator client {',
            '  provider = "prisma-client-js"',
            '}',
            '',
            'datasource db {',
            '  provider = "postgresql"',
            '  url      = env("DATABASE_URL")',
            '}',
            ''
        ]
        
        for model in self.models:
            schema_parts.append(self._generate_model(model))
            schema_parts.append('')
        
        return '\n'.join(schema_parts)
    
    def _generate_model(self, model_data: Dict) -> str:
        """Generate a single Prisma model"""
        
        class_name = model_data['class_name']
        properties = model_data['properties']
        attributes = model_data.get('attributes', {})
        
        lines = [f'model {class_name} {{']
        
        for prop in properties:
            prop_line = self._generate_property(prop, attributes.get(prop['name'], {}))
            lines.append(prop_line)
        
        # Add indexes for frequently queried fields
        indexed_fields = self._get_indexed_fields(properties, attributes)
        if indexed_fields:
            lines.append('')
            for fields in indexed_fields:
                lines.append(f'  @@index([{fields}])')
        
        # Add table mapping
        table_name = self._class_to_table_name(class_name)
        lines.append(f'  @@map("{table_name}")')
        lines.append('}')
        
        return '\n'.join(lines)
    
    def _generate_property(self, prop: Dict, attrs: Dict) -> str:
        """Generate a single Prisma property"""
        
        name = prop['name']
        prisma_type = prop['prisma_type']
        is_nullable = prop['is_nullable']
        is_collection = prop['is_collection']
        
        # Handle ID property
        if name.lower() == 'id':
            return f'  {name.ljust(20)} Int      @id @default(autoincrement())'
        
        # Handle collections (relationships)
        if is_collection:
            related_model = prop['csharp_type']
            return f'  {name.ljust(20)} {related_model}[]'
        
        # Build type string
        type_str = prisma_type
        if is_nullable:
            type_str += '?'
        
        # Add attributes
        prop_attrs = []
        
        if attrs.get('required') and not is_nullable:
            prop_attrs.append('@db.VarChar(255)')
        
        if attrs.get('string_length'):
            length = attrs['string_length']
            prop_attrs.append(f'@db.VarChar({length})')
        
        if attrs.get('email'):
            prop_attrs.append('@db.VarChar(255)')
        
        if attrs.get('key'):
            prop_attrs.insert(0, '@id')
        
        # Check for common patterns
        if name.lower() == 'createdat':
            prop_attrs.append('@default(now())')
        elif name.lower() == 'updatedat':
            prop_attrs.append('@updatedAt')
        elif name.lower() == 'isactive':
            prop_attrs.append('@default(true)')
        elif name.lower() == 'isdeleted':
            prop_attrs.append('@default(false)')
        
        # Build final line
        attr_str = ' '.join(prop_attrs) if prop_attrs else ''
        
        return f'  {name.ljust(20)} {type_str.ljust(8)} {attr_str}'.rstrip()
    
    def _get_indexed_fields(self, properties: List[Dict], attributes: Dict) -> List[str]:
        """Get fields that should be indexed"""
        
        indexed = []
        
        for prop in properties:
            name = prop['name'].lower()
            
            # Index common query fields
            if name in ['email', 'username', 'slug', 'code', 'status']:
                indexed.append(f'[{prop["name"]}]')
            
            # Index foreign keys
            if name.endswith('id') and name != 'id':
                indexed.append(f'[{prop["name"]}]')
        
        return indexed
    
    def _class_to_table_name(self, class_name: str) -> str:
        """Convert class name to table name (PascalCase to snake_case)"""
        
        # Insert underscore before uppercase letters and convert to lowercase
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', class_name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower() + 's'


def convert_model(input_file: str, output_file: Optional[str] = None, append: bool = False):
    """Convert a C# model file to Prisma schema"""
    
    # Parse C# model
    parser = CSharpModelParser()
    model_data = parser.parse_file(input_file)
    
    print(f"📄 Parsed C# model: {model_data['class_name']}")
    print(f"   Found {len(model_data['properties'])} properties")
    
    # Generate Prisma schema
    generator = PrismaSchemaGenerator()
    generator.add_model(model_data)
    schema = generator.generate_model(model_data)
    
    # Output
    if output_file:
        output_path = Path(output_file)
        
        if append and output_path.exists():
            # Read existing schema and append
            with open(output_path, 'r', encoding='utf-8') as f:
                existing = f.read()
            
            # Remove closing brace if exists
            existing = existing.rstrip()
            if existing.endswith('}'):
                existing = existing[:-1].rstrip()
            
            schema = existing + '\n\n' + schema
        
        # Write schema
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(schema)
        
        print(f"✅ Generated Prisma schema: {output_path}")
    else:
        print("\n" + schema)


def main():
    parser = argparse.ArgumentParser(
        description="Convert C# model classes to Prisma schema"
    )
    parser.add_argument(
        "input",
        help="Path to C# model file (.cs)"
    )
    parser.add_argument(
        "--output",
        help="Output Prisma schema file (default: stdout)"
    )
    parser.add_argument(
        "--append",
        action="store_true",
        help="Append to existing schema file"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output"
    )
    
    args = parser.parse_args()
    
    try:
        convert_model(args.input, args.output, args.append)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    import sys
    main()
