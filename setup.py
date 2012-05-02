from setuptools import setup

setup(
    name='Skeletor',
    version='0.1.0',
    url='https://github.com/jpvanhal/skeletor',
    license='BSD',
    author='Janne Vanhala',
    author_email='janne.vanhala@gmail.com',
    description='Simple project skeleton builder.',
    long_description=open('README.rst').read() + '\n\n' +
                     open('CHANGES.rst').read(),
    py_modules=['skeletor'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=['jinja2'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    scripts=['bin/skeletor'],
)
