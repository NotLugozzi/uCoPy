import sys
from cx_Freeze import setup, Executable

company_name = 'Mercury'
product_name = 'uCoPy'

bdist_msi_options = {
    'upgrade_code': '{48B079F4-B598-438D-A62A-8A233A3F8901}',
    'add_to_path': False,
    'initial_target_dir': r'[ProgramFilesFolder]\%s\%s' % (company_name, product_name),
}

build_exe_options = {
    'includes': ["tqdm"],
}

# GUI applications require a different base on Windows
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

exe = Executable(script='uCoPy.py', base=base)

setup(
    name=product_name,
    version='1.5',
    description='uCopy - an extremely lightweight file transfer utility',
    executables=[exe],
    options={
        'bdist_msi': bdist_msi_options,
        'build_exe': build_exe_options,
    }
)
