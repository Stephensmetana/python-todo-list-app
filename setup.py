from setuptools import setup, find_packages

setup(
    name="python-todo-list-app",
    version="1.0.0",
    description="A fully featured command-line todo list manager with import/export, tags, priorities, and more.",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        # Add runtime dependencies here
    ],
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'todo-app=todo_app.main:main',
        ],
    },
    include_package_data=True,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
