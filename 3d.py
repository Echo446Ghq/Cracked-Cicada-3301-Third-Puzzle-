#!/usr/bin/env python3

import os
import sys
import subprocess
import time
import platform
import json
from pathlib import Path

GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
BLUE = '\033[0;34m'
CYAN = '\033[0;36m'
MAGENTA = '\033[0;35m'
BOLD = '\033[1m'
NC = '\033[0m'

class CicadaDependencyManager:
    
    def __init__(self):
        self.is_root = os.geteuid() == 0 if hasattr(os, 'geteuid') else False
        self.cuda_version = None
        self.install_log = []
        self.workspace_dir = Path("/workspace")
        self.workspace_dir.mkdir(exist_ok=True)
        
    def print_colored(self, message, color=NC):
        timestamp = time.strftime('%H:%M:%S')
        print(f"{color}[{timestamp}] {message}{NC}", flush=True)
        self.install_log.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}")
    
    def print_banner(self, text):
        width = 80
        self.print_colored("═" * width, CYAN)
        padding = (width - len(text) - 2) // 2
        banner_line = f"{'═' * padding} {text} {'═' * (width - padding - len(text) - 2)}"
        self.print_colored(banner_line, CYAN)
        self.print_colored("═" * width, CYAN)
    
    def run_command(self, command, description="", timeout=300, show_output=False, ignore_error=False):
        if description:
            self.print_colored(f"  {description}...", YELLOW)
        
        try:
            if show_output:
                result = subprocess.run(command, shell=True, timeout=timeout, check=not ignore_error)
                return True, "Success"
            else:
                result = subprocess.run(
                    command, 
                    shell=True, 
                    capture_output=True, 
                    text=True, 
                    timeout=timeout,
                    check=False
                )
                if result.returncode == 0 or ignore_error:
                    return True, result.stdout
                else:
                    return False, result.stderr
        except subprocess.TimeoutExpired:
            return False, f"Command timed out after {timeout} seconds"
        except subprocess.CalledProcessError as e:
            if ignore_error:
                return True, str(e)
            return False, str(e)
        except Exception as e:
            return False, str(e)
    
    def check_system_info(self):
        self.print_banner("SYSTEM INFORMATION")
        
        self.print_colored(f"Platform: {platform.platform()}", BLUE)
        self.print_colored(f"Python: {sys.version.split()[0]}", BLUE)
        self.print_colored(f"Architecture: {platform.machine()}", BLUE)
        self.print_colored(f"Root privileges: {'Yes' if self.is_root else 'No'}", BLUE)
        
        try:
            with open('/proc/meminfo', 'r') as f:
                mem_info = f.read()
                for line in mem_info.split('\n'):
                    if 'MemTotal' in line:
                        mem_total = int(line.split()[1]) // 1024
                        self.print_colored(f"Total Memory: {mem_total} MB", BLUE)
                        break
        except:
            pass
        
        success, output = self.run_command("df -h /workspace 2>/dev/null || df -h .", timeout=10, ignore_error=True)
        if success and output:
            lines = output.strip().split('\n')
            if len(lines) > 1:
                disk_info = lines[1].split()
                if len(disk_info) >= 4:
                    self.print_colored(f"Available Disk Space: {disk_info[3]}", BLUE)
        
        self.check_cuda_version()
    
    def check_cuda_version(self):
        self.print_colored("Checking CUDA availability...", YELLOW)
        
        success, output = self.run_command("nvidia-smi --query-gpu=name --format=csv,noheader,nounits", timeout=10, ignore_error=True)
        if success and output.strip():
            gpu_names = output.strip().split('\n')
            self.print_colored(f"  ✓ GPU(s) detected: {', '.join(gpu_names)}", GREEN)
            
            success, output = self.run_command("nvidia-smi | grep -oP 'CUDA Version: \\K[0-9.]+'", timeout=10, ignore_error=True)
            if success and output.strip():
                self.cuda_version = output.strip()
                self.print_colored(f"  ✓ CUDA Version: {self.cuda_version}", GREEN)
                return self.cuda_version
        
        success, output = self.run_command("nvcc --version", timeout=10, ignore_error=True)
        if success and 'release' in output:
            import re
            match = re.search(r'release (\d+\.\d+)', output)
            if match:
                self.cuda_version = match.group(1)
                self.print_colored(f"  ✓ CUDA Compiler Version: {self.cuda_version}", GREEN)
                return self.cuda_version
        
        self.print_colored("  ⚠ CUDA not detected (CPU-only mode)", YELLOW)
        return None
    
    def install_system_packages(self):
        self.print_banner("SYSTEM PACKAGES INSTALLATION")
        
        if not self.is_root:
            self.print_colored("ERROR: Root privileges required for system packages", RED)
            self.print_colored("Please run: sudo python3 cicada_dependency_manager.py", YELLOW)
            return False
        
        self.print_colored("Updating package repository...", YELLOW)
        success, _ = self.run_command(
            "apt-get update -qq",
            "Updating APT package lists",
            timeout=300
        )
        if not success:
            self.print_colored("  ⚠ Failed to update package lists", YELLOW)
        
        system_packages = [
            ("build-essential", "Compilation tools"),
            ("python3-dev", "Python development headers"),
            ("python3-pip", "Python package manager"),
            ("python3-venv", "Python virtual environments"),
            
            ("gpg", "GNU Privacy Guard"),
            ("gnupg2", "GNU Privacy Guard v2"),
            ("openssl", "OpenSSL toolkit"),
            ("steghide", "Steganography tool"),
            ("outguess", "Steganography detection"),
            ("stegosuite", "Steganography suite"),
            
            ("file", "File type identification"),
            ("xxd", "Hex dump utility"),
            ("hexdump", "Hex dump alternative"),
            ("binutils", "Binary analysis tools"),
            ("strings", "Extract strings from files"),
            ("grep", "Text pattern matching"),
            ("sed", "Stream editor"),
            ("awk", "Text processing"),
            
            ("imagemagick", "Image manipulation"),
            ("exiftool", "Metadata extraction"),
            ("libimage-exiftool-perl", "EXIF tool library"),
            
            ("curl", "HTTP client"),
            ("wget", "File downloader"),
            ("nmap", "Network scanner"),
            ("whois", "Domain information"),
            
            ("bc", "Calculator"),
            ("factor", "Number factorization"),
            ("units", "Unit conversion"),
            
            ("libssl-dev", "SSL development files"),
            ("libffi-dev", "Foreign function interface"),
            ("libgmp-dev", "GNU multiple precision arithmetic"),
            ("libmpfr-dev", "Multiple precision floating-point"),
            ("libmpc-dev", "Multiple precision complex arithmetic"),
            ("libjpeg-dev", "JPEG library"),
            ("libpng-dev", "PNG library"),
            ("libtiff-dev", "TIFF library"),
            ("libfreetype6-dev", "FreeType font engine"),
            
            ("p7zip-full", "7-Zip archiver"),
            ("unrar", "RAR archive extractor"),
            ("zip", "ZIP archiver"),
            ("unzip", "ZIP extractor"),
            
            ("git", "Version control"),
            ("htop", "System monitor"),
            ("tree", "Directory structure viewer"),
            ("tmux", "Terminal multiplexer"),
            ("screen", "Terminal multiplexer alternative"),
            
            ("sox", "Audio processing"),
            ("audacity", "Audio editor"),
            ("ffmpeg", "Multimedia framework"),
            
            ("nvidia-cuda-toolkit", "NVIDIA CUDA toolkit"),
            ("nvidia-cuda-dev", "CUDA development files"),
        ]
        
        total_packages = len(system_packages)
        installed_packages = []
        failed_packages = []
        
        for i, (package, description) in enumerate(system_packages, 1):
            progress = f"[{i}/{total_packages}]"
            self.print_colored(f"{progress} Installing {package}...", YELLOW)
            
            success, output = self.run_command(
                f"DEBIAN_FRONTEND=noninteractive apt-get install -y -qq {package}",
                timeout=300,
                ignore_error=True
            )
            
            if success or "already installed" in str(output).lower():
                self.print_colored(f"  ✓ {package} - {description}", GREEN)
                installed_packages.append(package)
            else:
                self.print_colored(f"  ✗ {package} - Failed or unavailable", RED)
                failed_packages.append(package)
        
        self.print_colored(f"\nInstallation summary:", BOLD)
        self.print_colored(f"  Successful: {len(installed_packages)}", GREEN)
        self.print_colored(f"  Failed: {len(failed_packages)}", RED if failed_packages else GREEN)
        
        if failed_packages:
            self.print_colored(f"  Failed packages: {', '.join(failed_packages[:10])}", YELLOW)
            if len(failed_packages) > 10:
                self.print_colored(f"  ... and {len(failed_packages) - 10} more", YELLOW)
        
        return True
    
    def install_python_packages(self):
        self.print_banner("PYTHON PACKAGES INSTALLATION")
        
        self.print_colored("Upgrading pip and setuptools...", YELLOW)
        for tool in ["pip", "setuptools", "wheel"]:
            success, _ = self.run_command(
                f"{sys.executable} -m pip install --upgrade {tool}",
                f"Upgrading {tool}",
                timeout=120
            )
            if success:
                self.print_colored(f"  ✓ {tool} upgraded", GREEN)
        
        python_packages = [
            ("numpy>=1.24.0", "Numerical computing"),
            ("scipy>=1.10.0", "Scientific computing"),
            ("sympy>=1.12", "Symbolic mathematics"),
            ("gmpy2>=2.1.0", "Multiple precision arithmetic"),
            ("matplotlib>=3.7.0", "Plotting and visualization"),
            ("seaborn>=0.12.0", "Statistical visualization"),
            ("plotly>=5.17.0", "Interactive plotting"),
            
            ("pycryptodome>=3.19.0", "Comprehensive cryptography"),
            ("cryptography>=41.0.0", "Modern cryptographic recipes"),
            ("hashlib", "Hashing algorithms"),
            ("base58>=2.1.0", "Base58 encoding"),
            ("base64", "Base64 encoding"),
            
            ("Pillow>=10.0.0", "Image processing"),
            ("opencv-python>=4.8.0", "Computer vision"),
            ("imageio>=2.31.0", "Image I/O"),
            ("scikit-image>=0.21.0", "Image processing algorithms"),
            ("stegano>=0.11.0", "Steganography tools"),
            
            ("nltk>=3.8.0", "Natural language processing"),
            ("textstat>=0.7.0", "Text statistics"),
            ("beautifulsoup4>=4.12.0", "HTML/XML parsing"),
            ("lxml>=4.9.0", "XML processing"),
            
            ("requests>=2.31.0", "HTTP library"),
            ("urllib3>=2.0.0", "HTTP client"),
            ("scrapy>=2.11.0", "Web scraping framework"),
            
            ("pandas>=2.1.0", "Data manipulation"),
            ("openpyxl>=3.1.0", "Excel file handling"),
            ("xlrd>=2.0.0", "Excel reading"),
            
            ("python-magic>=0.4.27", "File type detection"),
            ("PyPDF2>=3.0.0", "PDF processing"),
            ("python-docx>=0.8.11", "Word document processing"),
            
            ("librosa>=0.10.0", "Audio analysis"),
            ("soundfile>=0.12.0", "Audio file I/O"),
            ("pydub>=0.25.0", "Audio manipulation"),
            
            ("psutil>=5.9.0", "System monitoring"),
            ("tqdm>=4.66.0", "Progress bars"),
            ("rich>=13.7.0", "Rich terminal output"),
            ("colorama>=0.4.6", "Colored output"),
            ("click>=8.1.0", "Command line interface"),
            
            ("joblib>=1.3.0", "Parallel computing"),
            ("multiprocessing", "Multi-processing"),
            ("concurrent.futures", "Concurrent execution"),
            
            ("ipython>=8.15.0", "Enhanced Python shell"),
            ("jupyter>=1.0.0", "Jupyter notebooks"),
            ("memory-profiler>=0.61.0", "Memory profiling"),
            ("line-profiler>=4.1.0", "Line-by-line profiling"),
            
            ("networkx>=3.2.0", "Graph analysis"),
            ("igraph>=0.10.0", "Graph analysis alternative"),
            ("z3-solver>=4.12.0", "SMT solver"),
            ("sage", "Mathematical software system"),
        ]
        
        total_packages = len(python_packages)
        installed_packages = []
        failed_packages = []
        
        for i, (package, description) in enumerate(python_packages, 1):
            progress = f"[{i}/{total_packages}]"
            package_name = package.split('>=')[0].split('==')[0]
            
            self.print_colored(f"{progress} Installing {package_name}...", YELLOW)
            
            success, output = self.run_command(
                f"{sys.executable} -m pip install --no-cache-dir '{package}'",
                timeout=300,
                ignore_error=True
            )
            
            if success:
                self.print_colored(f"  ✓ {package_name} - {description}", GREEN)
                installed_packages.append(package_name)
            else:
                success, output = self.run_command(
                    f"{sys.executable} -m pip install --no-cache-dir {package_name}",
                    timeout=300,
                    ignore_error=True
                )
                
                if success:
                    self.print_colored(f"  ✓ {package_name} (latest) - {description}", GREEN)
                    installed_packages.append(package_name)
                else:
                    self.print_colored(f"  ✗ {package_name} - Installation failed", RED)
                    failed_packages.append(package_name)
        
        self.print_colored("\nInstalling specialized packages...", YELLOW)
        
        specialized_packages = [
            ("git+https://github.com/Legrandin/pycryptodome.git", "Latest PyCryptodome"),
            ("git+https://github.com/pyca/cryptography.git", "Latest Cryptography"),
        ]
        
        for package, description in specialized_packages:
            success, _ = self.run_command(
                f"{sys.executable} -m pip install --no-cache-dir {package}",
                f"Installing {description}",
                timeout=600,
                ignore_error=True
            )
            if success:
                self.print_colored(f"  ✓ {description}", GREEN)
        
        self.print_colored(f"\nPython packages summary:", BOLD)
        self.print_colored(f"  Successful: {len(installed_packages)}", GREEN)
        self.print_colored(f"  Failed: {len(failed_packages)}", RED if failed_packages else GREEN)
        
        return True
    
    def install_gpu_packages(self):
        self.print_banner("GPU PACKAGES INSTALLATION")
        
        cuda_version = self.check_cuda_version()
        
        if not cuda_version:
            self.print_colored("No CUDA detected. Skipping GPU packages.", YELLOW)
            return True
        
        self.print_colored(f"Installing GPU packages for CUDA {cuda_version}...", YELLOW)
        
        cuda_major = int(float(cuda_version.split('.')[0]))
        cupy_package = None
        
        if cuda_major >= 12:
            cupy_package = "cupy-cuda12x"
        elif cuda_major == 11:
            cupy_package = "cupy-cuda11x"
        elif cuda_major == 10:
            cupy_package = "cupy-cuda102"
        else:
            self.print_colored(f"Unsupported CUDA version: {cuda_version}", YELLOW)
            return False
        
        gpu_packages = [
            (cupy_package, "CuPy - NumPy for GPU"),
            ("numba", "JIT compiler with CUDA support"),
            ("pycuda", "Python CUDA bindings"),
            ("tensorflow-gpu", "TensorFlow with GPU support"),
            ("torch", "PyTorch"),
            ("jax[cuda]", "JAX with CUDA support"),
        ]
        
        for package, description in gpu_packages:
            success, _ = self.run_command(
                f"{sys.executable} -m pip install --no-cache-dir {package}",
                f"Installing {description}",
                timeout=600,
                ignore_error=True
            )
            if success:
                self.print_colored(f"  ✓ {package} installed", GREEN)
            else:
                self.print_colored(f"  ⚠ {package} failed - continuing", YELLOW)
        
        self.print_colored("Verifying GPU installation...", YELLOW)
        gpu_test_script = """
try:
    import cupy as cp
    print(f'✓ CuPy version: {cp.__version__}')
    print(f'✓ GPU: {cp.cuda.Device().name}')
    print(f'✓ Memory: {cp.cuda.Device().mem_info[1] / 1024**3:.1f} GB')
except ImportError:
    print('⚠ CuPy not available')
except Exception as e:
    print(f'⚠ GPU test failed: {e}')
"""
        
        success, output = self.run_command(
            f"{sys.executable} -c \"{gpu_test_script}\"",
            show_output=True,
            ignore_error=True
        )
        
        return True
    
    def setup_cicada_workspace(self):
        self.print_banner("CICADA 3301 WORKSPACE SETUP")
        
        directories = [
            "cicada_analysis",
            "cicada_analysis/data",
            "cicada_analysis/output", 
            "cicada_analysis/logs",
            "cicada_analysis/tools",
            "cicada_analysis/research",
            "cicada_analysis/temp"
        ]
        
        for directory in directories:
            dir_path = self.workspace_dir / directory
            dir_path.mkdir(exist_ok=True, parents=True)
            self.print_colored(f"  ✓ Created directory: {dir_path}", GREEN)
        
        config = {
            "cicada_number": "10412790658919985359827898739594318956404425106955675643739226952372682423852959081739834390370374475764863415203423499357108713631",
            "analysis_methods": [
                "basic_mathematical",
                "pattern_recognition", 
                "coordinate_analysis",
                "ascii_decoding",
                "book_cipher",
                "gematria",
                "steganography",
                "cryptographic"
            ],
            "workspace_dir": str(self.workspace_dir / "cicada_analysis"),
            "cuda_available": self.cuda_version is not None,
            "cuda_version": self.cuda_version
        }
        
        config_path = self.workspace_dir / "cicada_analysis" / "config.json"
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        self.print_colored(f"  ✓ Configuration saved to: {config_path}", GREEN)
        
        readme_content = """# Cicada 3301 Analysis Workspace

This workspace contains tools and data for analyzing the final Cicada 3301 puzzle.

## Structure
- `data/` - Input data and puzzle files
- `output/` - Analysis results and reports
- `logs/` - Execution logs
- `tools/` - Custom analysis tools
- `research/` - Research notes and references
- `temp/` - Temporary files

## Usage
Run the main solver: `python cicada_solver.py`

## Configuration
Edit `config.json` to modify analysis parameters.
"""
        
        readme_path = self.workspace_dir / "cicada_analysis" / "README.md"
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        
        self.print_colored(f"  ✓ README created: {readme_path}", GREEN)
        
        return True
    
    def verify_installation(self):
        self.print_banner("INSTALLATION VERIFICATION")
        
        python_version = sys.version.split()[0]
        self.print_colored(f"Python version: {python_version}", BLUE)
        
        self.print_colored("Verifying Python packages...", YELLOW)
        
        verification_script = """
import sys
import importlib

packages = {
    'numpy': 'NumPy',
    'scipy': 'SciPy', 
    'sympy': 'SymPy',
    'matplotlib': 'Matplotlib',
    'Crypto': 'PyCryptodome',
    'cryptography': 'Cryptography',
    'PIL': 'Pillow',
    'cv2': 'OpenCV',
    'requests': 'Requests',
    'pandas': 'Pandas',
    'nltk': 'NLTK',
    'psutil': 'psutil',
    'tqdm': 'tqdm',
    'rich': 'Rich'
}

installed = 0
total = len(packages)

for module, name in packages.items():
    try:
        m = importlib.import_module(module)
        version = getattr(m, '__version__', 'Unknown')
        print(f'✓ {name}: {version}')
        installed += 1
    except ImportError:
        print(f'✗ {name}: Not installed')

print(f'\\nPackage status: {installed}/{total} installed')
"""
        
        self.run_command(
            f"{sys.executable} -c \"{verification_script}\"",
            show_output=True,
            ignore_error=True
        )
        
        self.print_colored("\nVerifying system tools...", YELLOW)
        
        tools = [
            ('gpg', 'GNU Privacy Guard'),
            ('openssl', 'OpenSSL'),
            ('steghide', 'Steganography tool'),
            ('file', 'File type detection'),
            ('xxd', 'Hex dump'),
            ('convert', 'ImageMagick'),
            ('exiftool', 'EXIF tool'),
            ('factor', 'Number factorization')
        ]
        
        available_tools = 0
        for tool, description in tools:
            success, _ = self.run_command(f"which {tool}", timeout=5, ignore_error=True)
            if success:
                self.print_colored(f"  ✓ {tool} - {description}", GREEN)
                available_tools += 1
            else:
                self.print_colored(f"  ✗ {tool} - {description}", RED)
        
        self.print_colored(f"\nSystem tools: {available_tools}/{len(tools)} available", 
                          GREEN if available_tools > len(tools) // 2 else YELLOW)
        
        log_file = self.workspace_dir / "cicada_dependency_install.log"
        try:
            with open(log_file, 'w') as f:
                f.write('\n'.join(self.install_log))
            self.print_colored(f"\nInstallation log saved: {log_file}", GREEN)
        except Exception as e:
            self.print_colored(f"Could not save log: {e}", YELLOW)
        
        return True
    
    def install_all(self):
        self.print_banner("CICADA 3301 DEPENDENCY INSTALLER")
        
        self.check_system_info()
        
        if self.is_root:
            self.install_system_packages()
        else:
            self.print_colored("⚠ System packages skipped (not root)", YELLOW)
            self.print_colored("  Run with sudo for system packages", YELLOW)
        
        self.install_python_packages()
        
        self.install_gpu_packages()
        
        self.setup_cicada_workspace()
        
        self.verify_installation()
        
        self.print_banner("INSTALLATION COMPLETE")
        self.print_colored("🔍 Cicada 3301 analysis environment ready!", GREEN)
        self.print_colored(f"📁 Workspace: {self.workspace_dir / 'cicada_analysis'}", BLUE)
        self.print_colored("🚀 Run your solver: python cicada_solver.py", CYAN)
        
        return True

def main():
    manager = CicadaDependencyManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "--help" or command == "-h":
            print(f"""
{BOLD}Cicada 3301 Dependency Manager{NC}

Usage: python {sys.argv[0]} [OPTIONS]

Options:
  --system     Install system packages only (requires sudo)
  --python     Install Python packages only  
  --gpu        Install GPU packages only
  --workspace  Set up workspace only
  --verify     Verify installation
  --help, -h   Show this help message

Default: Install everything
""")
        elif command == "--system":
            manager.install_system_packages()
        elif command == "--python":
            manager.install_python_packages()
        elif command == "--gpu":
            manager.install_gpu_packages()
        elif command == "--workspace":
            manager.setup_cicada_workspace()
        elif command == "--verify":
            manager.verify_installation()
        else:
            print(f"Unknown option: {command}")
            print(f"Use --help for usage information")
    else:
        manager.install_all()

if __name__ == "__main__":
    main()