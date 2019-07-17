from setuptools import setup, find_packages

setup(
    name='is_face_detector',
    version='0.0.1',
    description='',
    url='http://github.com/labviros/is-face-detector',
    author='labviros',
    license='MIT',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'is-face-detector=is_face_detector.service:main',
        ],
    },
    zip_safe=False,
    install_requires=[
        'is-wire==1.2.0',
        'is-msgs==1.1.10',
        'opencv-python==4.1.0.*',
        'numpy==1.16.1',
    ],
)