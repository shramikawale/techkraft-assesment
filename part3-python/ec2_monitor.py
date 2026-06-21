#!/usr/bin/env python3

import argparse
import boto3
import json
import logging
from typing import Dict, List, Any, Optional
from botocore.exceptions import BotoCoreError, ClientError
from datetime import datetime, timedelta


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_config(config_path: str) -> Dict[str, Any]:
    try:
        with open(config_path, "r") as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Error loading config file: {e}")
        return {}


def get_running_instances(ec2_client) -> List[Dict[str, Any]]:
    instances = []

    try:
        paginator = ec2_client.get_paginator("describe_instances")

        for page in paginator.paginate(
            Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
        ):
            for reservation in page["Reservations"]:
                for instance in reservation["Instances"]:
                    name = "N/A"

                    if "Tags" in instance:
                        for tag in instance["Tags"]:
                            if tag["Key"] == "Name":
                                name = tag["Value"]

                    instances.append({
                        "InstanceId": instance["InstanceId"],
                        "Name": name,
                        "InstanceType": instance["InstanceType"]
                    })

        return instances

    except (BotoCoreError, ClientError) as e:
        logger.error(f"Error fetching EC2 instances: {e}")
        return []


def get_cpu_metrics(cloudwatch_client, instance_id: str) -> Optional[Dict[str, float]]:
    try:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=1)

        response = cloudwatch_client.get_metric_statistics(
            Namespace="AWS/EC2",
            MetricName="CPUUtilization",
            Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=["Average", "Minimum", "Maximum"]
        )

        data_points = response.get("Datapoints", [])

        if not data_points:
            return None

        avg = sum(dp["Average"] for dp in data_points) / len(data_points)
        min_val = min(dp["Minimum"] for dp in data_points)
        max_val = max(dp["Maximum"] for dp in data_points)

        return {
            "average": round(avg, 2),
            "min": round(min_val, 2),
            "max": round(max_val, 2)
        }

    except (BotoCoreError, ClientError) as e:
        logger.error(f"CloudWatch error for {instance_id}: {e}")
        return None


def generate_report(ec2_client, cloudwatch_client, threshold: float) -> List[Dict[str, Any]]:
    report = []
    instances = get_running_instances(ec2_client)

    for instance in instances:
        metrics = get_cpu_metrics(cloudwatch_client, instance["InstanceId"])

        if not metrics:
            continue

        report.append({
            "InstanceId": instance["InstanceId"],
            "Name": instance["Name"],
            "InstanceType": instance["InstanceType"],
            "CPU": metrics,
            "Flagged": metrics["average"] > threshold
        })

    return report


def save_report(report: List[Dict[str, Any]], output_file: str) -> None:
    try:
        with open(output_file, "w") as file:
            json.dump(report, file, indent=4)

        logger.info(f"Report saved to {output_file}")

    except Exception as e:
        logger.error(f"Error writing report: {e}")


def main():
    parser = argparse.ArgumentParser(description="EC2 Monitoring Script")

    parser.add_argument("--region", required=True, help="AWS region")
    parser.add_argument("--threshold", type=float, default=80, help="CPU threshold")
    parser.add_argument("--output", required=True, help="Output JSON file")
    parser.add_argument("--config", default="config.json", help="Config file path")

    args = parser.parse_args()

    config = load_config(args.config)
    threshold = args.threshold or config.get("alert_threshold", 80)

    try:
        ec2_client = boto3.client("ec2", region_name=args.region)
        cloudwatch_client = boto3.client("cloudwatch", region_name=args.region)

        logger.info("Starting EC2 monitoring...")

        report = generate_report(ec2_client, cloudwatch_client, threshold)
        save_report(report, args.output)

        logger.info("Monitoring completed successfully.")

    except (BotoCoreError, ClientError) as e:
        logger.error(f"AWS API error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
