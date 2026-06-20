import os
import ast
import re

class GeneticCritic:
    """
    Step 1201: The Genetic Critic
    Analyzes code quality and automatically refactors for performance.
    """
    def __init__(self, project_root):
        self.project_root = project_root
        self.refactor_count = 0

    def scan_project(self):
        print(f"--- Genetic Critic: Scanning {self.project_root} ---")
        for root, dirs, files in os.walk(self.project_root):
            for file in files:
                if file.endswith('.py') or file.endswith('.java'):
                    self.analyze_file(os.path.join(root, file))

    def analyze_file(self, file_path):
        print(f"Analyzing {file_path}...")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if file_path.endswith('.py'):
            self.refactor_python(file_path, content)
        elif file_path.endswith('.java'):
            self.refactor_java(file_path, content)

    def refactor_python(self, file_path, content):
        # Example heuristic: Replace slow list concatenations with joins
        # or look for unused imports, etc.
        new_content = content
        # Heuristic 1: Use list comprehension instead of for-loops for simple appends (complex to implement with regex)
        # Heuristic 2: Replace 'range(len(x))' with 'enumerate(x)'
        pattern = re.compile(r'for (\w+) in range\(len\((\w+)\)\):')
        new_content = pattern.sub(r'for i, \1 in enumerate(\2):', new_content)

        if new_content != content:
            print(f"Refactoring Python file: {file_path}")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            self.refactor_count += 1

    def refactor_java(self, file_path, content):
        # Example heuristic: Replace String concatenation in loops with StringBuilder
        new_content = content
        if 'for' in content and '+=' in content and '"' in content:
            # Simple heuristic detection
            print(f"Warning: Potential slow string concatenation in {file_path}")

        # Heuristic: Replace simple getters/setters with something else? No, Java needs them.
        # Maybe optimize imports or something simpler.

        # For now, let's just log potential optimizations
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            self.refactor_count += 1

    def report(self):
        print(f"--- Genetic Critic Report ---")
        print(f"Total refactors applied: {self.refactor_count}")

if __name__ == "__main__":
    critic = GeneticCritic("C:/Users/viper/Desktop/SimsMerged")
    critic.scan_project()
    critic.report()
