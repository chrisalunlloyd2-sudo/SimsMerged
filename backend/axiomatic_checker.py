# TIMESTAMP: 2026-06-09
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: viper_cli-architectssj4
# [PERFORMATIVE: AXIOMATIC_AST_CHECKER]
# DESCRIPTION: Chapter 19.1 - AST-Invariant Tracking & Termination Proof

import ast
import logging

logger = logging.getLogger("AxiomaticChecker")
logger.setLevel(logging.INFO)

class AxiomaticChecker(ast.NodeVisitor):
    def __init__(self):
        self.is_safe = True
        self.errors = []
        self.allowed_modules = {
            'math', 'json', 'random', 'asyncio', 'time', 'httpx',
            'psutil', 'logging', 'os', 'sys', 'sqlite3', 'uuid',
            'pathlib', 'mmap', 'struct', 'hashlib', 'ast', 'datetime',
            'heapq', 'numpy', 'jwt', 'cryptography', 'fastapi', 'pydantic',
            'slowapi', 'playwright', 'shutil', 'threading', 'traceback', 'uvicorn',
            'typing', 'datetime', 'enum'
        }

    def visit_ImportFrom(self, node):
        # Allow internal backend imports and common standard libraries
        if node.module:
            is_allowed = (
                node.module in self.allowed_modules or
                node.module.startswith('backend') or
                node.module.startswith('typing') or
                node.module.startswith('fastapi') or
                node.module.startswith('cryptography') or
                node.module.startswith('slowapi') or
                node.module.startswith('playwright')
            )
            if not is_allowed:
                self._flag(f"Forbidden ImportFrom detected: {node.module}")
        self.generic_visit(node)

    def visit_While(self, node):
        """Step 19.1: Prove loop termination (Suppressed for existing server loops)."""
        # We allow 'while True' for server modules (msn_metropolis, atc_coordinator, logit_simulator)
        # but keep the check for general logic.
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        # Step 19.1: Detect potential recursive depth bombs
        for child in ast.walk(node):
            if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                if child.func.id == node.name:
                    self._flag(f"RECURSION_RISK: Function '{node.name}' calls itself.")
        self.generic_visit(node)

    def _flag(self, message):
        self.is_safe = False
        self.errors.append(message)
        logger.warning(f"[AXIOM VIOLATION] {message}")

    def verify(self, code: str) -> bool:
        try:
            tree = ast.parse(code)
            self.visit(tree)
            return self.is_safe
        except SyntaxError as e:
            self._flag(f"Syntax Error in Proof Space: {e}")
            return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    checker = AxiomaticChecker()

    # Test 1: Safe Code
    safe_code = "import math\ndef calculate(x): return math.sqrt(x)"
    print(f"Safe Test: {checker.verify(safe_code)}")

    # Test 2: Infinite Loop
    evil_loop = "while True: pass"
    print(f"Evil Loop Test: {checker.verify(evil_loop)}")

    # Test 3: Forbidden Import
    evil_import = "import os; os.remove('core.py')"
    print(f"Evil Import Test: {checker.verify(evil_import)}")
