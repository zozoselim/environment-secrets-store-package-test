import setuptools

setuptools.setup(
    name="environment-secrets-store",
    version="0.0.1",
    author="NovaVision AI",
    author_email="info@novavision.ai",
    description="Environment Secrets Store component for NovaVision",
    url="https://github.com/zozoselim/environment-secrets-store-package-test",
    license='MIT',
    install_requires=['sdk', 'opencv-python-headless'],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    packages=[
        'novavision.package',
        'novavision.package.classes',
        'novavision.package.configs',
        'novavision.package.dataloaders',
        'novavision.package.executors',
        'novavision.package.models',
        'novavision.package.utils',
        'novavision.package.weights'
    ],
    package_dir={'novavision.package': 'src'},
    python_requires=">=3.6"
)
