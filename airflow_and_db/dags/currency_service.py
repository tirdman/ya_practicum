from airflow.providers.docker.operators.docker import DockerOperator
import pendulum

from airflow import DAG

with DAG(
    dag_id="currency_service",
    schedule="0 */3 * * *",
    start_date=pendulum.datetime(2023, 12, 24, tz="UTC"),
    catchup=False,
) as dag:

    docker_test_task = DockerOperator(
        task_id='get_currency_rate',
        image='currency_rate',
        api_version='auto',
        auto_remove=True,
        mount_tmp_dir=False,
        container_name='currency-rate-container',
        # docker_url='unix://var/run/docker.sock',
        docker_url='tcp://docker-proxy:2375',
        network_mode='ya_practicum',
        environment = {
            'CURRENCY_PAIR': 'USD,BTC'
        }
    )
