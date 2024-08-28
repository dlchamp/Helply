from setuptools import find_packages, setup

setup(
    name="helply",
    version="0.6.1",
    description="A library that simplifies 'help' command creation for application commands in your discord bot.",
    author="DLCHAMP",
    author_email="contact@dlchamp.com",
    license="MIT",
    url="https://github.com/dlchamp/helply",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    python_requires=">=3.8.1,<4.0",
    extras_require={
        "dev": [
            "ruff>=0.0.275",
            "black>=23.3.0",
            "isort>=5.12.0",
            "pre-commit>=3.3.3",
            "pyright>=1.1.318",
            "python-dotenv>=1.0.0",
            "poetry-setup>=0.3.6",
        ],
        "docs": [
            "mkdocs>=1.5.1",
            "mkdocs-markdownextradata-plugin>=0.2.5",
            "mkdocstrings[python]>=0.22.0",
            "mkdocs-material>=9.1.21",
            "mkdocs-autorefs>=0.4.1",
            "mkdocs-gen-files>=0.5.0",
            "mkdocs-literate-nav>=0.6.0",
            "mkdocs-minify-plugin>=0.7.1",
        ],
        "lint": [
            "disnake>=2.9.0",
            "nextcord >= 2.6.0"
        ],
    },
)