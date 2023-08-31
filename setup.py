from setuptools import setup, find_packages


setup(
    name='is_face_detector',
    version='0.0.2',
    description='',
    url='http://github.com/labviros/is-face-detector',
    author='labviros',
    license='MIT',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'is-face-detector-stream=is_face_detector.stream:main',
            'is-face-detector-rpc=is_face_detector.rpc:main',
        ],
    },
    zip_safe=False,
    install_requires=[
        "is-msgs==1.1.18",
        "is-wire==1.2.1",
        "numpy==1.24.4",
        "nptyping==2.5.0",
        "opencv-contrib-python==4.8.0.76",
        "opencensus-ext-zipkin==0.2.1",
        "python-dateutil==2.8.0",
    ],
)