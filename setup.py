from setuptools import setup, find_packages


def get_requirements(req_file="requirements.txt"):
    lines = [line.strip() for line in open(req_file)]
    return [line for line in lines if line]


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
            'is-face-detector-stream=is_face_detector.stream:main',
            'is-face-detector-rpc=is_face_detector.rpc:main',
        ],
    },
    zip_safe=False,
    install_requires=get_requirements(req_file="requirements.txt"),
)