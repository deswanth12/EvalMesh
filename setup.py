from setuptools import setup, find_packages

setup(
    name="evalmesh",
    version="0.3.0",
    author="EvalMesh Team",
    author_email="hello@evalmesh.com",
    description="Cloudflare & GitHub Actions for AI Agents - Real-Time WAF, DLP, RBAC & Evals",
    long_description=open("evalmesh/README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/evalmesh/evalmesh",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi>=0.100.0",
        "uvicorn>=0.22.0",
        "httpx>=0.24.0",
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0"
    ],
    entry_points={
        "console_scripts": [
            "evalmesh=evalmesh.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
)
