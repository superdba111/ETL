from setuptools import setup, find_packages

setup(
    name="commonPythonGlueLib",
    version="1.0.0",
    install_requires=['zcrmsdk', 'boto3', 'requests<2.27.2', 'pandas', 'numpy', 'awswrangler','PyJWT', 'cryptography', 'pyyaml', 'pybase64', 'jwt'],
    python_requires='>=3.6',
    packages=find_packages(exclude=["module_samples", 'db']),
    package_data={'': ['resources/*/*']},
    description="Ingestion pipelines",
    include_package_data=True,
    url="",
    email="farslan@opsguru.com"
)