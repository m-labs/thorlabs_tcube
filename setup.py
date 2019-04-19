from setuptools import setup, find_packages

setup(
    name="thorlabs_tcube",
    install_requires=["asyncserial"],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "aqctl_thorlabs_tcube = thorlabs_tcube.aqctl_thorlabs_tcube:main",
        ],
    },
)
