from setuptools import find_packages, setup

setup(
    name='tms-alert-service',
    version='0.2.0',
    description='Alert service for n9e events with schedule/trading-day filtering and webhook delivery',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'fastapi==0.115.6',
        'uvicorn==0.32.1',
        'pymysql==1.1.1',
        'pydantic==2.10.3',
        'httpx==0.28.1',
        'croniter==6.0.0',
        'prometheus-client==0.21.1',
        'PyYAML==6.0.2',
    ],
    entry_points={
        'console_scripts': [
            'tms-alert-service=app.main:main',
        ],
    },
    python_requires='>=3.10',
)
