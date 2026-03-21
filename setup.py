from setuptools import setup, find_packages

setup(
    name="ai-commit-translator",
    version="1.0.0",
    packages=find_packages(where=".", include=["src.*", "cli.*"]),
    package_dir={"": "."},
    python_requires=">=3.9",
    install_requires=[
        "openai>=1.0.0",
        "click>=8.1.0",
        "rich>=13.0.0",
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "ai-commit=cli.main:cli",
        ],
    },
)
