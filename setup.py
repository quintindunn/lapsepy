from setuptools import setup

VERSION = "0.0.1"
DESCRIPTION = "A Python API wrapper for the social media app Lapse."
LONG_DESCRIPTION = "An unofficial API wrapper for the social media app Lapse."

with open("requirements.txt", 'r', encoding="utf-16") as f:
    requirements = [i.strip() for i in f.readlines()]

print(requirements)

setup(name='lapsepy',
      version=VERSION,
      description=DESCRIPTION,
      long_description_content_type="text/markdown",
      long_description=LONG_DESCRIPTION,
      author="Quintin Dunn",
      author_email="dunnquintin07@gmail.com",
      url="https://github.com/quintindunn/lapsepy",
      packages=['lapsepy'],
      keywords=['social media', 'lapsepy', 'api', 'api wrapper'],
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Operating System :: Microsoft :: Windows :: Windows 10',
            'Programming Language :: Python :: 3',
      ],
      install_requires=requirements
      )
