from setuptools import setup, find_packages

setup(
    name='tms-alert-service',
    version='0.1.0',
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
        'python-dotenv==1.0.1',
    ],
    entry_points={
        'console_scripts': [
            'tms-alert-service=tms_alert_service.main:main',
        ],
    },
    python_requires='>=3.10',
)
