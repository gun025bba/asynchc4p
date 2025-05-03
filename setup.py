from setuptools import setup, find_packages

setup(
    name="async_http_client",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.9.1",
    ],
    author="Gallix",
    author_email="gallix.kim@gmail.com",
    description="An async HTTP client built with asyncio and aiohttp",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gallix/async-http-client",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
) 