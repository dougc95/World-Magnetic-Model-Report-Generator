import PyInstaller.__main__

def create_executable():
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
    ])

if __name__ == "__main__":
    create_executable()