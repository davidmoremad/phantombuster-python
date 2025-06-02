from setuptools import setup, find_packages

def read_file(filename):
    with open(filename) as f:
        return f.read()

setup(
    name='pbuster',
    version=read_file('VERSION').strip(),
    author='David Amrani Hernandez',
    author_email='notme@null.com',
    description='PhantomBuster API client for Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords='phantombuster api client python',
    project_urls={
        'Documentation': 'https://phantombuster-python.readthedocs.io',
        'Source': 'https://github.com/davidmoremad/phantombuster-python'
    },
    url='https://github.com/davidmoremad/phantombuster-python',
    packages=find_packages(),
    license='MIT',
    include_package_data=True,  # Include files specified in MANIFEST.in
    install_requires=read_file('requirements.txt').splitlines(),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topics :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Internet :: WWW/HTTP :: Web Services',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    python_requires='>=3.6',
)