import os
import PyInstaller.__main__

def create_executable():
    import site
    site_packages = site.getsitepackages()[0]

    PyInstaller.__main__.run([
        'main.py',
        '--name=WMM_Report_Generator',
        '--onefile',
        '--windowed',
        '--add-data=README.md:.',
        '--add-data=LICENSE:.',
        '--add-data=data/WMM.COF:data',
        '--add-data=gui:gui',
        '--add-data=src:src',
        '--hidden-import=PyQt6',
        '--hidden-import=PyQt6.QtCore',
        '--hidden-import=PyQt6.QtGui',
        '--hidden-import=PyQt6.QtWidgets',
        '--hidden-import=PyQt6.sip',
        '--hidden-import=openpyxl',
        '--hidden-import=numpy',
        '--hidden-import=pydantic',
        f'--add-data={os.path.join(site_packages, "PyQt6", "Qt6", "plugins", "platforms", "*.dll")};PyQt6/Qt6/plugins/platforms',
        f'--add-data={os.path.join(site_packages, "PyQt6", "Qt6", "bin", "*.dll")};PyQt6/Qt6/bin',
    ])

if __name__ == "__main__":
    create_executable()