from setuptools import setup

VERSION = '1.3.0'

setup(
    name='PyWavefront',
    version=VERSION,
    author='Kurt Yoder',
    author_email='kyoder@gmail.com',
    maintainer="Einar Forselv",
    maintainer_email="eforselv@gmail.com",
    url='https://github.com/pywavefront/PyWavefront',
    description='Python library for importing Wavefront .obj files',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='BSD',
    classifiers=[
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Multimedia :: Graphics :: 3D Rendering',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=['pywavefront'],
    python_requires='>=3.4',
    extras_require={
        'visualization': ['pyglet'],
    },
)
