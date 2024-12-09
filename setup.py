from setuptools import setup
from setuptools_rust import RustExtension

setup(
    name="iop-python",
    version="0.2.1",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Rust",
        "Programming Language :: Python :: Implementation :: CPython",
        "Development Status :: 5 - Production/Stable",
    ],
    rust_extensions=[RustExtension("iop_python", "Cargo.toml", binding="pyo3")],
    packages=["iop_python"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "kivy>=2.0.0",
        "maturin>=1.4,<2.0"
    ],
)
