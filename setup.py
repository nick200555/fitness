from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = [x.strip() for x in f.read().splitlines() if x.strip() and not x.startswith("#")]

setup(
    name="fitness_wellness",
    version="0.0.1",
    description="Fitness & Wellness Management System",
    author="fitness_wellness",
    author_email="admin@fitness_wellness.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
