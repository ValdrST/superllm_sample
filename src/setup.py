from setuptools import setup, find_packages

with open("readme.md", "r", encoding="utf-8") as f:
    readme = f.read()

# Leer requirements.txt sin pip
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="superllm_sample",
    version="0.2.0",
    description="Sample LLM service",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Valdr Stiglitz",
    author_email="valdr.stiglitz@gmail.com",
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "superllm_sample=superllm_sample:main",
            "superllm_sampleWSGI=superllm_sample:wsgi"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)