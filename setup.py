import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="pytdb",
    version="0.1.0",
    author="Daryl Correa (Epicode)",
    author_email="daryl.correa@epicode.in",
    description="Python wrapper for Transient Database (TDB) which is part of Epicode's IraCluster.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/epicira/pytdb",
    project_urls = {
        "Bug Tracker": "https://github.com/epicira/pytdb/issues"
    },
    license="MIT",
    packages=["pytdb"],
    install_requires=[]
)
